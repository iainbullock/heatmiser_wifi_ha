## Changelog

### v0.1.1 - Feb 2025
 - Fix deprecated features which were removed in HA Core 2025.1 https://developers.home-assistant.io/blog/2023/12/28/support-feature-magic-numbers-deprecation:
    - TEMP_CELSIUS was used from heatmiser_wifi, this is a deprecated constant which will be removed in HA Core 2025.1. Use UnitOfTemperature.CELSIUS instead
    - TEMP_FAHRENHEIT was used from heatmiser_wifi, this is a deprecated constant which will be removed in HA Core 2025.1. Use UnitOfTemperature.FAHRENHEIT instead
    - HVAC_MODE_OFF was used from heatmiser_wifi, this is a deprecated constant which will be removed in HA Core 2025.1. Use HVACMode.OFF instead
    - HVAC_MODE_HEAT was used from heatmiser_wifi, this is a deprecated constant which will be removed in HA Core 2025.1. Use HVACMode.HEAT instead
    - CURRENT_HVAC_OFF was used from heatmiser_wifi, this is a deprecated constant which will be removed in HA Core 2025.1. Use HVACAction.OFF instead,
    - CURRENT_HVAC_HEAT was used from heatmiser_wifi, this is a deprecated constant which will be removed in HA Core 2025.1. Use HVACAction.HEATING instead
    - CURRENT_HVAC_IDLE was used from heatmiser_wifi, this is a deprecated constant which will be removed in HA Core 2025.1. Use HVACAction.IDLE instead
    - SUPPORT_TARGET_TEMPERATURE was used from heatmiser_wifi, this is a deprecated constant which will be removed in HA Core 2025.1. Use ClimateEntityFeature.TARGET_TEMPERATURE instead. Entity None (<class 'custom_components.heatmiser_wifi.climate.HeatmiserWifi'>) is using deprecated supported features values which will be removed in HA Core 2025.1. Instead it should use <ClimateEntityFeature.TARGET_TEMPERATURE|PRESET_MODE https://developers.home-assistant.io/blog/2023/12/28/support-feature-magic-numbers-deprecation

### v0.1.0 - May 2024
 - First release of my forked version from the original (https://github.com/midstar/heatmiser_wifi_ha)
