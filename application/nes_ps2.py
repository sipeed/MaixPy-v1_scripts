import nes, lcd
from fpioa_manager import *

# AUDIO_PA_EN_PIN = None  # Bit Dock and old MaixGo
AUDIO_PA_EN_PIN = 32      # Maix Go(version 2.20)
# AUDIO_PA_EN_PIN = 2     # Maixduino

# open audio PA
if AUDIO_PA_EN_PIN:
    fm.register(AUDIO_PA_EN_PIN, fm.fpioa.GPIO1)
    wifi_en=GPIO(GPIO.GPIO1, GPIO.OUT)
    wifi_en.value(1)


fm.register(19, fm.fpioa.GPIOHS0)
fm.register(18, fm.fpioa.GPIOHS1)
fm.register(21, fm.fpioa.GPIOHS2)
fm.register(20, fm.fpioa.GPIOHS3)

lcd.init(freq=15000000)
nes.init(1, cs=fm.fpioa.GPIOHS0, clk=fm.fpioa.GPIOHS1, mosi=fm.fpioa.GPIOHS2, miso=fm.fpioa.GPIOHS3)
nes.run("/sd/mario.nes")

