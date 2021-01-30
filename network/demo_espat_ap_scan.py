# This file is part of MaixPY
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

#from board import board_info
#from Maix import config
#tmp = config.get_value('board_info', None)
#board_info.load(tmp)

from network_espat import wifi
wifi.reset()

print(wifi.at_cmd("AT\r\n"))

ap_info = []

import time
while True:
    time.sleep(1)
    print('ap-scan...')
    try:
        tmp = wifi.at_cmd('AT+CWLAP\r\n')
        #ap_info = wifi.nic.scan()
        if tmp != None and len(tmp) > 64:
            #print(tmp[len('+CWLAP:'):].split(b"\r\n"))
            aps = tmp.replace(b'+CWLAP:', b'').replace(b'\r\n\r\nOK\r\n', b'')
            #print(aps)
            ap_info = aps.split(b"\r\n")
            #print(ap_info)
            break
    except Exception as e:
        print('error', e)

def wifi_deal_ap_info(info):
    res = []
    for ap_str in info:
        ap_str = ap_str.split(b",")
        #print(ap_str)
        info_one = []
        for node in ap_str[1:-1]:
            if node.startswith(b'"'):
                info_one.append(node[1:-1])
            else:
                info_one.append(int(node))
        res.append(info_one)
    return res

#print(ap_info)

ap_info = wifi_deal_ap_info(ap_info)

ap_info.sort(key=lambda x:x[2], reverse=True) # sort by rssi
for ap in ap_info:
    print("SSID:{:^20}, RSSI:{:>5} , MAC:{:^20}".format(ap[0], ap[1], ap[2]) )

'''
MicroPython fa51290 on 2020-12-07; Sipeed_M1 with kendryte-k210
Type "help()" for more information.>>>
>>>
>>>
raw REPL; CTRL-B to exit
>OK
reset...
b'\r\n\r\nOK\r\n'
ap-scan...
ap-scan...
ap-scan...
ap-scan...
SSID:    webduino.io     , RSSI:  -50 , MAC: b6:e4:2f:f9:2f:1f
SSID:    Sipeed_2.4G     , RSSI:  -73 , MAC: b0:b9:8a:5b:be:7f
SSID:   ChinaNet-Ffdj    , RSSI:  -91 , MAC: a4:29:40:cc:51:f4
SSID:      wea_615       , RSSI:  -91 , MAC: 64:6e:97:e1:86:e5
SSID:      OpenWrt       , RSSI:  -88 , MAC: 20:76:93:40:15:9c
>
'''
