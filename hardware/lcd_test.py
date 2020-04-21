import lcd,image, time


lcd.init(type=1, freq=15000000)
# lcd.init(type=2, freq=20000000)
# lcd.init(type=1, width=320, height=240, invert=True, freq=20000000)

img = image.Image(size=(240,240))

img.draw_rectangle(0,0,30, 240, fill=True, color=(0xff, 0xff, 0xff))
img.draw_rectangle(30,0,30, 240, fill=True, color=(250, 232, 25))
img.draw_rectangle(60,0,30, 240, fill=True, color=(106, 198, 218))
img.draw_rectangle(90,0,30, 240, fill=True, color=(98, 177, 31))
img.draw_rectangle(120,0,30, 240, fill=True, color=(180, 82, 155))
img.draw_rectangle(150,0,30, 240, fill=True, color=(231, 47, 29))
img.draw_rectangle(180,0,30, 240, fill=True, color=(32, 77, 158))
img.draw_rectangle(210,0,30, 240, fill=True, color=(27, 28, 32))

lcd.display(img)

count = 500
while count > 0:
    t = time.ticks_ms()
    lcd.display(img)
    print(time.ticks_ms() - t)
    count -= 1
