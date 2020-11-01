# It is no longer supported, please use the new interface code.
# 现在已经不被支持，请使用新的接口代码。
# 2020年11月1日 我留着是用来做应用示例参考的。
# Untitled - By: Echo - 周一 5月 4 2020

import _thread
import os
import json
import time
import utime
from Maix import I2S, GPIO
from fpioa_manager import fm
import struct
from modules import SpeechRecognizer


def sr_data_save(s, content, keyword_num, model_num, path):
    data = s.get_model_data(keyword_num, model_num)  # 原始数据
    # s.print_model(keyword_num, model_num) # 这里打印大量数据, 会到导致后面打印的内容丢失
    with open(path, 'w') as f:
        f.write(data)


def sr_data_load(s, keyword_num, model_num, frame_num, path):
    # print(path)
    with open(path, 'r') as f:
        data = f.read()
        s.add_voice_model(keyword_num, model_num, frame_num, data)

# -------------------------------------------------------------


# register i2s(i2s0) pin
fm.register(20, fm.fpioa.I2S0_IN_D0, force=True)
fm.register(18, fm.fpioa.I2S0_SCLK, force=True)
fm.register(19, fm.fpioa.I2S0_WS, force=True)

# close WiFi, if use M1W Core module
if True:
    fm.register(8, fm.fpioa.GPIO0, force=True)
    wifi_en = GPIO(GPIO.GPIO0, GPIO.OUT)
    wifi_en.value(0)

sample_rate = 8000
# init i2s(i2s0)
i2s_dev = I2S(I2S.DEVICE_0)

# config i2s according to speechrecognizer
i2s_dev.channel_config(i2s_dev.CHANNEL_0,
                       I2S.RECEIVER,
                       resolution=I2S.RESOLUTION_16_BIT,
                       cycles=I2S.SCLK_CYCLES_32,
                       align_mode=I2S.STANDARD_MODE)
i2s_dev.set_sample_rate(sample_rate)
print("------")
s = SpeechRecognizer(i2s_dev)
print("------")
s.set_threshold(0, 0, 20000)  # 设置所处环境的噪声阈值, 环境噪声越大设置最后一个参数越大即可, 其余参数暂时无效
# -------------------------------------------------------------

#record = False
record = True

#load = False
load = True

save_data = False

if record == True:
    key_word_record = False
    tim2 = time.ticks_ms()

    def pins_irq(pin_num):
        global key_word_record
        global tim2
        if (time.ticks_ms() - tim2) > 800:
            key_word_record = not key_word_record
            tim2 = time.ticks_ms()
    fm.register(16, fm.fpioa.GPIOHS0)
    key_boot = GPIO(GPIO.GPIOHS0, GPIO.IN)
    key_boot.irq(pins_irq, GPIO.IRQ_FALLING, GPIO.WAKEUP_NOT_SUPPORT, 7)
    keyword_num = 3
    model_num = 3
    # Currently supports a maximum of 10 keywords, each recording a maximum of 4 templates
    for i in range(keyword_num):
        # Record three keywords, three times each
        for j in range(model_num):
            print("Press the button to record the {} keyword, the {}".format(i+1, j+1))
            while True:
                if key_word_record == True:
                    break
                else:
                    print('.', end="")
                    utime.sleep_ms(500)
            key_word_record = False
            s.record(i, j)
            print('wait record complete....')
            while (2 != s.get_status()):
                print('.', end='')
                time.sleep_ms(500)

            #print("frme_num ---->" + str(s.get_model_info(i, j)))

            # s.print_model(i, j) # 这里打印大量数据, 会到导致后面打印的内容丢失
            # utime.sleep_ms(2)
            if save_data == True:
                content = str(i) + '_' + str(j)  # 存储模型名称
                print(content)
                file_name = "/sd/sr/" + str(i) + '_' + str(j)+".sr"
                sr_data_save(s, content, i, j, file_name)
    print("record successful!")

if load == True:
    sr_data_load(s, 0, 0, 33, "/sd/sr/0_0.sr")
    sr_data_load(s, 0, 1, 19, "/sd/sr/0_1.sr")
    sr_data_load(s, 0, 2, 69, "/sd/sr/0_2.sr")
    sr_data_load(s, 1, 0, 22, "/sd/sr/1_0.sr")
    sr_data_load(s, 1, 1, 20, "/sd/sr/1_1.sr")
    sr_data_load(s, 1, 2, 20, "/sd/sr/1_2.sr")
    sr_data_load(s, 2, 0, 27, "/sd/sr/2_0.sr")
    sr_data_load(s, 2, 1, 22, "/sd/sr/2_1.sr")
    sr_data_load(s, 2, 2, 29, "/sd/sr/2_2.sr")
    print("load successful!")


def func():
    while 1:
        state = s.get_status()
        print(state)
        time.sleep(1)


# s.get_status()
#   SR_NONE = 0,
#   SR_RECORD_WAIT_SPEACKING = 1,
#   SR_RECORD_SUCCESSFUL = 2,
#   SR_RECOGNIZER_WAIT_SPEACKING = 3,
#   SR_RECOGNIZER_SUCCESSFULL = 4,
#   SR_GET_NOISEING = 5,
# 
_thread.start_new_thread(func, ())

while True:
    # recognize
    s.recognize()
    ret = s.get_result()
    if ret > 0:
        if ret == 1:
            print("ret:{}-{}".format(ret, "red"))
        elif ret == 2:
            print("ret:{}-{}".format(ret, "green"))
        elif ret == 3:
            print("ret:{}-{}".format(ret, "blue"))
    # else:
        # print("--")
