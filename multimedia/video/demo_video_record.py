import sensor, image, lcd, time

lcd.init(freq=15000000)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)

sensor.set_hmirror(1)
sensor.set_vflip(1)

sensor.run(1)
sensor.skip_frames(30)

import video

v = video.open("/sd/capture.avi", audio = False, record=1, interval=200000, quality=50)

tim = time.ticks_ms()
for i in range(50):
    tim = time.ticks_ms()
    img = sensor.snapshot()
    lcd.display(img)
    img_len = v.record(img)
    # print("record",time.ticks_ms() - tim)

print("record_finish")
v.record_finish()
v.__del__()

# play your record
v = video.open("/sd/capture.avi")
print(v)
v.volume(50)
while True:
    if v.play() == 0:
        print("play end")
        break

print("play finish")
v.__del__()

lcd.clear()

