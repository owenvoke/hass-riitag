"""Constants for the RiiTag integration."""
from datetime import timedelta
from typing import Final

DOMAIN: Final = "riitag"

DEFAULT_SCAN_INTERVAL: Final = timedelta(minutes=5)

SENSOR_KEY_USERNAME = "username"
SENSOR_KEY_TAG_URL = "tag_url"
SENSOR_KEY_LAST_PLAYED = "last_played"
