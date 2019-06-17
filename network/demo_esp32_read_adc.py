import nes,network
import utime
from Maix import GPIO
from fpioa_manager import *

#iomap at MaixDuino
fm.register(25,fm.fpioa.GPIOHS10)#cs
fm.register(8,fm.fpioa.GPIOHS11)#rst
fm.register(9,fm.fpioa.GPIOHS12)#rdy
fm.register(28,fm.fpioa.GPIOHS13)#mosi
fm.register(26,fm.fpioa.GPIOHS14)#miso
fm.register(27,fm.fpioa.GPIOHS15)#sclk

nic = network.ESP32_SPI(cs=fm.fpioa.GPIOHS10,rst=fm.fpioa.GPIOHS11,rdy=fm.fpioa.GPIOHS12,
mosi=fm.fpioa.GPIOHS13,miso=fm.fpioa.GPIOHS14,sclk=fm.fpioa.GPIOHS15)

adc_pin = ["PIN36", "PIN39", "PIN34", "PIN35", "PIN32"]

while True:
    adc = nic.adc()
    for i in range(len(adc)):
        print("%s:%d"%(adc_pin[i],adc[i]))
    utime.sleep_ms(50)
