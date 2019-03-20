import lvgl as lv
import lvgl_helper as lv_h
import lcd
import time
from machine import Timer
   
lcd.init()
lv.init()

disp_drv = lv.disp_drv_t()
lv.disp_drv_init(disp_drv)
disp_drv.disp_flush = lv_h.flush
disp_drv.disp_fill = lv_h.fill
lv.disp_drv_register(disp_drv)

scr = lv.obj()
btn = lv.btn(scr)
btn.align(lv.scr_act(), lv.ALIGN.CENTER, 0, 0)
label = lv.label(btn)
label.set_text("Button")
lv.scr_load(scr)

def on_timer(timer):
	lv.tick_inc(5)
	
timer = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PERIODIC, period=5, unit=Timer.UNIT_MS, callback=on_timer, arg=None)

while True:
	tim = time.ticks_ms()
	lv.task_handler()
	while time.ticks_ms()-tim < 0.005:
		pass

