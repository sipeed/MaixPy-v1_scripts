import utime
from Maix import GPIO
from board import board_info
from fpioa_manager import fm

def test_irq(GPIO, pin_num):
    print("key", pin_num)

# register pin to gpiohs0, 
# arg force means force register no matter we have registered before or not
fm.register(board_info.BOOT_KEY, fm.fpioa.GPIOHS0, force=True)
key=GPIO(GPIO.GPIOHS0, GPIO.IN, GPIO.PULL_NONE)
key.irq(test_irq, GPIO.IRQ_BOTH, GPIO.WAKEUP_NOT_SUPPORT, 7)

i = 0
while i<20:
    key.value()
    utime.sleep_ms(500)
    i+=1
key.disirq()
fm.unregister(board_info.BOOT_KEY, fm.fpioa.GPIOHS0)

