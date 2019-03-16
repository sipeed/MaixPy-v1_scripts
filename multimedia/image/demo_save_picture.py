import sensor, lcd, image

print("init")
lcd.init(freq=15000000)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
sensor.skip_frames(40)
print("init ok")

path = "/sd/image.jpg"
img = sensor.snapshot()
print("save image")
img.save(path)

print("read image")
img_read = image.Image(path)
lcd.display(img_read)
print("ok")


