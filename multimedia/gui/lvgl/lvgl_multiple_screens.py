#this demo shows how to create multiple screens, load and unload them properly without causing memory leak

import lvgl as lv
import lvgl_helper as lv_h
import lcd
import time
from machine import Timer
from machine import I2C
from touch import Touch, TouchLow
import KPU as kpu
import gc

config_touchscreen_support = True
board_m1n = False

lcd.init()


TOUCH = None

def read_cb(drv, ptr):
    data = lv.indev_data_t.cast(ptr)
    TOUCH.event()
    data.point = lv.point_t({'x': TOUCH.points[1][0], 'y': TOUCH.points[1][1]})
    data.state = lv.INDEV_STATE.PR if TOUCH.state == 1 else lv.INDEV_STATE.REL
    return False


if config_touchscreen_support:
    i2c = I2C(I2C.I2C0, freq=1000*1000, scl=24, sda=27)  # 24 27)
    devices = i2c.scan()
    print("devs", devices)  # devs 0 [16, 38, 52, 56]
    TouchLow.config(i2c)
    TOUCH = Touch(480, 320, 200)

lv.init()

disp_buf1 = lv.disp_buf_t()
buf1_1 = bytearray(320*10)
lv.disp_buf_init(disp_buf1,buf1_1, None, len(buf1_1)//4)
disp_drv = lv.disp_drv_t()
lv.disp_drv_init(disp_drv)
disp_drv.buffer = disp_buf1

disp_drv.flush_cb = lv_h.flush
if board_m1n:
    disp_drv.hor_res = 240
    disp_drv.ver_res = 240
else:
    disp_drv.hor_res = 480
    disp_drv.ver_res = 320
lv.disp_drv_register(disp_drv)

if config_touchscreen_support:
    indev_drv = lv.indev_drv_t()
    lv.indev_drv_init(indev_drv)
    indev_drv.type = lv.INDEV_TYPE.POINTER
    indev_drv.read_cb = read_cb
    lv.indev_drv_register(indev_drv)


lv.log_register_print_cb(lambda level,path,line,msg: print('%s(%d): %s' % (path, line, msg)))

class UI:

    def __init__(self):
        self.scr1 = self.create_scr1()
        self.scr2 = self.create_scr2()

    def create_scr1(self):
        scr1 = lv.obj()
        btn1 = lv.btn(scr1)
        btn1.align(scr1, lv.ALIGN.CENTER, 0, 0)
        label1 = lv.label(btn1)
        label1.set_text("Button 1")
        label1.set_size(20,20)
        return scr1

    def create_scr2(self):
        scr2 = lv.obj()
        btn2 = lv.btn(scr2)
        btn2.align(scr2, lv.ALIGN.CENTER, 0, 0)
        label2 = lv.label(btn2)
        label2.set_text("Button 2")
        label2.set_size(20,20)
        return scr2

ui = UI()
kpu.memtest()

def on_timer(timer):
    lv.tick_inc(5)
    lv.task_handler()
    gc.collect()

timer = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PERIODIC, period=5, unit=Timer.UNIT_MS, callback=on_timer, arg=None)

while True:
    tim = time.ticks_ms()
    while time.ticks_ms()-tim < 500:
        pass

    lv.scr_load(ui.scr1)
    kpu.memtest()

    tim = time.ticks_ms()
    while time.ticks_ms()-tim < 500:
        pass

    lv.scr_load(ui.scr2)
    kpu.memtest()
