import lcd, image
from machine import I2C
from modules import htpa

lcd_w = 320
lcd_h = 240

# lcd.init(type=2, freq=20000000)
# lcd.rotation(1)
# lcd.mirror(1)
# dev = htpa(i2c=I2C.I2C0, scl_pin=7, sda_pin=6, i2c_freq=1000000)
lcd.init()
dev = htpa(i2c=I2C.I2C0, scl_pin=10, sda_pin=11, i2c_freq=1000000)
sensor_width = dev.width()
sensor_height = dev.height()
img = image.Image(size=(32,32))
img = img.to_grayscale()
while 1:
    t = time.ticks_ms()
    temperature = dev.temperature()
    max = temperature[0]
    min = max
    max_temp_pos = (0,0)
    for i in range(1,1024):
        v = temperature[i]
        if v < min:
            min = v
        if v > max:
            max = v
            max_temp_pos = (i%sensor_width, i//sensor_height)
    temp_range = max - min + 1
    for i in range(0,1024):
        img[i] = int((temperature[i] - min)/temp_range*255)
    img2 = img.resize(lcd_w, lcd_h)
    img2 = img2.to_rainbow(1)
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
    print(1000/(time.ticks_ms()-t))

