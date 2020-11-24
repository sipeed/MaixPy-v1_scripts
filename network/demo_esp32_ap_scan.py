# This file is part of MaixPY
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

# Uasge see readme.md
from network_esp32 import wifi

wifi.reset()
enc_str = ["OPEN", "", "WPA PSK", "WPA2 PSK", "WPA/WPA2 PSK", "", "", ""]
aps = wifi.nic.scan()
for ap in aps:
    print("SSID:{:^20}, ENC:{:>5} , RSSI:{:^20}".format(ap[0], enc_str[ap[1]], ap[2]))

'''
    >>>
    raw REPL; CTRL-B to exit
    >OK
    SSID:    Sipeed_2.4G     , ENC:WPA/WPA2 PSK , RSSI:        -57
    SSID:   ChinaNet-Ffdj    , ENC:WPA/WPA2 PSK , RSSI:        -58
    SSID:      wea_615       , ENC:WPA/WPA2 PSK , RSSI:        -67
    SSID:   ChinaNet-PnAN    , ENC:WPA/WPA2 PSK , RSSI:        -70
    SSID:      wea_613       , ENC:WPA/WPA2 PSK , RSSI:        -73
    SSID:   ChinaNet-TnSG    , ENC:WPA/WPA2 PSK , RSSI:        -82
    SSID:  chipshine_GUEST   , ENC:WPA/WPA2 PSK , RSSI:        -83
    SSID:        ASUS        , ENC:WPA/WPA2 PSK , RSSI:        -86
    SSID:       gta888       , ENC:WPA/WPA2 PSK , RSSI:        -87
    SSID:       huahua       , ENC:WPA/WPA2 PSK , RSSI:        -88
    >
    MicroPython v0.5.1-136-g039f72b6c-dirty on 2020-11-18; Sipeed_M1 with kendryte-k210
    Type "help()" for more information.
    >>>
'''
