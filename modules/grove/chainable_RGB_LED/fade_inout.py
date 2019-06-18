
from fpioa_manager import *
from Maix import GPIO
import time
from RGB_LED import RGB_LED


led_num  = 5  # LED number
clk_pin  = 21 # borad_info.D[2] # Maixduino D2
data_pin = 22 # borad_info.D[3] # Maixduino D3

clk_gpiohs_num = 0
data_gpiohs_num = 1

led = RGB_LED(clk_pin, data_pin, led_num, clk_gpiohs_num, data_gpiohs_num, force_register_io=True)

r = 0
g = 0
b = 0
power = 0
while True:
    
        
    for i in range(led_num):
        if i%2 == 0:
            r = power
            g = 0
            b = 0
        else:
            r = 0
            g = 255 - power
            b = 0
        led.set_RGB(i, r, g, b)
    power = (power + 10) & 0xFF
    time.sleep_ms(10)

