"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)

from homeassistant.const import (
    EntityCategory,
    UnitOfTemperature,
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
    add_entities([programSensor(),air_temp_sensor(),date_time_sensor()])


class programSensor(SensorEntity):
    def __init__(self) -> None:
        self._state = None
        self._attributes = []

    @property
    def name(self) -> str:
        return self.hass.data[DOMAIN]['name'] + '_program_mode'

    @property
    def icon(self) -> str | None:
        return 'mdi:calendar-clock'

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    def update(self) -> None:
        mon_t_str = ""
        tue_t_str = ""
        wed_t_str = ""
        thu_t_str = ""
        fri_t_str = ""
        sat_t_str = ""
        sun_t_str = ""
        we_t_str = ""
        wd_t_str = ""
        monhw_t_str = ""
        tuehw_t_str = ""
        wedhw_t_str = ""
        thuhw_t_str = ""
        frihw_t_str = ""
        sathw_t_str = ""
        sunhw_t_str = ""
        wehw_t_str = ""
        wdhw_t_str = ""

        if self.hass.data[DOMAIN]['heatmiser_info']['program_mode'] == '7 day mode':
            self._state = 1

            mon_t_dict = (self.hass.data[DOMAIN]['heatmiser_info']['mon_triggers'])
            tue_t_dict = (self.hass.data[DOMAIN]['heatmiser_info']['tue_triggers'])
            wed_t_dict = (self.hass.data[DOMAIN]['heatmiser_info']['wed_triggers'])
            thu_t_dict = (self.hass.data[DOMAIN]['heatmiser_info']['thu_triggers'])
            fri_t_dict = (self.hass.data[DOMAIN]['heatmiser_info']['fri_triggers'])
            sat_t_dict = (self.hass.data[DOMAIN]['heatmiser_info']['sat_triggers'])
            sun_t_dict = (self.hass.data[DOMAIN]['heatmiser_info']['sun_triggers'])

            for y in range(0,4):
                for x in range(0,3):
                    mon_t_str = mon_t_str + str((list(((list(mon_t_dict.items())[y])[1]).items())[x])[1]) + "," 
                    tue_t_str = tue_t_str + str((list(((list(tue_t_dict.items())[y])[1]).items())[x])[1]) + "," 
                    wed_t_str = wed_t_str + str((list(((list(wed_t_dict.items())[y])[1]).items())[x])[1]) + "," 
                    thu_t_str = thu_t_str + str((list(((list(thu_t_dict.items())[y])[1]).items())[x])[1]) + "," 
                    fri_t_str = fri_t_str + str((list(((list(fri_t_dict.items())[y])[1]).items())[x])[1]) + "," 
                    sat_t_str = sat_t_str + str((list(((list(sat_t_dict.items())[y])[1]).items())[x])[1]) + "," 
                    sun_t_str = sun_t_str + str((list(((list(sun_t_dict.items())[y])[1]).items())[x])[1]) + "," 

            we_t_str = [0,0,0,0,0,0,0,0,0,0,0,0,]
            wd_t_str = [0,0,0,0,0,0,0,0,0,0,0,0,]

            monhw_t_dict = (self.hass.data[DOMAIN]['heatmiser_info']['mon_hw_triggers'])
            tuehw_t_dict = (self.hass.data[DOMAIN]['heatmiser_info']['tue_hw_triggers'])
            wedhw_t_dict = (self.hass.data[DOMAIN]['heatmiser_info']['wed_hw_triggers'])
            thuhw_t_dict = (self.hass.data[DOMAIN]['heatmiser_info']['thu_hw_triggers'])
            frihw_t_dict = (self.hass.data[DOMAIN]['heatmiser_info']['fri_hw_triggers'])
            sathw_t_dict = (self.hass.data[DOMAIN]['heatmiser_info']['sat_hw_triggers'])
            sunhw_t_dict = (self.hass.data[DOMAIN]['heatmiser_info']['sun_hw_triggers'])

            for y in range(0,4):
                for x in range(0,4):
                    monhw_t_str = monhw_t_str + str((list(((list(monhw_t_dict.items())[y])[1]).items())[x])[1]) + "," 
                    tuehw_t_str = tuehw_t_str + str((list(((list(tuehw_t_dict.items())[y])[1]).items())[x])[1]) + "," 
                    wedhw_t_str = wedhw_t_str + str((list(((list(wedhw_t_dict.items())[y])[1]).items())[x])[1]) + "," 
                    thuhw_t_str = thuhw_t_str + str((list(((list(thuhw_t_dict.items())[y])[1]).items())[x])[1]) + "," 
                    frihw_t_str = frihw_t_str + str((list(((list(frihw_t_dict.items())[y])[1]).items())[x])[1]) + "," 
                    sathw_t_str = sathw_t_str + str((list(((list(sathw_t_dict.items())[y])[1]).items())[x])[1]) + "," 
                    sunhw_t_str = sunhw_t_str + str((list(((list(sunhw_t_dict.items())[y])[1]).items())[x])[1]) + "," 

            wehw_t_str = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
            wdhw_t_str = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]

        else:
            self._state = 0
        
            we_t_dict = (self.hass.data[DOMAIN]['heatmiser_info']['weekend_triggers'])
            wd_t_dict = (self.hass.data[DOMAIN]['heatmiser_info']['weekday_triggers'])

            for y in range(0,4):
              for x in range(0,3):
                we_t_str = we_t_str + str((list(((list(we_t_dict.items())[y])[1]).items())[x])[1]) + "," 
                wd_t_str = wd_t_str + str((list(((list(wd_t_dict.items())[y])[1]).items())[x])[1]) + "," 

            mon_t_str = [0,0,0,0,0,0,0,0,0,0,0,0,]
            tue_t_str = [0,0,0,0,0,0,0,0,0,0,0,0,]
            wed_t_str = [0,0,0,0,0,0,0,0,0,0,0,0,]
            thu_t_str = [0,0,0,0,0,0,0,0,0,0,0,0,]
            fri_t_str = [0,0,0,0,0,0,0,0,0,0,0,0,]
            sat_t_str = [0,0,0,0,0,0,0,0,0,0,0,0,]
            sun_t_str = [0,0,0,0,0,0,0,0,0,0,0,0,]

            wehw_t_dict = (self.hass.data[DOMAIN]['heatmiser_info']['weekend_hw_triggers'])
            wdhw_t_dict = (self.hass.data[DOMAIN]['heatmiser_info']['weekday_hw_triggers'])

            for y in range(0,4):
                for x in range(0,4):
                    wehw_t_str = wehw_t_str + str((list(((list(wehw_t_dict.items())[y])[1]).items())[x])[1]) + "," 
                    wdhw_t_str = wdhw_t_str + str((list(((list(wdhw_t_dict.items())[y])[1]).items())[x])[1]) + "," 

            monhw_t_str = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
            tuehw_t_str = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
            wedhw_t_str = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
            thuhw_t_str = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
            frihw_t_str = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
            sathw_t_str = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
            sunhw_t_str = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]

        self._attributes = {
            'weekend_triggers': we_t_str,
            'weekday_triggers': wd_t_str,
            'mon_triggers': mon_t_str,
            'tue_triggers': tue_t_str,
            'wed_triggers': wed_t_str,
            'thu_triggers': thu_t_str,
            'fri_triggers': fri_t_str,
            'sat_triggers': sat_t_str,
            'sun_triggers': sun_t_str,
            'weekend_hw_triggers': wehw_t_str,
            'weekday_hw_triggers': wdhw_t_str,
            'mon_hw_triggers': monhw_t_str,
            'tue_hw_triggers': tuehw_t_str,
            'wed_hw_triggers': wedhw_t_str,
            'thu_hw_triggers': thuhw_t_str,
            'fri_hw_triggers': frihw_t_str,
            'sat_hw_triggers': sathw_t_str,
            'sun_hw_triggers': sunhw_t_str
        }

