import lvgl as lv
import lvgl_helper as lv_h
import lcd
import time
from machine import Timer
from machine import I2C

config_touchscreen_support = True
board_m1n = False
   
i2c = I2C(I2C.I2C0, freq=400000, scl=30, sda=31)
if not board_m1n:
	lcd.init()
else:
	lcd.init(type=2, freq=20000000)
if config_touchscreen_support:
	import touchscreen as ts
	ts.init(i2c)
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
    disp_drv.hor_res = 320
    disp_drv.ver_res = 240
lv.disp_drv_register(disp_drv)

if config_touchscreen_support:
	indev_drv = lv.indev_drv_t()
	lv.indev_drv_init(indev_drv) 
	indev_drv.type = lv.INDEV_TYPE.POINTER
	indev_drv.read_cb = lv_h.read
	lv.indev_drv_register(indev_drv)

# lv.log_register_print_cb(lv_h.log)
lv.log_register_print_cb(lambda level,path,line,msg: print('%s(%d): %s' % (path, line, msg)))

scr = lv.obj()
btn = lv.btn(scr)
btn.align(lv.scr_act(), lv.ALIGN.IN_TOP_LEFT, 0, 0)
label = lv.label(btn)
label.set_text("Button")
label.set_size(20,20)
lv.scr_load(scr)

while True:
	tim = time.ticks_ms()
	lv.tick_inc(5)
	lv.task_handler()
	while time.ticks_ms()-tim < 5:
		pass


