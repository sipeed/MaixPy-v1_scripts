# This file is part of MaixPY
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

# from network_w5k import wlan

SSID = "Sipeed_2.4G"
PASW = "xxxxxxxx"

def enable_esp32():
    from network_esp32 import wifi
    if wifi.isconnected() == False:
        for i in range(5):
            try:
                # Running within 3 seconds of power-up can cause an SD load error
                # wifi.reset(is_hard=False)
                wifi.reset(is_hard=True)
                print('try AT connect wifi...')
                wifi.connect(SSID, PASW)
                if wifi.isconnected():
                    break
            except Exception as e:
                print(e)
    print('network state:', wifi.isconnected(), wifi.ifconfig())

#enable_esp32()

# UDP not support enable_espat

# from network_w5k import wlan

import socket

ADDR = ("192.168.0.107", 60000)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1)

while 1:
    try:
        sock.sendto("hello\n", ADDR)
        data, addr = sock.recvfrom(1024)
    except Exception as e:
        print("receive error:", e)
        continue
    print("addr:", addr, "data:", data)
    time.sleep(2)

sock.close()

'''
>>>
raw REPL; CTRL-B to exit
>OK
network state: True ('192.168.0.186', '255.255.255.0', '192.168.0.1')
addr: ('192.168.0.107', 60000) data: b'HELLO\n'
addr: ('192.168.0.107', 60000) data: b'HELLO\n'
addr: ('192.168.0.107', 60000) data: b'HELLO\n'
'''
