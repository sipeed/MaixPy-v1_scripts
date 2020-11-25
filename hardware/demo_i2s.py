from Maix import GPIO, I2S
import image, lcd, math, audio
from fpioa_manager import fm

sample_rate = 22050
sample_points = 1024

rx = I2S(I2S.DEVICE_0)
rx.channel_config(I2S.CHANNEL_0, rx.RECEIVER, resolution = I2S.RESOLUTION_16_BIT, cycles = I2S.SCLK_CYCLES_32, align_mode = I2S.STANDARD_MODE)
rx.set_sample_rate(sample_rate)

fm.fpioa.set_function(pin=20, func=fm.fpioa.I2S0_IN_D0)
fm.fpioa.set_function(pin=19, func=fm.fpioa.I2S0_WS)
fm.fpioa.set_function(pin=18, func=fm.fpioa.I2S0_SCLK)

tx = I2S(I2S.DEVICE_2)

tx.channel_config(I2S.CHANNEL_1, I2S.TRANSMITTER, resolution = I2S.RESOLUTION_16_BIT, cycles = I2S.SCLK_CYCLES_32, align_mode = I2S.RIGHT_JUSTIFYING_MODE)
tx.set_sample_rate(sample_rate)

fm.fpioa.set_function(pin=34, func=fm.fpioa.I2S2_OUT_D1)
fm.fpioa.set_function(pin=35, func=fm.fpioa.I2S2_SCLK)
fm.fpioa.set_function(pin=33, func=fm.fpioa.I2S2_WS)

while True:
    tx.play(rx.record(sample_points))
