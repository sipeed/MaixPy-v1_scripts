

import network
from Maix import GPIO
from fpioa_manager import fm
from board import board_info

# IO map for ESP32 on Maixduino
fm.register(25,fm.fpioa.GPIOHS10, force=True)#cs
fm.register(8,fm.fpioa.GPIOHS11, force=True)#rst
fm.register(9,fm.fpioa.GPIOHS12, force=True)#rdy
fm.register(28,fm.fpioa.GPIOHS13, force=True)#mosi
fm.register(26,fm.fpioa.GPIOHS14, force=True)#miso
fm.register(27,fm.fpioa.GPIOHS15, force=True)#sclk

nic = network.ESP32_SPI(cs=fm.fpioa.GPIOHS10,rst=fm.fpioa.GPIOHS11,rdy=fm.fpioa.GPIOHS12, mosi=fm.fpioa.GPIOHS13,miso=fm.fpioa.GPIOHS14,sclk=fm.fpioa.GPIOHS15)

enc_str = ["OPEN", "", "WPA PSK", "WPA2 PSK", "WPA/WPA2 PSK"]
aps = nic.scan()
for ap in aps:
    print("SSID:{:^20}, ENC:{:>5} , RSSI:{:^20}".format(ap[0], enc_str[ap[1]], ap[2]) )


