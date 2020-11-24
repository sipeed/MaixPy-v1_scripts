# This file is part of MaixPY
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

# Uasge see readme.md
from network_esp32 import wifi

SSID = "Sipeed_2.4G"
PASW = "XXXXXXXX"

if wifi.isconnected() == False:
    for i in range(5):
        try:
            wifi.reset()
            print('try AT connect wifi...')
            wifi.connect(SSID, PASW)
            if wifi.isconnected():
                break
        except Exception as e:
            print(e)
print('network state:', wifi.isconnected(), wifi.ifconfig())

print("ping baidu.com:", wifi.nic.ping("baidu.com"), "ms")
wifi.nic.disconnect()

'''
    ESP32_SPI firmware version: 1.4.0
    try AT connect wifi...
    network state: True ('192.168.0.180', '255.255.255.0', '192.168.0.1')
    ping baidu.com: 40 ms
    >
    MicroPython v0.5.1-136-g039f72b6c-dirty on 2020-11-18; Sipeed_M1 with kendryte-k210
    Type "help()" for more information.
    >>>
'''
