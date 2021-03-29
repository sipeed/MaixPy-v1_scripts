# This file is part of MaixPY
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import time, network
from Maix import GPIO
from fpioa_manager import fm

class wifi():

    nic = None

    def reset(force=False, reply=5, is_hard=True):
        if force == False and __class__.isconnected():
            return True
        try:
            # IO map for ESP32 on Maixduino
            fm.register(25,fm.fpioa.GPIOHS10)#cs
            fm.register(8,fm.fpioa.GPIOHS11)#rst
            fm.register(9,fm.fpioa.GPIOHS12)#rdy

            if is_hard:
                print("Use Hareware SPI for other maixduino")
                fm.register(28,fm.fpioa.SPI1_D0, force=True)#mosi
                fm.register(26,fm.fpioa.SPI1_D1, force=True)#miso
                fm.register(27,fm.fpioa.SPI1_SCLK, force=True)#sclk
                __class__.nic = network.ESP32_SPI(cs=fm.fpioa.GPIOHS10, rst=fm.fpioa.GPIOHS11, rdy=fm.fpioa.GPIOHS12, spi=1)
                print("ESP32_SPI firmware version:", __class__.nic.version())
            else:
                # Running within 3 seconds of power-up can cause an SD load error
                print("Use Software SPI for other hardware")
                fm.register(28,fm.fpioa.GPIOHS13, force=True)#mosi
                fm.register(26,fm.fpioa.GPIOHS14, force=True)#miso
                fm.register(27,fm.fpioa.GPIOHS15, force=True)#sclk
                __class__.nic = network.ESP32_SPI(cs=fm.fpioa.GPIOHS10,rst=fm.fpioa.GPIOHS11,rdy=fm.fpioa.GPIOHS12, mosi=fm.fpioa.GPIOHS13,miso=fm.fpioa.GPIOHS14,sclk=fm.fpioa.GPIOHS15)
                print("ESP32_SPI firmware version:", __class__.nic.version())

            # time.sleep_ms(500) # wait at ready to connect
        except Exception as e:
            print(e)
            return False
        return True

    def connect(ssid="wifi_name", pasw="pass_word"):
        if __class__.nic != None:
            return __class__.nic.connect(ssid, pasw)

    def ifconfig(): # should check ip != 0.0.0.0
        if __class__.nic != None:
            return __class__.nic.ifconfig()

    def isconnected():
        if __class__.nic != None:
            return __class__.nic.isconnected()
        return False

if __name__ == "__main__":
    # It is recommended to callas a class library (upload network_espat.py)

    # from network_esp32 import wifi
    SSID = "Sipeed_2.4G"
    PASW = "xxxxxxxx"

    def check_wifi_net(reply=5):
        if wifi.isconnected() != True:
            for i in range(reply):
                try:
                    wifi.reset(is_hard=True)
                    print('try esp32spi connect wifi...')
                    wifi.connect(SSID, PASW)
                    if wifi.isconnected():
                        break
                except Exception as e:
                    print(e)
        return wifi.isconnected()

    if wifi.isconnected() == False:
        check_wifi_net()
    print('network state:', wifi.isconnected(), wifi.ifconfig())

    # The network is no longer configured repeatedly
    import socket
    sock = socket.socket()
    # your send or recv
    # see other demo_socket_tcp.py / udp / http / mqtt
    sock.close()

'''ouput
    MicroPython v0.5.1-136-g039f72b6c-dirty on 2020-11-18; Sipeed_M1 with kendryte-k210
    Type "help()" for more information.
    >>>
    >>>
    >>>
    raw REPL; CTRL-B to exit
    >OK
    Use Hareware SPI for other maixduino
    [esp32_spi] use hard spi(1)

    hard spi

    esp32 set hard spi clk:9159090

    Get version fail
    try esp32spi connect wifi...
    Use Hareware SPI for other maixduino
    [Warning] function is used by unknown(pin:10)
    [Warning] function is used by unknown(pin:6)
    [Warning] function is used by unknown(pin:11)
    [esp32_spi] use hard spi(1)

    hard spi

    esp32 set hard spi clk:9159090

    ESP32_SPI firmware version: 1.4.0
    try AT connect wifi...
    network state: True ('192.168.0.180', '255.255.255.0', '192.168.0.1')
    >
    MicroPython v0.5.1-136-g039f72b6c-dirty on 2020-11-18; Sipeed_M1 with kendryte-k210
    Type "help()" for more information.
    >>>
    >>>
    >>>
    raw REPL; CTRL-B to exit
    >OK
    network state: True ('192.168.0.180', '255.255.255.0', '192.168.0.1')
    >
    MicroPython v0.5.1-136-g039f72b6c-dirty on 2020-11-18; Sipeed_M1 with kendryte-k210
    Type "help()" for more information.
    >>>
'''
