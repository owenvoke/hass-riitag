import logging
from datetime import timedelta

from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import RiiTagUpdateCoordinator
from .entity import RiiTagSensorEntity
from .const import (
    DOMAIN,
    SENSOR_KEY_USERNAME,
    SENSOR_KEY_TAG_URL,
    SENSOR_KEY_LAST_PLAYED, DEFAULT_SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]

SCAN_INTERVAL = DEFAULT_SCAN_INTERVAL

SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key=SENSOR_KEY_USERNAME,
        name="Username",
        icon="mdi:account",
    ),
    SensorEntityDescription(
        key=SENSOR_KEY_TAG_URL,
        name="Tag URL",
        icon="mdi:link",
    ),
    SensorEntityDescription(
        key=SENSOR_KEY_LAST_PLAYED,
        name="Last Played",
        icon="mdi:controller-classic",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up all sensors for this entry."""
    coordinator: RiiTagUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        RiiTagSensorEntity(coordinator, entry, description) for description in SENSORS
    )
