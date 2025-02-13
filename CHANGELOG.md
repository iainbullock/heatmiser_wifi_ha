## Changelog

### v0.1.0 - May 2024
 - First release of my forked version from the original (https://github.com/midstar/heatmiser_wifi_ha)

### v0.1.1 - Feb 2025
 - Fix deprecated features which were removed in HA Core 2025.1:
    - Entity None (<class 'custom_components.heatmiser_wifi.climate.HeatmiserWifi'>) is using deprecated supported features values which will be removed in HA Core 2025.1. Instead it should use <ClimateEntityFeature.TARGET_TEMPERATURE|PRESET_MODE https://developers.home-assistant.io/blog/2023/12/28/support-feature-magic-numbers-deprecation
    - TEMP_CELSIUS was used from heatmiser_wifi, this is a deprecated constant which will be removed in HA Core 2025.1. Use UnitOfTemperature.CELSIUS instead, please report it to the author of the 'heatmiser_wifi' custom integration
    - TEMP_FAHRENHEIT was used from heatmiser_wifi, this is a deprecated constant which will be removed in HA Core 2025.1. Use UnitOfTemperature.FAHRENHEIT instead, please report it to the author of the 'heatmiser_wifi' custom integration
    - HVAC_MODE_OFF was used from heatmiser_wifi, this is a deprecated constant which will be removed in HA Core 2025.1. Use HVACMode.OFF instead, please report it to the author of the 'heatmiser_wifi' custom integration
    - HVAC_MODE_HEAT was used from heatmiser_wifi, this is a deprecated constant which will be removed in HA Core 2025.1. Use HVACMode.HEAT instead, please report it to the author of the 'heatmiser_wifi' custom integration
    - CURRENT_HVAC_OFF was used from heatmiser_wifi, this is a deprecated constant which will be removed in HA Core 2025.1. Use HVACAction.OFF instead, please report it to the author of the 'heatmiser_wifi' custom integration
    - CURRENT_HVAC_HEAT was used from heatmiser_wifi, this is a deprecated constant which will be removed in HA Core 2025.1. Use HVACAction.HEATING instead, please report it to the author of the 'heatmiser_wifi' custom integration
    - CURRENT_HVAC_IDLE was used from heatmiser_wifi, this is a deprecated constant which will be removed in HA Core 2025.1. Use HVACAction.IDLE instead, please report it to the author of the 'heatmiser_wifi' custom integration