# This file is part of MaixPY
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

# Uasge see readme.md
# from network_esp8285 import wifi
# from network_w5k import wlan

SSID = "Sipeed_2.4G"
PASW = "Sipeed123."

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

enable_esp32()

def enable_esp8285():
    from network_esp8285 import wifi
    if wifi.isconnected() == False:
        for i in range(5):
            try:
                # Running within 3 seconds of power-up can cause an SD load error
                # wifi.reset(is_hard=False)
                wifi.reset()
                print('try AT connect wifi...')
                wifi.connect(SSID, PASW)
                if wifi.isconnected():
                    break
            except Exception as e:
                print(e)
    print('network state:', wifi.isconnected(), wifi.ifconfig())

#enable_esp8285()

try:
    import usocket as socket
except:
    import socket

TestHttps = False

def main(use_stream=True):
    s = socket.socket()
    s.settimeout(1)
    host = "www.baidu.com"
    if TestHttps:
        ai = socket.getaddrinfo(host, 443)
    else:
        ai = socket.getaddrinfo(host, 80)
    print("Address infos:", ai)
    addr = ai[0][-1]
    for i in range(5):
        try:
            print("Connect address:", addr)
            s.connect(addr)

            if TestHttps: # ssl
                try:
                    import ussl as ssl
                except:
                    import ssl
                tmp = ssl.wrapsocket(s, server_hostname=host)
                tmp.write(b"GET / HTTP/1.1\r\n\r\n")
            else:
                s.write(b"GET / HTTP/1.1\r\n\r\n")
            data = (s.readline('\r\n'))
            print(data)
            with open('test.txt', 'wb') as f:
                f.write(data)

        except Exception as e:
          print(e)

    s.close()

main()


