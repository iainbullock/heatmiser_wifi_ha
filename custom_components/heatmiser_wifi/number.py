from __future__ import annotations

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
)

from homeassistant.const import (
    EntityCategory,
    UnitOfTemperature,
    UnitOfTime,
)

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
    add_entities([frost_temp_Number(),time_offset_Number()])


class frost_temp_Number(NumberEntity):
    def __init__(self) -> None:
        self._native_value = None

    @property
    def name(self) -> str:
        return self.hass.data[DOMAIN]['name'] + '_frost_temp'

    @property
    def device_class(self) -> str:
        return NumberDeviceClass.TEMPERATURE

    @property
    def native_unit_of_measurement(self) -> str:
        return UnitOfTemperature.CELSIUS

    @property
    def icon(self) -> str | None:
        return 'mdi:thermometer-alert'

    @property
    def native_max_value(self) -> float:
        return 12

    @property
    def native_min_value(self) -> float:
        return 6

    @property
    def native_step(self) -> float:
        return 1

    @property
    def native_value(self):
        return self._native_value

    def set_native_value(self, value: float) -> None:
        self.hass.data[DOMAIN]['heatmiser'].connect()
        self.hass.data[DOMAIN]['heatmiser'].set_value('frost_protect_temperature',int(value))
        self.hass.data[DOMAIN]['heatmiser'].disconnect()
        self.hass.data[DOMAIN]['heatmiser_info']['frost_protect_temperature'] = int(value)
        
    def update(self) -> None:
        self._native_value = self.hass.data[DOMAIN]['heatmiser_info']['frost_protect_temperature']

class time_offset_Number(NumberEntity):
    def __init__(self) -> None:
        self._native_value = 0

    @property
    def name(self) -> str:
        return self.hass.data[DOMAIN]['name'] + '_time_offset'

    @property
    def native_unit_of_measurement(self) -> str:
        return UnitOfTime.MINUTES

    @property
    def icon(self) -> str | None:
        return 'mdi:timer-plus'

    @property
    def native_max_value(self) -> float:
        return 15

    @property
    def native_min_value(self) -> float:
        return -15

    @property
    def native_step(self) -> float:
        return 1

    @property
    def native_value(self):
        return self._native_value

    def set_native_value(self, value: float) -> None:
        self._native_value = int(value)
        self.hass.data[DOMAIN]['time_offset'] = int(value)
        
    def update(self) -> None:
        return 
