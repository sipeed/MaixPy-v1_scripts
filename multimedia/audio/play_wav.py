from fpioa_manager import *
from Maix import I2S, GPIO
import audio

# disable wifi
fm.register(8, fm.fpioa.GPIO0)
wifi_en=GPIO(GPIO.GPIO0,GPIO.OUT)
wifi_en.value(0)

# register i2s(i2s0) pin
fm.register(34,fm.fpioa.I2S0_OUT_D1)
fm.register(35,fm.fpioa.I2S0_SCLK)
fm.register(33,fm.fpioa.I2S0_WS)

# init i2s(i2s0)
wav_dev = I2S(I2S.DEVICE_0)

# init audio
player = audio.Audio(path = "/sd/6.wav")
player.volume(40)

# read audio info
wav_info = player.play_process(wav_dev)
print("wav file head information: ", wav_info)

# config i2s according to audio info
wav_dev.channel_config(wav_dev.CHANNEL_1, I2S.TRANSMITTER,resolution = I2S.RESOLUTION_16_BIT ,cycles = I2S.SCLK_CYCLES_32, align_mode = I2S.RIGHT_JUSTIFYING_MODE)
wav_dev.set_sample_rate(wav_info[1])

# loop to play audio
while True:
    ret = player.play()
    if ret == None:
        print("format error")
        break
    elif ret==0:
        print("end")
        break
player.finish()

