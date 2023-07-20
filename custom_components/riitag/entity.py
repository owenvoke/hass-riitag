from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_UNAVAILABLE
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import RiiTagUpdateCoordinator, DOMAIN
from .const import (
    SENSOR_KEY_USERNAME,
    SENSOR_KEY_TAG_URL,
    SENSOR_KEY_LAST_PLAYED,
)


class RiiTagSensorEntity(CoordinatorEntity[RiiTagUpdateCoordinator], SensorEntity):
    """Representation of a RiiTag sensor."""

    entity_description: SensorEntityDescription

    def __init__(
        self,
        coordinator: RiiTagUpdateCoordinator,
        entry: ConfigEntry,
        description: SensorEntityDescription,
    ):
        """Initialize the sensor and set the update coordinator."""
        super().__init__(coordinator)
        self._attr_name = description.name
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"

        self.entry = entry
        self.entity_description = description

    @property
    def native_value(self) -> str:
        if self.entity_description.key == SENSOR_KEY_USERNAME:
            return self.coordinator.data["user"]["name"]

        if self.entity_description.key == SENSOR_KEY_TAG_URL:
            return self.coordinator.data["tag_url"]["normal"]

        if self.entity_description.key == SENSOR_KEY_LAST_PLAYED:
            return self.coordinator.data["game_data"]["last_played"]["game_id"]

        return STATE_UNAVAILABLE

    @property
    def extra_state_attributes(self):
        if self.entity_description.key == SENSOR_KEY_USERNAME:
            return {"id": self.coordinator.data["user"]["id"]}

        if self.entity_description.key == SENSOR_KEY_TAG_URL:
            return {"hd": self.coordinator.data["tag_url"]["max"]}

        if self.entity_description.key == SENSOR_KEY_LAST_PLAYED:
            return {
                "console": self.coordinator.data["game_data"]["last_played"]["console"],
                "cover_url": self.coordinator.data["game_data"]["last_played"][
                    "cover_url"
                ],
                "time": self.coordinator.data["game_data"]["last_played"]["time"],
            }

        return {}

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            name=self.coordinator.name,
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, f"{self.entry.entry_id}")},
            manufacturer="RiiTag",
        )
