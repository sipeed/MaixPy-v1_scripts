import time
from machine import SPI
from fpioa_manager import fm

fm.register(25,fm.fpioa.GPIOHS10, force=True)#cs

from Maix import GPIO

cs = GPIO(GPIO.GPIOHS10, GPIO.OUT)

fm.register(28,fm.fpioa.SPI1_D0, force=True)#mosi
fm.register(26,fm.fpioa.SPI1_D1, force=True)#miso
fm.register(27,fm.fpioa.SPI1_SCLK, force=True)#sclk
spi1 = SPI(SPI.SPI1, mode=SPI.MODE_MASTER, baudrate=10000000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB)

while True:
  w = b'\xFF'
  r = bytearray(1)
  cs.value(0)
  print(spi1.write_readinto(w, r))
  cs.value(1)
  print(w, r)
  time.sleep(0.1)

'''
from machine import SPI
spi1 = SPI(SPI.SPI1, mode=SPI.MODE_MASTER, baudrate=10000000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=28, mosi=29, miso=30)
w = b'1234'
r = bytearray(4)
spi1.write(w)
spi1.write_readinto(w, r)
spi1.read(5, write=0x00)
spi1.readinto(r, write=0x00)
'''
