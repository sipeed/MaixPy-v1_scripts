import image, lcd, time
import audio
from Maix import GPIO, I2S
from board import board_info
from fpioa_manager import fm

sample_rate = 22050
sample_points = 4096

fm.register(8,  fm.fpioa.GPIO0, force=True)
wifi_en = GPIO(GPIO.GPIO0, GPIO.OUT)
wifi_en.value(0)

fm.register(20,fm.fpioa.I2S0_IN_D0, force=True)
fm.register(30,fm.fpioa.I2S0_WS, force=True)    # 19 on Go Board and Bit(new version)
fm.register(32,fm.fpioa.I2S0_SCLK, force=True)  # 18 on Go Board and Bit(new version)

rx = I2S(I2S.DEVICE_0)
rx.channel_config(rx.CHANNEL_0, rx.RECEIVER, align_mode=I2S.STANDARD_MODE)
rx.set_sample_rate(sample_rate)
print(rx)

# init i2s(i2s0)
wav_dev = I2S(I2S.DEVICE_2)
wav_dev.channel_config(wav_dev.CHANNEL_1, I2S.TRANSMITTER, resolution=I2S.RESOLUTION_16_BIT,
                       cycles=I2S.SCLK_CYCLES_32, align_mode=I2S.RIGHT_JUSTIFYING_MODE)
wav_dev.set_sample_rate(sample_rate)

#import time
# init audio
player = audio.Audio(path="/sd/record.wav", is_create=True, samplerate=22050)

queue = []

for i in range(400):
    tmp = rx.record(sample_points)
    if len(queue) > 0:
        ret = player.record(queue[0])
        queue.pop(0)
    rx.wait_record()
    queue.append(tmp)
    print(str(i) + ":" + str(time.ticks()))

player.finish()
