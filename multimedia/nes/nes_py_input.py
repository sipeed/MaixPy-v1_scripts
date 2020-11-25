from machine import I2C
import nes, lcd
from sound import CubeAudio
import sys, time
from fpioa_manager import fm
from Maix import FPIOA, GPIO

from machine import I2C
#i2c = I2C(I2C.I2C1, freq=100*1000, sda=31, scl=30) # cube
i2c = I2C(I2C.I2C3, freq=100*1000, sda=27, scl=24) # amigo
CubeAudio.init(i2c)
tmp = CubeAudio.check()
print(tmp)

CubeAudio.ready(volume=100)

# amigo
fm.fpioa.set_function(13,fm.fpioa.I2S0_MCLK)
fm.fpioa.set_function(21,fm.fpioa.I2S0_SCLK)
fm.fpioa.set_function(18,fm.fpioa.I2S0_WS)
fm.fpioa.set_function(35,fm.fpioa.I2S0_IN_D0)
fm.fpioa.set_function(34,fm.fpioa.I2S0_OUT_D2)

# cube 
#fm.fpioa.set_function(19,fm.fpioa.I2S0_MCLK)
#fm.fpioa.set_function(35,fm.fpioa.I2S0_SCLK)
#fm.fpioa.set_function(33,fm.fpioa.I2S0_WS)
#fm.fpioa.set_function(34,fm.fpioa.I2S0_IN_D0)
#fm.fpioa.set_function(18,fm.fpioa.I2S0_OUT_D2)

CubeAudio.i2s.set_sample_rate(44100)

i2c = I2C(I2C.I2C0, freq=400*1000, sda=27, scl=24)

lcd.init(freq=15000000)
lcd.register(0x36, 0x20) # amigo
# lcd.register(0x36, 0x68) # cube

# B A SEL START UP DOWN LEFT RIGHT
# 1 2 4   8     16  32   64   128
state = 0

try:
  nes.init(nes.INPUT)
  nes.load("mario.nes")
  for i in range(20000):
    nes.loop()
  for i in range(500):
    nes.loop()
    nes.input(8, 0, 0)
    nes.loop()
    nes.input(0, 0, 0)
    nes.loop()
  while True:
    # tmp = i2c.readfrom(66, 1) # handle i2c addr
    # tmp = i2c.readfrom(74, 1) # handle i2c addr
    # nes.input(tmp[0], 0, 0)
    # for i in range(100):
    #   nes.loop()
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
