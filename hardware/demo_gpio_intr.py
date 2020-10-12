from board import board_info

from fpioa_manager import fm
fm.register(board_info.BOOT_KEY, fm.fpioa.GPIOHS0, force=True)

from Maix import GPIO

def test_irq(pin_num):
    print("key", pin_num)

key=GPIO(GPIO.GPIOHS0, GPIO.IN, GPIO.PULL_NONE)
key.irq(test_irq, GPIO.IRQ_BOTH, GPIO.WAKEUP_NOT_SUPPORT, 7)

import time
for i in range(20):
    #print('key.value(): ', key.value())
    time.sleep_ms(500)

key.disirq()
fm.unregister(board_info.BOOT_KEY)

