import logging
from datetime import timedelta

import async_timeout
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from riitag import RiiTag, Tag

_LOGGER = logging.getLogger(__name__)


class RiiTagUpdateCoordinator(DataUpdateCoordinator[Tag]):
    """Coordinates updates between all RiiTag sensors defined."""

    def __init__(
        self,
        hass: HomeAssistant,
        name: str,
        username: str,
        update_interval: timedelta,
    ) -> None:
        self._riitag = RiiTag()
        self._username = username

        """Initialize the UpdateCoordinator for RiiTag sensors."""
        super().__init__(
            hass,
            _LOGGER,
            name=name,
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> Tag:
        async with async_timeout.timeout(5):
            return await self.hass.async_add_executor_job(
                lambda: self._riitag.tags.get(self._username)
            )
