from machine import I2C
import nes, lcd, sys, time
from sound import CubeAudio # see ../modules/es8374 put sound.py and es8374.py
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

import video
v = video.open("/sd/badapple.avi")
print(v)
v.volume(90)
while True:
    if v.play() == 0:
        print("play end")
        break
