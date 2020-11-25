# This file is part of MaixPY
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import time, network
from Maix import GPIO
from machine import UART
from fpioa_manager import fm
from board import board_info

class wifi():

    __is_m1w__ = True
    uart = None
    eb = None
    nic = None

    def init():
        if __class__.__is_m1w__:
            fm.register(0, fm.fpioa.GPIOHS1, force=True)
            M1wPower=GPIO(GPIO.GPIOHS1, GPIO.OUT)
            M1wPower.value(0) # b'\r\n ets Jan  8 2013,rst cause:1, boot mode:(7,6)\r\n\r\nwaiting for host\r\n'

        fm.register(board_info.WIFI_EN, fm.fpioa.GPIOHS0) # board_info.WIFI_EN == IO 8
        __class__.en = GPIO(GPIO.GPIOHS0,GPIO.OUT)

        fm.register(board_info.WIFI_RX,fm.fpioa.UART2_TX) # board_info.WIFI_RX == IO 7
        fm.register(board_info.WIFI_TX,fm.fpioa.UART2_RX) # board_info.WIFI_TX == IO 6
        __class__.uart = UART(UART.UART2, 115200, timeout=1000, read_buf_len=8192)

    def enable(en):
        __class__.en.value(en)

    def _at_cmd(cmd="AT\r\n", resp="OK\r\n", timeout=20):
        __class__.uart.write(cmd) # "AT+GMR\r\n"
        time.sleep_ms(timeout)
        tmp = __class__.uart.read()
        # print(tmp)
        if tmp and tmp.endswith(resp):
            return True
        return False

    def at_cmd(cmd="AT\r\n", timeout=20):
        __class__.uart.write(cmd) # "AT+GMR\r\n"
        time.sleep_ms(timeout)
        tmp = __class__.uart.read()
        return tmp

    def reset(force=False, reply=5):
        if force == False and __class__.isconnected():
            return True
        __class__.init()
        for i in range(reply):
            print('reset...')
            __class__.enable(False)
            time.sleep_ms(50)
            __class__.enable(True)
            time.sleep_ms(500) # at start > 500ms
            if __class__._at_cmd(timeout=500):
                break
        __class__._at_cmd()
        __class__._at_cmd('AT+UART_CUR=921600,8,1,0,0\r\n', "OK\r\n")
        __class__.uart = UART(UART.UART2, 921600, timeout=1000, read_buf_len=10240)
        # important! baudrate too low or read_buf_len too small will loose data
        #print(__class__._at_cmd())
        try:
            __class__.nic = network.ESP8285(__class__.uart)
            time.sleep_ms(500) # wait at ready to connect
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

    # from network_espat import wifi
    SSID = "Sipeed_2.4G"
    PASW = "xxxxxxxx"

    def check_wifi_net(reply=5):
        if wifi.isconnected() != True:
            for i in range(reply):
                try:
                    wifi.reset()
                    print('try AT connect wifi...', wifi._at_cmd())
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
    >>>
    raw REPL; CTRL-B to exit
    >OK
    [Warning] function is used by fm.fpioa.GPIOHS1(pin:17)
    [Warning] function is used by fm.fpioa.GPIOHS0(pin:16)
    reset...
    try AT connect wifi... True
    could not connect to ssid=Sipeed_2.4G

    reset...
    try AT connect wifi... True
    network state: True ('192.168.0.165', '255.255.255.0', '192.168.0.1', '0', '0', 'b0:b9:8a:5b:be:7f', 'Sipeed_2.4G')
    >
    MicroPython v0.5.1-136-g039f72b6c-dirty on 2020-11-18; Sipeed_M1 with kendryte-k210
    Type "help()" for more information.
    >>>
    >>>
    >>>
    raw REPL; CTRL-B to exit
    >OK
    network state: True ('192.168.0.165', '255.255.255.0', '192.168.0.1', '0', '0', 'b0:b9:8a:5b:be:7f', 'Sipeed_2.4G')
    >
'''
