from Maix import GPIO, I2S, FFT
import image
import lcd
import math
import time
import gc
from board import board_info
from fpioa_manager import fm
import audio

sample_rate = 22050
sample_points = 4096

fm.register(8,  fm.fpioa.GPIO0, force=True)
wifi_en = GPIO(GPIO.GPIO0, GPIO.OUT)
wifi_en.value(0)

fm.register(20, fm.fpioa.I2S0_IN_D0, force=True)
# 19 on Go Board and Bit(new version)
fm.register(19, fm.fpioa.I2S0_WS, force=True)
# 18 on Go Board and Bit(new version)
fm.register(18, fm.fpioa.I2S0_SCLK, force=True)

rx = I2S(I2S.DEVICE_0)
rx.channel_config(rx.CHANNEL_0, rx.RECEIVER, align_mode=I2S.STANDARD_MODE)
rx.set_sample_rate(sample_rate)
print(rx)

fm.register(0, fm.fpioa.GPIO1, force=True)
wifi_en = GPIO(GPIO.GPIO1, GPIO.OUT)
wifi_en.value(1)

# register i2s(i2s0) pin
fm.register(33, fm.fpioa.I2S2_OUT_D1, force=True)
fm.register(35, fm.fpioa.I2S2_SCLK, force=True)
fm.register(34, fm.fpioa.I2S2_WS, force=True)

# init i2s(i2s0)
wav_dev = I2S(I2S.DEVICE_2)

wav_dev.channel_config(wav_dev.CHANNEL_1, I2S.TRANSMITTER, resolution=I2S.RESOLUTION_16_BIT,
                       cycles=I2S.SCLK_CYCLES_32, align_mode=I2S.RIGHT_JUSTIFYING_MODE)
wav_dev.set_sample_rate(sample_rate)

# loop to play audio
# while True:
# wav_dev.play(rx.record(sample_points))
# print("running")
# wav_dev.finish()

#import time

# init audio
player = audio.Audio(path="/sd/record_1.wav", is_create=True, samplerate=22050)

queue = []

for i in range(400):
    tmp = rx.record(sample_points)
    if len(queue) > 0:
        ret = player.record(queue[0])
        queue.pop(0)
    rx.wait_record()
    queue.append(tmp)
    # print(time.ticks())

player.finish()
