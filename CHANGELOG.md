## Changelog

### v0.1.1 - Feb 2025

   - Fix deprecated features which were removed in HA Core 2025.1 https://developers.home-assistant.io/blog/2023/12/28/support-feature-magic-numbers-deprecation:
      - TEMP_CELSIUS was used from heatmiser_wifi, this is a deprecated constant which will be removed in HA Core 2025.1. Use UnitOfTemperature.CELSIUS instead
      - TEMP_FAHRENHEIT was used from heatmiser_wifi, this is a deprecated constant which will be removed in HA Core 2025.1. Use UnitOfTemperature.FAHRENHEIT instead
      - HVAC_MODE_OFF was used from heatmiser_wifi, this is a deprecated constant which will be removed in HA Core 2025.1. Use HVACMode.OFF instead
      - HVAC_MODE_HEAT was used from heatmiser_wifi, this is a deprecated constant which will be removed in HA Core 2025.1. Use HVACMode.HEAT instead
      - CURRENT_HVAC_OFF was used from heatmiser_wifi, this is a deprecated constant which will be removed in HA Core 2025.1. Use HVACAction.OFF instead
      - CURRENT_HVAC_HEAT was used from heatmiser_wifi, this is a deprecated constant which will be removed in HA Core 2025.1. Use HVACAction.HEATING instead
      - CURRENT_HVAC_IDLE was used from heatmiser_wifi, this is a deprecated constant which will be removed in HA Core 2025.1. Use HVACAction.IDLE instead
      - SUPPORT_TARGET_TEMPERATURE was used from heatmiser_wifi, this is a deprecated constant which will be removed in HA Core 2025.1. Use ClimateEntityFeature.TARGET_TEMPERATURE instead

   - Fix deprecated features which will be removed in HA Core 2025.5:
      - Detected that custom integration 'heatmiser_wifi' accesses hass.helpers.discovery, which should be updated to import functions used from discovery directly at custom_components/heatmiser_wifi/__init__.py, line 55: hass.helpers.discovery.load_platform('climate', DOMAIN, {}, config)

   - Fix other errors / warnings in the logs:
      - Error adding entity sensor.prt_hw_air_temp for domain sensor with platform heatmiser_wifi


### v0.1.0 - May 2024
 - First release of my forked version from the original (https://github.com/midstar/heatmiser_wifi_ha)
