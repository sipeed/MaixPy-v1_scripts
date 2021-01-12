# This file is part of MaixPY
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

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

enable_esp32()

def enable_espat():
    from network_espat import wifi
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

#enable_espat()

def network_wiznet5k():
    from network_wiznet5k import lan
    from machine import SPI
    from Maix import GPIO
    if lan.isconnected() == False:
        WIZNET5K_SPI_SCK = 21
        WIZNET5K_SPI_MOSI = 8
        WIZNET5K_SPI_MISO = 15
        WIZNET5K_SPI_CS = 20
        spi1 = SPI(4, mode=SPI.MODE_MASTER, baudrate=600 * 1000,
                    polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=WIZNET5K_SPI_SCK, mosi=WIZNET5K_SPI_MOSI, miso=WIZNET5K_SPI_MISO)
        for i in range(5):
            try:
                lan.reset(spi1, WIZNET5K_SPI_CS)
                print('try connect lan...')
                if lan.isconnected():
                    break
            except Exception as e:
                print(e)
    print('network state:', lan.isconnected(), lan.ifconfig())

# network_wiznet5k()

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


