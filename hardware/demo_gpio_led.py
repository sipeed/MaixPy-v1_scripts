
import time
from Maix import GPIO
from fpioa_manager import fm
from board import board_info

# see board/readme.md to config your sipeed's hardware.
print(board_info.LED_R)
print(board_info.LED_G)
print(board_info.LED_B)

fm.register(board_info.LED_R, fm.fpioa.GPIO0, force=True)
fm.register(board_info.LED_G, fm.fpioa.GPIOHS0, force=True)
fm.register(board_info.LED_B, fm.fpioa.GPIO2, force=True)
fm.register(board_info.BOOT_KEY, fm.fpioa.GPIO3, force=True)

led_r = GPIO(GPIO.GPIO0, GPIO.OUT)
led_g = GPIO(GPIO.GPIOHS0, GPIO.OUT)
led_b = GPIO(GPIO.GPIO2, GPIO.OUT)
key_input = GPIO(GPIO.GPIO3, GPIO.IN)

status = 0
for i in range(0, 20):
    led_r.value(status)
    time.sleep_ms(300)
    led_g.value(status)
    time.sleep_ms(300)
    led_b.value(status)
    time.sleep_ms(300)
    status = 0 if (status == 1) else 1
    time.sleep_ms(300)
    print("LED RGB(%d,%d,%d)" % (led_r.value(), led_g.value(), led_b.value()))
    time.sleep_ms(100)
    print("key_input:", key_input.value())

fm.unregister(board_info.LED_R)
fm.unregister(board_info.LED_G)
fm.unregister(board_info.LED_B)
fm.unregister(board_info.BOOT_KEY)
