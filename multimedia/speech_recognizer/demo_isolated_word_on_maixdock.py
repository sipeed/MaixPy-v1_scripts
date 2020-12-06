import time
from Maix import GPIO, I2S
from fpioa_manager import fm
import os, Maix, lcd, image
sample_rate   = 16000
record_time   = 2
img = image.Image(size=(320, 240))
fm.register(20,fm.fpioa.I2S0_IN_D0, force=True)
fm.register(30,fm.fpioa.I2S0_WS, force=True)    # 19 on Go Board and Bit(new version)
fm.register(32,fm.fpioa.I2S0_SCLK, force=True)  # 18 bit
rx = I2S(I2S.DEVICE_0)
rx.channel_config(rx.CHANNEL_0, rx.RECEIVER, align_mode=I2S.STANDARD_MODE)
rx.set_sample_rate(sample_rate)
print(rx)
from speech_recognizer import isolated_word
# model
sr = isolated_word(dmac=2, i2s=I2S.DEVICE_0, size=10)
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
        img.draw_rectangle((0, 0, 320, 240), fill=True, color=(255, 255, 255))
        img.draw_string(10,80, "Please speak A", color=(255, 0, 0), scale=4, mono_space=0)
        lcd.display(img)
sr.set(1, data)
img.draw_rectangle((0, 0, 320, 240), fill=True, color=(255, 255, 255))
img.draw_string(10, 80, "get !", color=(255, 0, 0), scale=4, mono_space=0)
lcd.display(img)
time.sleep_ms(500)

while True:
    time.sleep_ms(100)
    print(sr.state())
    if sr.Done == sr.record(2):
        data = sr.get(2)
        print(data)
        break
    if sr.Speak == sr.state():
        print('speak B')
        img.draw_rectangle((0, 0, 320, 240), fill=True, color=(255, 255, 255))
        img.draw_string(10, 80, "Please speak B", color=(255, 0, 0), scale=4, mono_space=0)
        lcd.display(img)
sr.set(3, data)
img.draw_rectangle((0, 0, 320, 240), fill=True, color=(255, 255, 255))
img.draw_string(10, 80, "get !", color=(255, 0, 0), scale=4, mono_space=0)
lcd.display(img)
time.sleep_ms(500)

while True:
    time.sleep_ms(100)
    print(sr.state())
    if sr.Done == sr.record(4):
        data = sr.get(4)
        print(data)
        break
    if sr.Speak == sr.state():
        print('speak C')
        img.draw_rectangle((0, 0, 320, 240), fill=True, color=(255, 255, 255))
        img.draw_string(10, 80, "Please speak C", color=(255, 0, 0), scale=4, mono_space=0)
        lcd.display(img)
sr.set(5, data)
img.draw_rectangle((0, 0, 320, 240), fill=True, color=(255, 255, 255))
img.draw_string(10, 80, "get !", color=(255, 0, 0), scale=4, mono_space=0)
lcd.display(img)
time.sleep_ms(500)

## recognizer
print('recognizer')
img.draw_rectangle((0, 0, 320, 240), fill=True, color=(255, 255, 255))
img.draw_string(10, 80, "Recognition begin", color=(255, 0, 0), scale=3, mono_space=0)
lcd.display(img)
time.sleep_ms(1000)

while True:
    time.sleep_ms(200)
    img.draw_rectangle((0, 0, 320, 240), fill=True, color=(255, 255, 255))
    img.draw_string(20, 80, "Please speak A or B or C", color=(255, 0, 0), scale=2, mono_space=0)
    lcd.display(img)
    print(sr.state())
    print(sr.dtw(data))
    if sr.Done == sr.recognize():
        res = sr.result()
        if res != None:
            print(str(res[0]))
            if res[0] == 0:
                img.draw_rectangle((0, 0, 320, 240), fill=True, color=(255, 255, 255))
                img.draw_string(150,100, "A", color=(255, 0, 0), scale=10, mono_space=0)
                lcd.display(img)
                time.sleep_ms(200)
            if res[0] == 2:
                img.draw_rectangle((0, 0, 320, 240), fill=True, color=(255, 255, 255))
                img.draw_string(150, 100, "B", color=(255, 0, 0), scale=10, mono_space=0)
                lcd.display(img)
                time.sleep_ms(200)
            if res[0] == 4:
                img.draw_rectangle((0, 0, 320, 240), fill=True, color=(255, 255, 255))
                img.draw_string(150,100,"C", color=(255, 0, 0), scale=10, mono_space=0)
                lcd.display(img)
                time.sleep_ms(200)


