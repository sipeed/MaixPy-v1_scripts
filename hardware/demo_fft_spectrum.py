from Maix import GPIO, I2S, AUDIO, FFT
import image, lcd, math
from board import board_info
from fpioa_manager import fm

sample_rate = 38640
sample_points = 1024
fft_points = 512
hist_x_num = 50


lcd.init(freq=15000000)

# close WiFi
fm.register(8,  fm.fpioa.GPIO0)
wifi_en=GPIO(GPIO.GPIO0,GPIO.OUT)
wifi_en.value(0)

fm.register(20,fm.fpioa.I2S0_IN_D0)
fm.register(30,fm.fpioa.I2S0_WS)    # 19 on Go Board
fm.register(32,fm.fpioa.I2S0_SCLK)  # 18 on Go Board

rx = I2S(I2S.DEVICE_0)
rx.channel_config(rx.CHANNEL_0, rx.RECEIVER, align_mode = I2S.STANDARD_MODE)
rx.set_sample_rate(sample_rate)
img = image.Image()
if hist_x_num > 320:
    hist_x_num = 320
hist_width = int(320 / hist_x_num)#changeable
x_shift = 0
while True:
    audio = rx.record(sample_points)
    fft_res = FFT.run(audio.to_bytes(),fft_points)
    fft_amp = FFT.amplitude(fft_res)
    img = img.clear()
    x_shift = 0
    for i in range(hist_x_num):
        if fft_amp[i] > 240:
            hist_height = 240
        else:
            hist_height = fft_amp[i]
        img = img.draw_rectangle((x_shift,240-hist_height,hist_width,hist_height),[255,255,255],2,True)
        x_shift = x_shift + hist_width
    lcd.display(img)
    fft_amp.clear()

