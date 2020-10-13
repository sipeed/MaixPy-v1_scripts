# simple_camera - By: chris - 周四 8月 6 2020

import sensor, image, time, lcd
from fpioa_manager import fm
from board import board_info
from Maix import GPIO
import time


num = 0
switch_status = 0
fm.register(board_info.BOOT_KEY, fm.fpioa.GPIO1, force=True)
fm.register(board_info.ENTER,fm.fpioa.GPIOHS10,force=True)
key_shot = GPIO(GPIO.GPIOHS10,GPIO.IN)
repl_unlock = GPIO(GPIO.GPIO1, GPIO.IN)
lcd.init(freq=15000000)
sensor.reset()

sensor.set_pixformat(sensor.YUV422)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

while(repl_unlock.value() != 0):
    clock.tick()
    img = sensor.snapshot()
    if key_shot.value() == 0:
        path = "/flash/camera-" + str(num) + ".jpg"
        lcd.draw_string(80,40,"Saved :)",lcd.RED,lcd.WHITE)
        time.sleep(1)
        img.save(path)
        num += 1
    else:
        lcd.display(img)
time.sleep(2)
import lcd

lcd.init()
lcd.draw_string(60, 100, "REPL is unlocked!", lcd.RED, lcd.BLACK)
time.sleep(4)
