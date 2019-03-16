import video, sensor, image, lcd, time

lcd.init(freq=15000000) 
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
sensor.skip_frames(30)
v = video.open("/sd/capture.avi", record=1, interval=200000, quality=50)
i = 0
tim = time.ticks_ms()
while True:
    tim = time.ticks_ms()
    img = sensor.snapshot()
    lcd.display(img)
    img_len = v.record(img)
    # print("record",time.ticks_ms() - tim)
    i += 1
    if i > 100:
        break
print("finish")
v.record_finish()
lcd.clear()

