import sensor
import image
import lcd
import time

clock = time.clock()
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(1)
sensor.run(1)
sensor.skip_frames(30)
while True:
    clock.tick()
    img = sensor.snapshot()
    res = img.find_qrcodes()
    fps =clock.fps()
    if len(res) > 0:
        img.draw_string(2,2, res[0].payload(), color=(0,128,0), scale=2)
        print(res[0].payload())
    lcd.display(img)

