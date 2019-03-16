import sensor
import image
import lcd
import time

lcd.init(freq=15000000)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
green_threshold   = (0,   80,  -70,   -10,   -0,   30)
while True:
    img=sensor.snapshot()
    blobs = img.find_blobs([green_threshold])
    if blobs:    
        for b in blobs:
            tmp=img.draw_rectangle(b[0:4]) 
            tmp=img.draw_cross(b[5], b[6]) 
            c=img.get_pixel(b[5], b[6])
    lcd.display(img)
