import lcd, image, sensor
from machine import I2C
from modules import htpa

lcd_w = 320
lcd_h = 240

edge = (-1,-1,-1,-1,8,-1,-1,-1,-1)

offset_x = 0
offset_y = 50
zoom = 2
rotate = 0

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
lcd.init(type=2, freq=20000000)
lcd.rotation(2)
# lcd.mirror(1)
dev = htpa(i2c=I2C.I2C0, scl_pin=7, sda_pin=6, i2c_freq=1000000)
# lcd.init()
# dev = htpa(i2c=I2C.I2C0, scl_pin=10, sda_pin=11, i2c_freq=1000000)
sensor_width = dev.width()
sensor_height = dev.height()
# img = image.Image(size=(32,32))
# img = img.to_grayscale()
clock = time.clock()
while 1:
    clock.tick()
    temperature = dev.temperature()
    min, max, min_pos, max_pos = dev.min_max()
    temp_range = max - min + 1
    img = dev.to_image(min, max)
    img = img.rotation_corr(z_rotation=90)
    img = img.replace(img, hmirror=True)
    max_temp_pos = (max_pos//sensor_width, max_pos%sensor_width)
    img = img.resize(lcd_w, lcd_h)
    img = img.to_rainbow(1)
    img2 = sensor.snapshot()
    img2.conv3(edge)
    img2 = img2.rotation_corr(z_rotation=rotate, x_translation=offset_x, y_translation=offset_y, zoom=zoom)
    img2 = img.blend(img2)
    del img
    # center
    center_temp = temperature[int(sensor_width/2 + sensor_height/2*sensor_width)]/100.0
    img2 = img2.draw_rectangle(lcd_w//2-36, lcd_h//2, 80, 22, color=(0xff,112,0xff), fill=True)
    img2 = img2.draw_string(lcd_w//2-36, lcd_h//2, "%.2f" %(center_temp), color=(0xff,0xff,0xff), scale=2)
    img2 = img2.draw_cross(lcd_w//2, lcd_h//2, color=(0xff,0xff,0xff), thickness=3)
    # max
    max_temp_pos = (int(lcd_w/sensor_width*max_temp_pos[0]), int(lcd_h/sensor_height*max_temp_pos[1]))
    if max_temp_pos[0] >=  lcd_w/2:
        x = max_temp_pos[0] - 80
    else:
        x = max_temp_pos[0] + 4
    img2 = img2.draw_rectangle(x, max_temp_pos[1], 80, 22, color=(0xff,112,0xff), fill=True)
    img2 = img2.draw_string(x, max_temp_pos[1], "%.2f" %(max/100.0), color=(0xff,0xff,0xff), scale=2)
    img2 = img2.draw_cross(max_temp_pos[0], max_temp_pos[1], color=(0xff,0xff,0xff), thickness=3)
    lcd.display(img2)
    del img2
    print(clock.fps())
