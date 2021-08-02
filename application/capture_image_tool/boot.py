'''
    image caupture tool, capture images to SD card with directory switch support
    @usage 1. Change camera and lcd configs according to your hardware like `lcd.rotation`
           2. Prepare a SD card with SPI mode support, and format to FAT32 with MBR(msdos) partition
           3. Copy this boot.py to your SD card root directory
           4. Power off board, then insert SD card to board
           5. Power on, it will automatically create a directory like `cap_images_1`,
                the next time will be `cap_images_2` to avoid rewrite
           6. Capture images for one class,
                push `boot` button on board and release to capture one image,
                this will save images as `cap_images_1/0/0.jpg`,
                the name of image will automaitcally increase, like `0.jpg` `1.jpg` ...
           7. Long push `boot` botton on board to switch class,
                this will create a new directory like `cap_images_1/1/`,
                and later captured images will be saved to this directory like `cap_images_1/1/0.jpg`
           8. Power off board, pop out SD card, mount on your PC, now you get your images in your file brower
    @update https://github.com/sipeed/MaixPy_scripts
    @author neucrack@sipeed
    @license MIT
'''

import sensor, lcd
from Maix import GPIO
from fpioa_manager import fm
from board import board_info
import os, sys
import time
import image

#### image size ####
set_windowing = (224, 224)       

#### sensor config ####

sensor.reset(freq=22000000, dual_buff=False)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA) # 320x240
try:
    sensor.set_jb_quality(95)         # for IDE display quality
except Exception:
    pass # no IDE support
if set_windowing:
    sensor.set_windowing(set_windowing)
# sensor.set_auto_gain(False)
# sensor.set_auto_whitebal(False, rgb_gain_db=(0x52,0x40,0x4d))
# sensor.set_saturation(0)
# sensor.set_brightness(4)
# sensor.set_contrast(0)
# sensor.set_hmirror(True)        # image horizonal mirror
# sensor.set_vflip(True)          # image vertical flip
# sensor.set_auto_whitebal(False)

sensor.skip_frames()

#### lcd config ####
lcd.init(type=1, freq=15000000)
lcd.rotation(2)

#### boot key ####
boot_pin = 16 # board_info.BOOT_KEY
fm.register(boot_pin, fm.fpioa.GPIOHS0)
key = GPIO(GPIO.GPIOHS0, GPIO.PULL_UP)

######################################################

#### main ####
def capture_main(key):
    def draw_string(img, x, y, text, color, scale, bg=None , full_w = False):
        if bg:
            if full_w:
                full_w = img.width()
            else:
                full_w = len(text)*8*scale+4
            img.draw_rectangle(x-2,y-2, full_w, 16*scale, fill=True, color=bg)
        img = img.draw_string(x, y, text, color=color,scale=scale)
        return img

    def del_all_images():
        os.chdir("/sd")
        images_dir = "cap_images"
        if images_dir in os.listdir():
            os.chdir(images_dir)
            types = os.listdir()
            for t in types:
                os.chdir(t)
                files = os.listdir()
                for f in files:
                    os.remove(f)
                os.chdir("..")
                os.rmdir(t)
            os.chdir("..")
            os.rmdir(images_dir)

    # del_all_images()
    os.chdir("/sd")
    dirs = os.listdir()
    images_dir = "cap_images"
    last_dir = 0
    for d in dirs:
        if d.startswith(images_dir):
            if len(d) > 11:
                n = int(d[11:])
                if n > last_dir:
                    last_dir = n
    images_dir = "{}_{}".format(images_dir, last_dir+1)
    print("save to ", images_dir)
    if images_dir in os.listdir():
        img = image.Image()
        img = draw_string(img, 2, 200, "please del cap_images dir", color=lcd.WHITE,scale=1, bg=lcd.RED)
        lcd.display(img)
        sys.exit(1)
    os.mkdir(images_dir)
    last_cap_time = 0
    last_btn_status = 1
    save_dir = 0
    save_count = 0
    os.mkdir("{}/{}".format(images_dir, save_dir))
    while(True):
        img0 = sensor.snapshot()
        if set_windowing:
            img = image.Image()
            img = img.draw_image(img0, (img.width() - set_windowing[0])//2, img.height() - set_windowing[1])
        else:
            img = img0.copy()
        # img = img.resize(320, 240)
        if key.value() == 0:
            time.sleep_ms(30)
            if key.value() == 0 and (last_btn_status == 1) and (time.ticks_ms() - last_cap_time > 500):
                last_btn_status = 0
                last_cap_time = time.ticks_ms()
            else:
                if time.ticks_ms() - last_cap_time > 5000:
                    img = draw_string(img, 2, 200, "release to change type", color=lcd.WHITE,scale=1, bg=lcd.RED)
                else:
                    img = draw_string(img, 2, 200, "release to capture", color=lcd.WHITE,scale=1, bg=lcd.RED)
                    if time.ticks_ms() - last_cap_time > 2000:
                        img = draw_string(img, 2, 160, "keep push to change type", color=lcd.WHITE,scale=1, bg=lcd.RED)
        else:
            time.sleep_ms(30)
            if key.value() == 1 and (last_btn_status == 0):
                if time.ticks_ms() - last_cap_time > 5000:
                    img = draw_string(img, 2, 200, "change object type", color=lcd.WHITE,scale=1, bg=lcd.RED)
                    lcd.display(img)
                    time.sleep_ms(1000)
                    save_dir += 1
                    save_count = 0
                    dir_name = "{}/{}".format(images_dir, save_dir)
                    os.mkdir(dir_name)
                else:
                    draw_string(img, 2, 200, "capture image {}".format(save_count), color=lcd.WHITE,scale=1, bg=lcd.RED)
                    lcd.display(img)
                    f_name = "{}/{}/{}.jpg".format(images_dir, save_dir, save_count)
                    img0.save(f_name, quality=95)
                    save_count += 1
                last_btn_status = 1
        img = draw_string(img, 2, 0, "will save to {}/{}/{}.jpg".format(images_dir, save_dir, save_count), color=lcd.WHITE,scale=1, bg=lcd.RED, full_w=True)
        lcd.display(img)
        del img
        del img0


def main():
    try:
        capture_main(key)
    except Exception as e:
        print("error:", e)
        import uio
        s = uio.StringIO()
        sys.print_exception(e, s)
        s = s.getvalue()
        img = image.Image()
        img.draw_string(0, 0, s)
        lcd.display(img)
main()

