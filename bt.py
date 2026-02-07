import sys
import time

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_ble.services.standard.hid import HIDService

# Use default HID descriptor
hid = HIDService()
device_info = DeviceInfoService(
   software_revision=adafruit_ble.__version__, manufacturer="Alex"
)
advertisement = ProvideServicesAdvertisement(hid)
advertisement.appearance = 961
scan_response = Advertisement()

ble = adafruit_ble.BLERadio()
if ble.connected:
    for connection in ble.connections:
        connection.disconnect()

print("advertising")
ble.start_advertising(advertisement, scan_response)

k = Keyboard(hid.devices)
kl = KeyboardLayoutUS(k)

def kb_demo():
    while not ble.connected:
        pass
    print("Start typing:")
    while ble.connected:
        c = sys.stdin.read(1)
        sys.stdout.write(c)
        kl.write(c)
        time.sleep(0.1)
    ble.start_advertising(advertisement)

