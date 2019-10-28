
from fpioa_manager import *
from Maix import GPIO
import time
from RGB_LED import RGB_LED


led_num  = 1  # LED number
clk_pin  = 21 # board_info.D[2] # Maixduino D2
data_pin = 22 # board_info.D[3] # Maixduino D3

clk_gpiohs_num = fm.fpioa.GPIOHS0
data_gpiohs_num = fm.fpioa.GPIOHS1

led = RGB_LED(clk_pin, data_pin, led_num, clk_gpiohs_num, data_gpiohs_num)


r = 0
g = 0
b = 0
dir = 0
while True:
    if dir == 0:
        if r < 255:
            r += 1
        elif g < 255:
            g += 1
        elif b < 255:
            b += 1
        else:
            dir = 1
    else:
        if b > 0:
            b -= 1
        elif g > 0:
            g -= 1
        elif r > 0:
            r -= 1
        else:
            dir = 0
        
    for i in range(led_num):
        led.set_RGB(i, r, g, b)
    time.sleep_ms(1)