class air_temp_sensor(SensorEntity):
    def __init__(self) -> None:
        self._state = None
        self._attributes = []

    @property
    def name(self) -> str:
        return self.hass.data[DOMAIN]['name'] + '_air_temp'

    @property
    def device_class(self) -> str:
        return SensorDeviceClass.TEMPERATURE

    @property
    def suggested_unit_of_measurement(self) -> str:
        return UnitOfTemperature.CELSIUS

    @property
    def icon(self) -> str | None:
        return 'mdi:thermometer'

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    def update(self) -> None:
        self._state = self.hass.data[DOMAIN]['heatmiser_info']['air_temp']

        self._attributes = {
            'model': (self.hass.data[DOMAIN]['heatmiser_info']['model']),
            'heating_status': (self.hass.data[DOMAIN]['heatmiser_info']['heating_is_currently_on']),
            'room_temp_setpoint': self.hass.data[DOMAIN]['heatmiser_info']['set_room_temp'],
            'frost_protect_setpoint': self.hass.data[DOMAIN]['heatmiser_info']['frost_protect_temperature'],
            'frost_protect_mode': 1 if (self.hass.data[DOMAIN]['heatmiser_info']['run_mode'] == 'Frost protection mode') else 0,
            'away_mode': 1 if (self.hass.data[DOMAIN]['heatmiser_info']['away_mode'] == 'On') else 0,
            'hot_water_state': 1 if (self.hass.data[DOMAIN]['heatmiser_info']['hot_water_state'] == 'On') else 0
        }

class date_time_sensor(SensorEntity):
    def __init__(self) -> None:
        self._state = None

    @property
    def name(self) -> str:
        return self.hass.data[DOMAIN]['name'] + '_date_time'

    @property
    def icon(self) -> str | None:
        return 'mdi:clock-digital'

    @property
    def state(self):
        return self._state

    def update(self) -> None:
        self._state = self.hass.data[DOMAIN]['heatmiser_info']['date_time']

