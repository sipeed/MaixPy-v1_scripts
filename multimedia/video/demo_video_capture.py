import lcd
import video
import image

lcd.init()
v = video.open("/sd/badapple_320_240_15fps.avi")
print(v)
img = image.Image()
while True:
    status = v.capture(img)
    if status != 0:
        lcd.display(img)
    else:
        print("end")
        break;
v.__del__()