import sensor
import image
import lcd
import time

clock = time.clock()
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
sensor.skip_frames(30)
while True:
    clock.tick()
    img = sensor.snapshot()
    fps =clock.fps()
    img.draw_string(2,2, ("%2.1ffps" %(fps)), color=(0,128,0), scale=2)
    lcd.display(img)


