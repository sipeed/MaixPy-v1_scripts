import sensor, lcd

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
sensor.skip_frames()
lcd.init(freq=15000000)

while(True):
    lcd.display(sensor.snapshot())

