# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

import time
from Maix import GPIO, I2S
from fpioa_manager import fm

# user setting
sample_rate   = 16000
record_time   = 4  #s

#fm.register(8,  fm.fpioa.GPIO0, force=True)
#wifi_en = GPIO(GPIO.GPIO0, GPIO.OUT)
#wifi_en.value(0)

fm.register(20,fm.fpioa.I2S0_IN_D0, force=True)
fm.register(18,fm.fpioa.I2S0_SCLK, force=True)
fm.register(19,fm.fpioa.I2S0_WS, force=True)

# fm.register(32,fm.fpioa.I2S0_SCLK, force=True)  # dock
# fm.register(30,fm.fpioa.I2S0_WS, force=True)    # dock

rx = I2S(I2S.DEVICE_0)
rx.channel_config(rx.CHANNEL_0, rx.RECEIVER, align_mode=I2S.STANDARD_MODE)
rx.set_sample_rate(sample_rate)
print(rx)

from speech_recognizer import isolated_word

# default: maix dock / maix duino set shift=0
sr = isolated_word(dmac=2, i2s=I2S.DEVICE_0, size=10, shift=0) # maix bit set shift=1
print(sr.size())
print(sr)

## threshold
sr.set_threshold(0, 0, 10000)

## record and get & set

while True:
  time.sleep_ms(100)
  print(sr.state())
  if sr.Done == sr.record(0):
    data = sr.get(0)
    print(data)
    break
  if sr.Speak == sr.state():
    print('speak A')

#sr.set(1, data)

while True:
  time.sleep_ms(100)
  print(sr.state())
  if sr.Done == sr.record(2):
    data = sr.get(2)
    print(data)
    break
  if sr.Speak == sr.state():
    print('speak B')

#sr.set(3, data)

## recognizer
#sr.stop()
#sr.run()

print('recognizer')
while True:
  time.sleep_ms(200)
  #print(sr.state())
  #print(sr.dtw(data))
  if sr.Done == sr.recognize():
    res = sr.result()
    print(res)
