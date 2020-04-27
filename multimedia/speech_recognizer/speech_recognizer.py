from Maix import I2S, GPIO
from fpioa_manager import fm
from modules import SpeechRecognizer
import utime, time

# register i2s(i2s0) pin
fm.register(20, fm.fpioa.I2S0_OUT_D0, force=True)
fm.register(18, fm.fpioa.I2S0_SCLK, force=True)
fm.register(19, fm.fpioa.I2S0_WS, force=True)

# close WiFi, if use M1W Core module
if True:
    fm.register(8,  fm.fpioa.GPIO0, force=True)
    wifi_en=GPIO(GPIO.GPIO0,GPIO.OUT)
    wifi_en.value(0)

sample_rate = 8000
# init i2s(i2s0)
i2s_dev = I2S(I2S.DEVICE_0)

# config i2s according to speechrecognizer
i2s_dev.channel_config(i2s_dev.CHANNEL_0,
    I2S.RECEIVER,
    resolution = I2S.RESOLUTION_16_BIT,
    cycles = I2S.SCLK_CYCLES_32,
    align_mode = I2S.RIGHT_JUSTIFYING_MODE)
i2s_dev.set_sample_rate(sample_rate)

s = SpeechRecognizer(i2s_dev)
type(s)
print(s)

key_word_record = False
tim2 = time.ticks_ms()

def pins_irq(pin_num):
    global key_word_record
    global tim2
    if (time.ticks_ms() - tim2 )> 800:
        key_word_record = not key_word_record
        tim2 = time.ticks_ms()

fm.register(16, fm.fpioa.GPIOHS0)
key_boot = GPIO(GPIO.GPIOHS0, GPIO.IN)
key_boot.irq(pins_irq, GPIO.IRQ_FALLING, GPIO.WAKEUP_NOT_SUPPORT, 7)

#Currently supports a maximum of 10 keywords, each recording a maximum of 4 templates
for i in range(3):
    # Record three keywords, three times each
    for j in range(3):

        print("Press the button to record the {} keyword, the {}".format(i+1, j+1))
        while True:
            if key_word_record == True:
                break
            else:
                print('.', end="")
                utime.sleep_ms(500)
        print("---")
        s.record(i, j)
        key_word_record = False


print("record successful!")

while True:
    # recognize
    ret = s.recognize()
    if ret > 0:
        if ret == 1:
            print("ret:{}-{}".format(ret, "red"))
        elif ret == 2:
            print("ret:{}-{}".format(ret, "green"))
        elif ret == 3:
            print("ret:{}-{}".format(ret, "blue"))

    else:
        print("")
