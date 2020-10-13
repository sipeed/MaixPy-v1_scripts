

import network
from Maix import GPIO
from fpioa_manager import fm
from board import board_info
WIFI_SSID = "Sipeed_2.4G"
WIFI_PASSWD = "passwd"

# IO map for ESP32 on Maixduino
fm.register(25,fm.fpioa.GPIOHS10, force=True)#cs
fm.register(8,fm.fpioa.GPIOHS11, force=True)#rst
fm.register(9,fm.fpioa.GPIOHS12, force=True)#rdy
fm.register(28,fm.fpioa.GPIOHS13, force=True)#mosi
fm.register(26,fm.fpioa.GPIOHS14, force=True)#miso
fm.register(27,fm.fpioa.GPIOHS15, force=True)#sclk

nic = network.ESP32_SPI(cs=fm.fpioa.GPIOHS10,rst=fm.fpioa.GPIOHS11,rdy=fm.fpioa.GPIOHS12, mosi=fm.fpioa.GPIOHS13,miso=fm.fpioa.GPIOHS14,sclk=fm.fpioa.GPIOHS15)

nic.connect(WIFI_SSID, WIFI_PASSWD)
print(nic.ifconfig())
print(nic.isconnected())
print("ping baidu.com:", nic.ping("baidu.com"), "ms")
nic.disconnect()




