import lcd, image, sensor
from fpioa_manager import *
from machine import UART
import gc

auto_color = True
max_temp_limit = 300      # max 300
min_temp_limit = 0       # min -40

edge = (-1,-1,-1,-1,8,-1,-1,-1,-1)

offset_x = 0
offset_y = 50
zoom = 1.2
rotate = 0

START_FLAG = 0x5A
sensor_width = 32
sensor_height = 24
lcd_w = 320
lcd_h = 240

fm.register(9, fm.fpioa.UART1_TX)
fm.register(10, fm.fpioa.UART1_RX)

com = UART(UART.UART1, 460800, timeout=1000, read_buf_len=4096)


lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)

clock = time.clock()

find_frame_flag = False
while 1:
    clock.tick()
    if not find_frame_flag:
        data = 0
        flag_count = 0
        while 1:
            if com.any() <= 0:
                continue
            data = com.read(1)
            if int.from_bytes(data, 'little') == START_FLAG:
                flag_count += 1
                if flag_count == 2:
                    find_frame_flag = True
                    break
            else:
                flag_count = 0
    else:
        find_frame_flag = False
        max_temp_pos=None
        data = com.read(2)
        data_len = int.from_bytes(data[:2], "little")
        sum = START_FLAG * 256 + START_FLAG + data_len
        if auto_color:
            min_temp = max_temp_limit
            max_temp = min_temp_limit
        data = com.read(data_len-2)
        target_temp = []
        for i in range(data_len//2-1):
            v = int.from_bytes(data[i*2:i*2+2], 'little')
            sum += v
            v = v/100.0
            if auto_color:
                if v < min_temp:
                    if v < min_temp_limit:
                        min_temp = min_temp_limit
                    else:
                        min_temp = v
                if v > max_temp:
                    if v > max_temp_limit:
                        min_temp = max_temp_limit
                    else:
                        max_temp = v
                    max_temp_pos = (i%sensor_width, i//sensor_width)
            target_temp.append( v )
        data = com.read(2)
        v = int.from_bytes(data, 'little')
        sum += v
        machine_temp = v/100.0
        data = com.read(2)
        parity_sum = int.from_bytes(data, 'little')
        if len(target_temp) != sensor_height*sensor_width:
            print("err")
            continue
        # print("{:02x} {:02x}".format(parity_sum, sum%0xffff))
        # TODO: parity not correct according to the doc
        # if parity_sum != sum%0xffff:
        #     print("parity sum error")
        #     continue
        center_temp = target_temp[int(sensor_width/2 + sensor_height/2*sensor_width)]
        # print("data length:", len(target_temp))
        # print("machine temperature:", machine_temp)
        # print("center temperature:", center_temp)
        img = image.Image(size=(sensor_width, sensor_height))
        img = img.to_grayscale()
        if max_temp == min_temp:
            max_temp += 1
        for i in range(sensor_height):
            for j in range(sensor_width):
                color = (target_temp[i*sensor_width+j]-min_temp)/(max_temp-min_temp)*255
                img[sensor_width*i + j] = int(color)
        img = img.resize(lcd_w, lcd_h)
        del target_temp
        img = img.to_rainbow(1)
        img2 = sensor.snapshot()
        img2.conv3(edge)
        img2 = img2.rotation_corr(z_rotation=rotate, x_translation=offset_x, y_translation=offset_y, zoom=zoom)
        img = img.blend(img2)
        del img2
        img = img.draw_rectangle(lcd_w//2+4, lcd_h//2, 80, 22, color=(0xff,112,0xff), fill=True)
        img = img.draw_string(lcd_w//2+4, lcd_h//2, "%.2f" %(center_temp), color=(0xff,0xff,0xff), scale=2)
        img = img.draw_cross(lcd_w//2, lcd_h//2, color=(0xff,0xff,0xff), thickness=3)
        if max_temp_pos:
            max_temp_pos = (int(lcd_w/sensor_width*max_temp_pos[0]), int(lcd_h/sensor_height*max_temp_pos[1]))
            img = img.draw_rectangle(max_temp_pos[0]+4, max_temp_pos[1], 80, 22, color=(0xff,112,0xff), fill=True)
            img = img.draw_string(max_temp_pos[0]+4, max_temp_pos[1], "%.2f" %(max_temp), color=(0xff,0xff,0xff), scale=2)
            img = img.draw_cross(max_temp_pos[0], max_temp_pos[1], color=(0xff,0xff,0xff), thickness=3)
        fps =clock.fps()
        img = img.draw_string(2,2, ("%2.1ffps" %(fps)), color=(0xff,0xff,0xff), scale=2)
        lcd.display(img)
        img = com.read()
        del img
        gc.collect()
        # gc.mem_free()


