# Heatmiser WiFi Home Assistant Component

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

This repository is forked from the original (https://github.com/midstar/heatmiser_wifi_ha) and updated for my personal requirements only. Feel free to use it as is or clone 
and take over the responsibility for public maintenance.

## Overview
A [Heatmiser](http://www.heatmiser.com/) WiFi Thermostat Home Assistant plugin.

Original version supports:
* Read current air temperature
* Read/set temperature setting (i.e. wanted temperature)
* Read/set on/off of the Thermostat

Original version supported Heatmiser Thermostats are WiFi versions of DT, DT-E, PRT and PRT-E. 

This fork adds support for the PRT-HW WiFi thermostat, and extends the following functionality (for PRT-HW, maybe others):
* TBA 
* TBA

Note that non-WiFi thermostat versions (i.e. using RS-485 serial bus) 
connected through an Heatmiser Ethernet HUB are supported by the
[Home Assistant Heatmiser Core component](https://www.home-assistant.io/integrations/heatmiser/)

## Installation
Install through [HACS](https://hacs.xyz/).

Alternatively copy the heatmiser_wifi directory and its contents to the 
Home Assistant custom_components directory.

## Configuration
Add following configuration to Home Assistant configuration.yaml

    climate:
    - platform: heatmiser_wifi
        host:          <mandatory - hostname or ip address>
        port:          <optional  - default 8068>
        pin:           <optional  - default 0>
        friendly_name: <optional  - default 'Heatmiser MODELNO'>
  
## See also
* [Heatmiser Wifi](https://github.com/midstar/heatmiser_wifi) the library used for communication with Heatmiser WiFi. No longer maintained. This project is forked from here. 
* [daveNewcastle/Heatmiser-WIFI](https://github.com/daveNewcastle/Heatmiser-WIFI) Heatmiser Wifi Home Assistant Component for older versions of Home Assistant. It has not been updated for many years.
* [Home Assistant Heatmiser Core component](https://www.home-assistant.io/integrations/heatmiser/) for non WiFi versions of Heatmister Thermostats.
 
### Author and license
This component is was written by Joel Midstjärna and licensed under the MIT License. This fork is updated by Iain Bullock and licensed under the MIT License.
