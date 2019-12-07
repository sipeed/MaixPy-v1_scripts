import touchscreen as ts
from machine import I2C
import lcd, image
from board import board_info
from fpioa_manager import fm
from Maix import GPIO

fm.register(board_info.BOOT_KEY, fm.fpioa.GPIO1, force=True)
btn_clear = GPIO(GPIO.GPIO1, GPIO.IN)

lcd.init()
i2c = I2C(I2C.I2C0, freq=400000, scl=30, sda=31)
ts.init(i2c)
#ts.calibrate()
lcd.clear()
img = image.Image()
status_last = ts.STATUS_IDLE
x_last = 0
y_last = 0
draw = False
while True:
    (status,x,y) = ts.read()
    print(status, x, y)
    if draw:
        img.draw_line((x_last, y_last, x, y))
    if status_last!=status:
        if (status==ts.STATUS_PRESS or status == ts.STATUS_MOVE):
            draw = True
        else:
            draw = False
        status_last = status
    lcd.display(img)
    x_last = x
    y_last = y
    if btn_clear.value() == 0:
        img.clear()


