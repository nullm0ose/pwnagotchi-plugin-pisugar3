# Improved PiSugar 3 Plugin For Pwnagotchi 

The PiSugar 3 Plugin displays the battery percentage as well as the charging status on your Pwnagotchi's UI. 

# Improvements
-This plugin introduces a smoothing mechanism for the battery readings. It calculates a smoothed average based on a sample size of battery readings, resulting in a more stable and accurate battery percentage display.

-The UI has also been simplified, showing only the battery percentage. The voltage as well as the tempature readout have been removed.

-Battery status will automatically change from "BAT" to "CHG", when plugged into a charger.


------------------------------------------------------------------------------------------------------------------------------------------------------------------------

<img width="1439" alt="Screenshot 2023-07-04 at 1 57 00 PM" src="https://github.com/nullm0ose/pwnagotchi-plugin-pisugar3/assets/77137650/e72e1d05-d07c-4d7b-98ed-b259027a99b4">



<img width="1440" alt="Screenshot 2023-07-04 at 1 55 46 PM" src="https://github.com/nullm0ose/pwnagotchi-plugin-pisugar3/assets/77137650/ef2b7b6c-95b6-49c9-ab04-242f31cd499b">

------------------------------------------------------------------------------------------------------------------------------------------------------------------------


## Requirements
- Supports PiSugar 3 Only!
- I2C interface Enabled
- PiSugar Power Manager
- Custom plugins enabled and directory configured 


## PiSugar3 Plugin Installation

To install the PiSugar3 plugin and configure the PiSugar3 UPS module, follow these steps:

## Enable the I2C interface and configure PiSugar3

  Enable the I2C interface by running the following command:
   ```bash
   sudo raspi-config
   ```
   Select "Interfacing Options," then "I2C," and choose "Yes" to enable the I2C interface.

  Detect the I2C bus and devices by running the following commands:
   ```bash
   i2cdetect -y 1
   i2cdump -y 1 0x32
   i2cdump -y 1 0x75
   ```

## Install the PiSugar Power Manager

  Run the following command to install the PiSugar Power Manager:
   ```bash
   curl http://cdn.pisugar.com/release/pisugar-power-manager.sh | sudo bash
   ```

## Create the custom plugins directory

  If the custom plugins directory doesn't already exist, create it by running the following command:
   ```bash
   mkdir /etc/pwnagotchi/custom-plugins
   ```

## Download the plugin

  Navigate to the custom plugins directory:
   ```bash
   cd /etc/pwnagotchi/custom-plugins
   ```

  Clone the PiSugar3 plugin repository:
   ```bash
   git clone https://github.com/nullm0ose/pwnagotchi-plugin-pisugar3.git
   ```

## Copy the plugin file

  Copy the `pisugar3.py` file to the custom plugins directory:
   ```bash
   cp /etc/pwnagotchi/custom-plugins/pwnagotchi-plugin-pisugar3/pisugar3.py /etc/pwnagotchi/custom-plugins
   ```

## Add the plugin configuration

  Add the following lines `config.toml`:
   ```bash
   main.plugins.pisugar3.enabled = true
   main.plugins.pisugar3.shutdown = 5
   ```
   Adjust the `shutdown` value to the desired battery percentage at which the pwnagotchi should shut down.

## Restart your Pwnagotchi

  Restart your Pwnagotchi for the changes to take effect:
   ```bash
   systemctl restart pwnagotchi
   ```
