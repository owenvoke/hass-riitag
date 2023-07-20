from __future__ import annotations

from datetime import timedelta
import logging
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.const import (
    CONF_USERNAME,
    CONF_SCAN_INTERVAL,
)
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from riitag import RiiTag, NotFoundException

import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL

_LOGGER: logging.Logger = logging.getLogger(__package__)

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
            vol.Coerce(int), vol.Range(min=1)
        ),
    }
)


class RiiTagConfigFlow(ConfigFlow, domain=DOMAIN):
    """The configuration flow for a RiiTag system."""

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input:
            try:
                tag = await self.hass.async_add_executor_job(
                    lambda: get_tag(
                        username=user_input[CONF_USERNAME],
                    )
                )
                if tag:
                    await self.async_set_unique_id(
                        f"riitag_{user_input[CONF_USERNAME]}"
                    )
                    self._abort_if_unique_id_configured()

                    return self.async_create_entry(
                        title=f"RiiTag ({user_input[CONF_USERNAME]})",
                        data=user_input,
                    )
            except NotFoundException:
                errors[CONF_USERNAME] = "invalid_username"
            else:
                errors[CONF_USERNAME] = "server_error"

        return self.async_show_form(
            step_id="user", data_schema=CONFIG_SCHEMA, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> RiiTagOptionsFlowHandler:
        return RiiTagOptionsFlowHandler(config_entry)


class RiiTagOptionsFlowHandler(OptionsFlow):
    """Config flow options handler for RiiTag."""

    def __init__(self, config_entry: ConfigEntry):
        """Initialize options flow."""
        self.config_entry = config_entry
        # Cast from MappingProxy to dict to allow update.
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            self.options.update(user_input)
            coordinator = self.hass.data[DOMAIN][self.config_entry.entry_id]

            update_interval = timedelta(
                seconds=self.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
            )

            _LOGGER.debug("Updating coordinator, update_interval: %s", update_interval)

            coordinator.update_interval = update_interval

            return self.async_create_entry(title="", data=self.options)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=1)),
                }
            ),
        )


def get_tag(username: str):
    return RiiTag().tags.get(username)
