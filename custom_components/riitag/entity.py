from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_UNAVAILABLE
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import RiiTagUpdateCoordinator, DOMAIN
from .const import (
    SENSOR_KEY_TAG,
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
        if self.entity_description.key == SENSOR_KEY_TAG:
            return self.coordinator.data["game_data"]["last_played"]["game_id"]

        return STATE_UNAVAILABLE

    @property
    def extra_state_attributes(self):
        if self.entity_description.key == SENSOR_KEY_TAG:
            return {
                "user_id": self.coordinator.data["user"]["id"],
                "user_name": self.coordinator.data["user"]["name"],
                "tag_url": self.coordinator.data["tag_url"]["normal"],
                "tag_url_hd": self.coordinator.data["tag_url"]["max"],
                "last_played_game_id": self.coordinator.data["game_data"][
                    "last_played"
                ]["game_id"],
                "last_played_console": self.coordinator.data["game_data"][
                    "last_played"
                ]["console"],
                "last_played_cover_url": self.coordinator.data["game_data"][
                    "last_played"
                ]["cover_url"],
                "last_played_time": str(
                    self.coordinator.data["game_data"]["last_played"]["time"]
                ),
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
