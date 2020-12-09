from machine import I2C
import nes, lcd
from sound import CubeAudio
import sys, time
from fpioa_manager import fm
from Maix import FPIOA, GPIO

i2c = I2C(I2C.I2C3, freq=500*1000, sda=27, scl=24)
CubeAudio.init(i2c)
tmp = CubeAudio.check()
print(tmp)

CubeAudio.ready(volume=100)

fm.fpioa.set_function(13,fm.fpioa.I2S0_MCLK)
fm.fpioa.set_function(21,fm.fpioa.I2S0_SCLK)
fm.fpioa.set_function(18,fm.fpioa.I2S0_WS)
fm.fpioa.set_function(35,fm.fpioa.I2S0_IN_D0)
fm.fpioa.set_function(34,fm.fpioa.I2S0_OUT_D2)

CubeAudio.i2s.set_sample_rate(44100)

lcd.init(freq=15000000)
lcd.register(0x36, 0x20)

# B A SEL START UP DOWN LEFT RIGHT
# 1 2 4   8     16  32   64   128
state = 0

try:
  nes.init(nes.INPUT)
  nes.load("sd/game/mario.nes")
  for i in range(20000):
    nes.loop()
  for i in range(500):
    nes.loop()
    nes.input(8, 0, 0)
    nes.loop()
    nes.input(0, 0, 0)
  while True:
    tmp = i2c.readfrom(66, 1)
    for i in range(10):
      nes.loop()
    nes.input(tmp[0], 0, 0)
    for i in range(10):
      nes.loop()
finally:
  nes.free()

#import time
#i = 0
#while True:
    ##dev = i2c.scan()
    ##print(dev)
    ##time.sleep(0.5)
    #try:
        ##i2c.writeto(66, b'0')
        #tmp = (i2c.readfrom(66, 1))
        #print('{:08b}'.format(tmp[0]))
    #except Exception as e:
        #print(e)
