import logging
import struct
import time

from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts
import pwnagotchi.plugins as plugins
import pwnagotchi


class UPS:
    def __init__(self):
        # only import when the module is loaded and enabled
        import smbus
        # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
        self._bus = smbus.SMBus(1)
        self.sample_size = 25
        self.battery_readings = []

    def capacity(self):
        battery_level = 0
        try:
            battery_level = self._bus.read_byte_data(0x57, 0x2a)
        except:
            pass
        return battery_level

    def status(self):
        stat02 = self._bus.read_byte_data(0x57, 0x02)
        stat03 = self._bus.read_byte_data(0x57, 0x03)
        stat04 = self._bus.read_byte_data(0x57, 0x04)
        return stat02, stat03, stat04

    def smoothed_capacity(self):
        if len(self.battery_readings) < self.sample_size:
            self.battery_readings.append(self.capacity())
        else:
            self.battery_readings.pop(0)
            self.battery_readings.append(self.capacity())

        return int(sum(self.battery_readings) / len(self.battery_readings))


class PiSugar3(plugins.Plugin):
    __author__ = 'nullm0ose'
    __version__ = '1.0.0'
    __license__ = 'MIT'
    __description__ = 'A plugin that shows charging status and battery percentage for the PiSugar3'

    def __init__(self):
        self.ups = None
        self.lasttemp = 69
        self.drot = 0  # display rotation
        self.nextDChg = 0  # last time display changed, rotate on updates after 5 seconds

    def on_loaded(self):
        self.ups = UPS()
        logging.info("[pisugar3] plugin loaded.")

    def on_ui_setup(self, ui):
        try:
            ui.add_element('bat', LabeledValue(color=BLACK, label='BAT', value='0%',
                                               position=(ui.width() / 2 + 10, 0),
                                               label_font=fonts.Bold, text_font=fonts.Medium))
        except Exception as err:
            logging.warning("pisugar3 setup err: %s" % repr(err))

    def on_unload(self, ui):
        try:
            with ui._lock:
                ui.remove_element('bat')
        except Exception as err:
            logging.warning("pisugar3 unload err: %s" % repr(err))

    def on_ui_update(self, ui):
        capacity = self.ups.smoothed_capacity()
        status = self.ups.status()

        if status[0] & 0x80:  # Charging or power connected
            ui._state._state['bat'].label = "CHG"
        else:
            ui._state._state['bat'].label = "BAT"

        if capacity <= self.options['shutdown']:
            logging.info('[pisugar3] Empty battery (<= %s%%): shutting down' % self.options['shutdown'])
            ui.update(force=True, new_data={'status': 'Battery exhausted, bye ...'})
            pwnagotchi.shutdown()

        ui.set('bat', "%2i%%" % capacity)
