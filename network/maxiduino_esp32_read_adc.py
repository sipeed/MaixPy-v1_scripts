
import network
import utime
from Maix import GPIO
from fpioa_manager import *

# IO map for ESP32 on Maixduino
fm.register(25,fm.fpioa.GPIOHS10, force=True)#cs
fm.register(8,fm.fpioa.GPIOHS11, force=True)#rst
fm.register(9,fm.fpioa.GPIOHS12, force=True)#rdy
fm.register(28,fm.fpioa.GPIOHS13, force=True)#mosi
fm.register(26,fm.fpioa.GPIOHS14, force=True)#miso
fm.register(27,fm.fpioa.GPIOHS15, force=True)#sclk

nic = network.ESP32_SPI(cs=fm.fpioa.GPIOHS10,rst=fm.fpioa.GPIOHS11,rdy=fm.fpioa.GPIOHS12,
mosi=fm.fpioa.GPIOHS13,miso=fm.fpioa.GPIOHS14,sclk=fm.fpioa.GPIOHS15)

# get ADC0 ADC1 ADC2
adc = nic.adc( (0,1,2) )
print(adc)

while True:
    try:
        # get ADC0~5
        adc = nic.adc()
    except Exception as e:
        print(e)
        continue
    for v in adc:
        print("%04d" %(v), end=" ")
    print()
    utime.sleep_ms(50)
