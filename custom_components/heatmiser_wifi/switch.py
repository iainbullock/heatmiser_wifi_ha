from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import DOMAIN

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    if discovery_info is None:
        return
    add_entities([key_lock_Switch()])


class key_lock_Switch(SwitchEntity):
    def __init__(self) -> None:
        self._state = None

    @property
    def name(self) -> str:
        return self.hass.data[DOMAIN]['name'] + '_key_lock'

    @property
    def icon(self) -> str | None:
        return 'mdi:lock'

    @property
    def is_on(self) -> bool | None:
        return self._state

    def turn_on(self, **kwargs) -> None: 
        self.hass.data[DOMAIN]['heatmiser'].connect()
        self.hass.data[DOMAIN]['heatmiser'].set_value('key_lock','Lock')
        self.hass.data[DOMAIN]['heatmiser'].disconnect()
        self.hass.data[DOMAIN]['heatmiser_info']['key_lock'] = 'Lock'

    def turn_off(self, **kwargs) -> None: 
        self.hass.data[DOMAIN]['heatmiser'].connect()
        self.hass.data[DOMAIN]['heatmiser'].set_value('key_lock','Unlock')
        self.hass.data[DOMAIN]['heatmiser'].disconnect()
        self.hass.data[DOMAIN]['heatmiser_info']['key_lock'] = 'Unlock'

    def toggle(self, **kwargs) -> None: 
        self.hass.data[DOMAIN]['heatmiser'].connect()
        if self.hass.data[DOMAIN]['heatmiser_info']['key_lock'] == 'Lock':
            self.hass.data[DOMAIN]['heatmiser'].set_value('key_lock','Unlock')
            self.hass.data[DOMAIN]['heatmiser_info']['key_lock'] = 'Unlock'
        else:
            self.hass.data[DOMAIN]['heatmiser'].set_value('key_lock','Lock')
            self.hass.data[DOMAIN]['heatmiser_info']['key_lock'] = 'Lock'
        self.hass.data[DOMAIN]['heatmiser'].disconnect()

    def update(self) -> None:
        if (self.hass.data[DOMAIN]['heatmiser_info']['key_lock'] == 'Lock'):
            self._state = 1
        else:
            self._state = 0

"""
# Disabled as this is managed by Climate entity
class frost_mode_Switch(SwitchEntity):
    def __init__(self) -> None:
        self._state = None

    @property
    def name(self) -> str:
        return self.hass.data[DOMAIN]['name'] + '_frost_mode'

    @property
    def icon(self) -> str | None:
        return 'mid:snowflake-thermometer'

    @property
    def is_on(self) -> bool | None:
        return self._state

    def turn_on(self, **kwargs) -> None: 
        self.hass.data[DOMAIN]['heatmiser'].connect()
        self.hass.data[DOMAIN]['heatmiser'].set_value('run_mode','Frost protection mode')
        self.hass.data[DOMAIN]['heatmiser'].disconnect()
        self.hass.data[DOMAIN]['heatmiser_info']['run_mode'] = 'Frost protection mode'

    def turn_off(self, **kwargs) -> None: 
        self.hass.data[DOMAIN]['heatmiser'].connect()
        self.hass.data[DOMAIN]['heatmiser'].set_value('run_mode','Heating mode (normal mode)')
        self.hass.data[DOMAIN]['heatmiser'].disconnect()
        self.hass.data[DOMAIN]['heatmiser_info']['run_mode'] = 'Heating mode (normal mode)'

    def toggle(self, **kwargs) -> None: 
        self.hass.data[DOMAIN]['heatmiser'].connect()
        if self.hass.data[DOMAIN]['heatmiser_info']['run_mode'] == 'Frost protection mode':
            self.hass.data[DOMAIN]['heatmiser'].set_value('run_mode','Heating mode (normal mode)')
            self.hass.data[DOMAIN]['heatmiser_info']['run_mode'] = 'Heating mode (normal mode)'
        else:
            self.hass.data[DOMAIN]['heatmiser'].set_value('run_mode','Frost protection mode')
            self.hass.data[DOMAIN]['heatmiser_info']['run_mode'] = 'Frost protection mode'
        self.hass.data[DOMAIN]['heatmiser'].disconnect()

    def update(self) -> None:
        if (self.hass.data[DOMAIN]['heatmiser_info']['run_mode'] == 'Frost protection mode'):
            self._state = 1
        else:
            self._state = 0
"""

