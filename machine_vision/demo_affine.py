import image
import lcd, sensor
import time

lcd.init()
# lcd.init(type=2, freq=20000000)

sensor.reset(freq=24000000)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)


matrix = image.get_affine_transform([(0,0), (240, 0), (240, 240)], [(60,60), (240, 0), (220, 200)])
print("matrix:")
print("[{:.02f}, {:.02f}, {:.02f}]".format(matrix[0], matrix[1], matrix[2]))
print("[{:.02f}, {:.02f}, {:.02f}]".format(matrix[3], matrix[4], matrix[5]))
print("[{:.02f}, {:.02f}, {:.02f}]".format(matrix[6], matrix[7], matrix[8]))


try:
    del img
    del img2
except Exception:
    pass

img2 = image.Image(size=(320, 240))
img2.pix_to_ai()
flag = False
while 1:
    img = sensor.snapshot()

    image.warp_affine_ai(img, img2, matrix)

    img2.ai_to_pix()
    if flag:
        lcd.display(img2)
    else:
        lcd.display(img)
    flag = not flag
    time.sleep_ms(500)

