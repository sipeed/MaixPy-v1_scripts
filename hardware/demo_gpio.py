import utime
from Maix import GPIO
from board import board_info
from fpioa_manager import *

board_info=board_info()

fm.register(board_info.LED_R, fm.fpioa.GPIO0)
fm.register(board_info.LED_G, fm.fpioa.GPIOHS0)
fm.register(board_info.BOOT_KEY, fm.fpioa.GPIO1)

led_r = GPIO(GPIO.GPIO0, GPIO.OUT)
led_g = GPIO(GPIO.GPIOHS0, GPIO.OUT)
input = GPIO(GPIO.GPIO1, GPIO.IN)

i = 0
status = 0
while i<20:
    led_r.value(status)
    led_g.value(status)
    print("LED :", led_r.value())
    print("-----input:", input.value())
    i+=1
    status = 0 if (status==1) else 1
    utime.sleep_ms(500)

fm.unregister(board_info.LED_R, fm.fpioa.GPIO0)
fm.unregister(board_info.LED_R, fm.fpioa.GPIOHS0)
fm.unregister(board_info.BOOT_KEY, fm.fpioa.GPIO1)

