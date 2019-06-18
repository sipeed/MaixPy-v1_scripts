
from fpioa_manager import *
from modules import ultrasonic
import time


fm.register(board_info.D[6], fm.fpioa.GPIOHS0, force = True)

device = ultrasonic(fm.fpioa.GPIOHS0)

while True:
    distance = device.measure(unit = ultrasonic.UNIT_CM, timeout = 3000000)
    print(distance)
    time.sleep_ms(100)



