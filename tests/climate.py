"""Heatmiser Wifi Platform for Home Assistant."""
import logging

from heatmiser_wifi import Heatmiser
import voluptuous as vol

import homeassistant.helpers.config_validation as cv

from homeassistant.components.climate import (
    PLATFORM_SCHEMA, ClimateEntity)

from homeassistant.components.climate.const import (
    SUPPORT_TARGET_TEMPERATURE, SUPPORT_PRESET_MODE, SUPPORT_AUX_HEAT, HVAC_MODE_OFF,
    HVAC_MODE_HEAT, CURRENT_HVAC_OFF, CURRENT_HVAC_HEAT,
    CURRENT_HVAC_IDLE, PRESET_HOME, PRESET_AWAY, ATTR_AUX_HEAT)

from homeassistant.const import (
    CONF_HOST, CONF_PORT, CONF_PIN, TEMP_CELSIUS, TEMP_FAHRENHEIT, 
    ATTR_FRIENDLY_NAME, ATTR_TEMPERATURE)

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_PORT, default=8068): cv.port,
    vol.Optional(CONF_PIN, default=0): cv.positive_int,
    vol.Optional(ATTR_FRIENDLY_NAME, default='_not_set_'): cv.string
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    # Assign configuration variables.
    # The configuration check takes care they are present.
    host = config[CONF_HOST]
    port = config[CONF_PORT]
    pin = config[CONF_PIN]
    name = config[ATTR_FRIENDLY_NAME]

    # Add devices
    add_entities([HeatmiserWifi(host, port, pin, name)], True)


class HeatmiserWifi(ClimateEntity):

    def __init__(self, host, port, pin, name):
        self._heatmiser = Heatmiser(host,port,pin)
        self._heatmiser_info = []
        self._name = name

    @property
    def name(self):
        if self._name == '_not_set_':
            self._name = 'Heatmiser ' + self._heatmiser_info['model']
        return self._name

    @property
    def supported_features(self):
        return SUPPORT_TARGET_TEMPERATURE | SUPPORT_PRESET_MODE | SUPPORT_AUX_HEAT

    @property
    def temperature_unit(self):
        if self._heatmiser_info['temperature_format'] == 'Celsius':
            return TEMP_CELSIUS
        return TEMP_FAHRENHEIT

    @property
    def current_temperature(self):
        return self._heatmiser_info['air_temp']

    @property
    def target_temperature(self):
        if self._heatmiser_info['run_mode'] == 'Frost protection mode':
            return self._heatmiser_info['frost_protect_temperature']
        return self._heatmiser_info['set_room_temp']

    @property
    def target_temperature_high(self):
        self.target_temperature()

    @property
    def target_temperature_low(self):
        return self.target_temperature() - self._heatmiser_info['switch_differential']

    @property
    def max_temp(self):
        if self._heatmiser_info['temperature_format'] == 'Celsius':
            return 35 # Celsius
        return 95 # Fahrenheit

    @property
    def min_temp(self):
        if self._heatmiser_info['temperature_format'] == 'Celsius':
            return 5 # Celsius
        return 45 # Fahrenheit

    @property
    def hvac_mode(self):
        if self._heatmiser_info['on_off'] == 'Off':
            return HVAC_MODE_OFF
        return HVAC_MODE_HEAT

    @property
    def hvac_modes(self):
        return [HVAC_MODE_OFF, HVAC_MODE_HEAT]

    @property
    def preset_mode(self):
        if self._heatmiser_info['run_mode'] == 'Frost protection mode':
            return PRESET_AWAY
        return PRESET_HOME

    @property
    def preset_modes(self):
        return [PRESET_HOME, PRESET_AWAY]

    @property
    def hvac_action(self):
        if self._heatmiser_info['on_off'] == 'Off':
            return CURRENT_HVAC_OFF
        elif self._heatmiser_info['heating_is_currently_on']:
            return CURRENT_HVAC_HEAT
        return CURRENT_HVAC_IDLE

    @property
    def is_aux_heat(self):
        #return self._heatmiser_info['hot_water']
        return 1


    def set_temperature(self, **kwargs):
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature == None:
            return
        self._heatmiser.connect()
        if self._heatmiser_info['run_mode'] == 'Frost protection mode':
            self._heatmiser.set_value('frost_protect_temperature', temperature)
        else:
            self._heatmiser.set_value('set_room_temp', temperature)
        self._heatmiser_info = self._heatmiser.get_info() # Update
        self._heatmiser.disconnect()

    def set_hvac_mode(self, hvac_mode):
        on_off = 'On'
        if hvac_mode == HVAC_MODE_OFF:
            on_off = 'Off'
        elif hvac_mode != HVAC_MODE_HEAT:
            return # Invalid mode return
        self._heatmiser.connect()
        self._heatmiser.set_value('on_off', on_off)
        self._heatmiser_info = self._heatmiser.get_info() # Update
        self._heatmiser.disconnect()

    def set_preset_mode(self, preset_mode):
        run_mode = 'Heating mode (normal mode)'
        if preset_mode == PRESET_AWAY:
            run_mode = 'Frost protection mode'
        elif preset_mode != PRESET_HOME:
            return # Invalid mode return
        self._heatmiser.connect()
        self._heatmiser.set_value('run_mode', run_mode)
        self._heatmiser_info = self._heatmiser.get_info() # Update
        self._heatmiser.disconnect()
        
    def turn_aux_heat_on(self):
        self._heatmiser.connect()
        self._heatmiser.set_value('hot_water', 'on')
        self._heatmiser_info = self._heatmiser.get_info() # Update
        self._heatmiser.disconnect()

    def turn_aux_heat_off(self):
        self._heatmiser.connect()
        self._heatmiser.set_value('hot_water', 'off')
        self._heatmiser_info = self._heatmiser.get_info() # Update
        self._heatmiser.disconnect()

    def update(self):
        self._heatmiser.connect()
        self._heatmiser_info = self._heatmiser.get_info()
        self._heatmiser.disconnect()