"""
# Disabled as this appears to be a read only parameter
class prog_mode_Switch(SwitchEntity):
    def __init__(self) -> None:
        self._state = None

    @property
    def name(self) -> str:
        return self.hass.data[DOMAIN]['name'] + '_prog_mode'

    @property
    def icon(self) -> str | None:
        return 'mdi:calendar-month'

    @property
    def is_on(self) -> bool | None:
        return self._state

    def turn_on(self, **kwargs) -> None: 
        self.hass.data[DOMAIN]['heatmiser'].connect()
        self.hass.data[DOMAIN]['heatmiser'].set_value('program_mode','7 day mode')
        self.hass.data[DOMAIN]['heatmiser'].disconnect()
        self.hass.data[DOMAIN]['heatmiser_info']['program_mode'] = '7 day mode'

    def turn_off(self, **kwargs) -> None: 
        self.hass.data[DOMAIN]['heatmiser'].connect()
        self.hass.data[DOMAIN]['heatmiser'].set_value('program_mode','2/5 mode')
        self.hass.data[DOMAIN]['heatmiser'].disconnect()
        self.hass.data[DOMAIN]['heatmiser_info']['program_mode'] = '2/5 mode'

    def toggle(self, **kwargs) -> None: 
        self.hass.data[DOMAIN]['heatmiser'].connect()
        if self.hass.data[DOMAIN]['heatmiser_info']['program_mode'] == '2/5 mode':
            self.hass.data[DOMAIN]['heatmiser'].set_value('program_mode','7 day mode')
            self.hass.data[DOMAIN]['heatmiser_info']['program_mode'] = '7 day mode'
        else:
            self.hass.data[DOMAIN]['heatmiser'].set_value('program_mode','2/5 mode')
            self.hass.data[DOMAIN]['heatmiser_info']['program_mode'] = '2/5 mode'
        self.hass.data[DOMAIN]['heatmiser'].disconnect()

    def update(self) -> None:
        if (self.hass.data[DOMAIN]['heatmiser_info']['program_mode'] == '7 day mode'):
            self._state = 1
        else:
            self._state = 0
"""

"""
# Disabled as this is managed by Climate entity
class away_mode_Switch(SwitchEntity):
    def __init__(self) -> None:
        self._state = None

    @property
    def name(self) -> str:
        return self.hass.data[DOMAIN]['name'] + '_away_mode'

    @property
    def icon(self) -> str | None:
        return 'mdi:beach'

    @property
    def is_on(self) -> bool | None:
        return self._state

    def turn_on(self, **kwargs) -> None: 
        self.hass.data[DOMAIN]['heatmiser'].connect()
        self.hass.data[DOMAIN]['heatmiser'].set_value('away_mode','On')
        self.hass.data[DOMAIN]['heatmiser'].disconnect()
        self.hass.data[DOMAIN]['heatmiser_info']['away_mode'] = 'On'

    def turn_off(self, **kwargs) -> None: 
        self.hass.data[DOMAIN]['heatmiser'].connect()
        self.hass.data[DOMAIN]['heatmiser'].set_value('away_mode','Off')
        self.hass.data[DOMAIN]['heatmiser'].disconnect()
        self.hass.data[DOMAIN]['heatmiser_info']['away_mode'] = 'Off'

    def toggle(self, **kwargs) -> None: 
        self.hass.data[DOMAIN]['heatmiser'].connect()
        if self.hass.data[DOMAIN]['heatmiser_info']['away_mode'] == 'On':
            self.hass.data[DOMAIN]['heatmiser'].set_value('away_mode','Off')
            self.hass.data[DOMAIN]['heatmiser_info']['away_mode'] = 'Off'
        else:
            self.hass.data[DOMAIN]['heatmiser'].set_value('away_mode','On')
            self.hass.data[DOMAIN]['heatmiser_info']['away_mode'] = 'On'
        self.hass.data[DOMAIN]['heatmiser'].disconnect()

    def update(self) -> None:
        if (self.hass.data[DOMAIN]['heatmiser_info']['away_mode'] == 'On'):
            self._state = 1
        else:
            self._state = 0
"""

