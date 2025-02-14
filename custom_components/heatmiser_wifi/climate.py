"""Heatmiser Wifi Platform for Home Assistant."""
from __future__ import annotations
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from heatmiser_wifi import Heatmiser
from homeassistant.components.climate import (ClimateEntity)

from homeassistant.components.climate.const import (
    PRESET_HOME, PRESET_AWAY, HVACMode, HVACAction, ClimateEntityFeature)

from homeassistant.const import (
    ATTR_FRIENDLY_NAME, ATTR_TEMPERATURE, UnitOfTemperature)

import logging
_LOGGER = logging.getLogger(__name__)

from . import DOMAIN

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    add_entities([HeatmiserWifi()])


class HeatmiserWifi(ClimateEntity):
    def __init__(self) -> None:
        self._state = None

    @property
    def name(self):
        if self.hass.data[DOMAIN]['name'] == '_not_set_':
            self._name = 'Heatmiser ' + self.hass.data[DOMAIN]['heatmiser_info']['model']
        else:
            self._name = self.hass.data[DOMAIN]['name']
        return self._name

    @property
    def supported_features(self):
        return ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.PRESET_MODE

    @property
    def temperature_unit(self):
        if self.hass.data[DOMAIN]['heatmiser_info']['temperature_format'] == 'Celsius':
            return UnitOfTemperature.CELSIUS
        return UnitOfTemperature.FAHRENHEIT

    @property
    def current_temperature(self):
        return self.hass.data[DOMAIN]['heatmiser_info']['air_temp']

    @property
    def target_temperature(self):
        if self.hass.data[DOMAIN]['heatmiser_info']['run_mode'] == 'Frost protection mode':
            return self.hass.data[DOMAIN]['heatmiser_info']['frost_protect_temperature']
        return self.hass.data[DOMAIN]['heatmiser_info']['set_room_temp']

    @property
    def target_temperature_high(self):
        return self.target_temperature()

    @property
    def target_temperature_low(self):
        return self.target_temperature() - self.hass.data[DOMAIN]['heatmiser_info']['switch_differential']

    @property
    def target_temperature_step(self):
        return self.hass.data[DOMAIN]['temp_step']

    @property
    def max_temp(self):
        if self.hass.data[DOMAIN]['heatmiser_info']['run_mode'] == 'Frost protection mode':
            return self.hass.data[DOMAIN]['heatmiser_info']['frost_protect_temperature']
        return self.hass.data[DOMAIN]['max_temp']

    @property
    def min_temp(self):
        if self.hass.data[DOMAIN]['heatmiser_info']['run_mode'] == 'Frost protection mode':
            return self.hass.data[DOMAIN]['heatmiser_info']['frost_protect_temperature']
        return self.hass.data[DOMAIN]['min_temp']

    @property
    def hvac_mode(self):
        if self.hass.data[DOMAIN]['heatmiser_info']['on_off'] == 'Off':
            return HVACMode.OFF
        return HVACMode.HEAT

    @property
    def hvac_modes(self):
        return [HVACMode.OFF, HVACMode.HEAT]

    @property
    def preset_mode(self):
        run_mode = self.hass.data[DOMAIN]['heatmiser_info']['run_mode']
        away_mode = self.hass.data[DOMAIN]['heatmiser_info']['away_mode']
        if run_mode == 'Frost protection mode':
            if away_mode == 'On':
                return PRESET_AWAY
            else:
                return 'Summer'
        return PRESET_HOME

    @property
    def preset_modes(self):
        return [PRESET_HOME, PRESET_AWAY, 'Summer']

    @property
    def hvac_action(self):
        if self.hass.data[DOMAIN]['heatmiser_info']['on_off'] == 'Off':
            return HVACAction.OFF
        elif self.hass.data[DOMAIN]['heatmiser_info']['heating_is_currently_on']:
            return HVACAction.HEATING
        return HVACAction.IDLE

    def set_temperature(self, **kwargs):
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature == None:
            return
        self.hass.data[DOMAIN]['heatmiser'].connect()
        self.hass.data[DOMAIN]['heatmiser'].set_value('set_room_temp', temperature)
        self.hass.data[DOMAIN]['heatmiser'].disconnect()

    def set_hvac_mode(self, hvac_mode):
        on_off = 'On'
        if hvac_mode == HVACMode.OFF:
            on_off = 'Off'
        elif hvac_mode != HVACMode.HEAT:
            return # Invalid mode return
        self.hass.data[DOMAIN]['heatmiser'].connect()
        self.hass.data[DOMAIN]['heatmiser'].set_value('on_off', on_off)
        self.hass.data[DOMAIN]['heatmiser'].disconnect()

    def set_preset_mode(self, preset_mode):
        away_mode = 'Off'
        run_mode = 'Heating mode (normal mode)'
        if preset_mode == PRESET_AWAY:
            away_mode = 'On'
            run_mode = 'Frost protection mode'
        elif preset_mode == 'Summer':
            run_mode = 'Frost protection mode'
        elif preset_mode != PRESET_HOME:
            return # Invalid mode return
        self.hass.data[DOMAIN]['heatmiser'].connect()
        self.hass.data[DOMAIN]['heatmiser'].set_value('away_mode', away_mode)
        self.hass.data[DOMAIN]['heatmiser'].set_value('run_mode', run_mode)
        self.hass.data[DOMAIN]['heatmiser'].disconnect()

    def update(self):
        self.hass.data[DOMAIN]['heatmiser'].connect()
        self.hass.data[DOMAIN] = {
          'name': self.hass.data[DOMAIN]['name'],
          'max_temp': self.hass.data[DOMAIN]['max_temp'],
          'min_temp': self.hass.data[DOMAIN]['min_temp'],
          'temp_step': self.hass.data[DOMAIN]['temp_step'],
          'time_offset': self.hass.data[DOMAIN]['time_offset'],
          'heatmiser': self.hass.data[DOMAIN]['heatmiser'],
          'heatmiser_info': self.hass.data[DOMAIN]['heatmiser'].get_info()
        }
        self.hass.data[DOMAIN]['heatmiser'].disconnect()

