"""Heatmiser Wifi Platform for Home Assistant."""
from __future__ import annotations
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.discovery import load_platform
from heatmiser_wifi import Heatmiser
from homeassistant.components.climate import (ClimateEntity)

from homeassistant.const import (
    CONF_HOST, CONF_PORT, CONF_PIN, ATTR_FRIENDLY_NAME )

import logging
_LOGGER = logging.getLogger(__name__)

import voluptuous as vol
import homeassistant.helpers.config_validation as cv

DOMAIN = 'heatmiser_wifi'

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_HOST): cv.string,
                vol.Optional(CONF_PORT, default=8068): cv.port,
                vol.Optional(CONF_PIN, default=0): cv.positive_int,
                vol.Optional(ATTR_FRIENDLY_NAME, default='_not_set_'): cv.string,
                vol.Optional('max_temp', default=25): cv.positive_int,
                vol.Optional('min_temp', default=5): cv.positive_int,
                vol.Optional('step_temp', default=1): cv.positive_int
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

def setup(hass: HomeAssistant, config: ConfigType) -> bool:

    heatmiser = Heatmiser(config[DOMAIN].get(CONF_HOST),config[DOMAIN].get(CONF_PORT),config[DOMAIN].get(CONF_PIN))

    heatmiser.connect()

    hass.data[DOMAIN] = {
        'name': config[DOMAIN].get(ATTR_FRIENDLY_NAME),
        'max_temp': config[DOMAIN].get('max_temp'),
        'min_temp': config[DOMAIN].get('min_temp'),
        'temp_step': config[DOMAIN].get('step_temp'),
        'time_offset': 0,
        'heatmiser' : heatmiser,
        'heatmiser_info': heatmiser.get_info()
    }

    heatmiser.disconnect()

    load_platform(hass, 'climate', DOMAIN, {}, config)
    load_platform(hass, 'sensor', DOMAIN, {}, config)
    load_platform(hass, 'switch', DOMAIN, {}, config)
    load_platform(hass, 'number', DOMAIN, {}, config)

    def set_value(call):
        name = call.data.get("name")
        value = call.data.get("value")

        hass.data[DOMAIN]['heatmiser'].connect()
        hass.data[DOMAIN]['heatmiser'].set_value(name,value)
        hass.data[DOMAIN]['heatmiser'].disconnect()
        hass.data[DOMAIN]['heatmiser_info'][name] = value

    def update_date_time(call):
        hass.data[DOMAIN]['heatmiser'].connect()
        hass.data[DOMAIN]['heatmiser'].set_value('date_time',hass.data[DOMAIN]['time_offset'])
        hass.data[DOMAIN]['heatmiser'].disconnect()

    def update_triggers(call):
        trigger = call.data.get("trigger")
        values = call.data.get("values")
        hass.data[DOMAIN]['heatmiser'].connect()
        hass.data[DOMAIN]['heatmiser'].set_value(trigger,values)
        hass.data[DOMAIN]['heatmiser'].disconnect()
        hass.data[DOMAIN]['heatmiser_info'][trigger] = values

    hass.services.register(DOMAIN, "set_value", set_value)
    hass.services.register(DOMAIN, "update_date_time", update_date_time)
    hass.services.register(DOMAIN, "update_triggers", update_triggers)

    return True
