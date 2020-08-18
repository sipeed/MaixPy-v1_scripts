
import sensor
import image
import lcd
import KPU as kpu

lcd.init()
sensor.reset()
sensor.set_hmirror(1)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
task = kpu.load_flash(0x600000, 1, 0xC000, 60000000)
print("load end")
anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
a = kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)
print("init yolo2 end")
while(True):
    img = sensor.snapshot()
    t = time.ticks_ms()
    code = kpu.run_yolo2(task, img)
    print(time.ticks_ms() - t)
    if code:
        for i in code:
            print(i)
            a = img.draw_rectangle(i.rect())
    lcd.display(img)
a = kpu.deinit(task)


