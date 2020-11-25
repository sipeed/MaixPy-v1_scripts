
def encode_get_utf8_size(utf):
    if utf < 0x80:
        return 1
    if utf >= 0x80 and utf < 0xC0:
        return -1
    if utf >= 0xC0 and utf < 0xE0:
        return 2
    if utf >= 0xE0 and utf < 0xF0:
        return 3
    if utf >= 0xF0 and utf < 0xF8:
        return 4
    if utf >= 0xF8 and utf < 0xFC:
        return 5
    if utf >= 0xFC:
        return 6

def encode_utf8_to_unicode(utf8):
    utfbytes = encode_get_utf8_size(utf8[0])
    if utfbytes == 1:
        unic = utf8[0]
    if utfbytes == 2:
        b1 = utf8[0]
        b2 = utf8[1]
        if ((b2 & 0xE0) != 0x80):
            return -1
        unic = ((((b1 << 6) + (b2 & 0x3F)) & 0xFF) << 8) | (((b1 >> 2) & 0x07) & 0xFF)
    if utfbytes == 3:
        b1 = utf8[0]
        b2 = utf8[1]
        b3 = utf8[2]
        if (((b2 & 0xC0) != 0x80) or ((b3 & 0xC0) != 0x80)):
            return -1
        unic = ((((b1 << 4) + ((b2 >> 2) & 0x0F)) & 0xFF) << 8) | (((b2 << 6) + (b3 & 0x3F)) & 0xFF)

    if utfbytes == 4:
        b1 = utf8[0]
        b2 = utf8[1]
        b3 = utf8[2]
        b4 = utf8[3]
        if (((b2 & 0xC0) != 0x80) or ((b3 & 0xC0) != 0x80) or ((b4 & 0xC0) != 0x80)):
            return -1
        unic = ((((b3 << 6) + (b4 & 0x3F)) & 0xFF) << 16) | ((((b2 << 4) + ((b3 >> 2)
                                                                  & 0x0F)) & 0xFF) << 8) | ((((b1 << 2) & 0x1C) + ((b2 >> 4) & 0x03)) & 0xFF)
    if utfbytes == 5:
        b1 = utf8[0]
        b2 = utf8[1]
        b3 = utf8[2]
        b4 = utf8[3]
        b5 = utf8[4]
        if (((b2 & 0xC0) != 0x80) or ((b3 & 0xC0) != 0x80) or ((b4 & 0xC0) != 0x80) or ((b5 & 0xC0) != 0x80)):
            return -1
        unic = ((((b4 << 6) + (b5 & 0x3F)) & 0xFF) << 24) | (((b3 << 4) + ((b4 >> 2) & 0x0F) & 0xFF) << 16) | ((((b2 << 2) + ((b3 >> 4) & 0x03)) & 0xFF) << 8) | (((b1 << 6)) & 0xFF)
    if utfbytes == 6:
        b1 = utf8[0]
        b2 = utf8[1]
        b3 = utf8[2]
        b4 = utf8[3]
        b5 = utf8[4]
        b6 = utf8[5]

        if (((b2 & 0xC0) != 0x80) or ((b3 & 0xC0) != 0x80) or ((b4 & 0xC0) != 0x80) or ((b5 & 0xC0) != 0x80) or ((b6 & 0xC0) != 0x80)):
            return -1

        unic = ((((b5 << 6) + (b6 & 0x3F)) << 24) & 0xFF) | (((b5 << 4) + ((b6 >> 2) & 0x0F) << 16) & 0xFF) | ((((b3 << 2) + ((b4 >> 4) & 0x03)) << 8) & 0xFF) | ((((b1 << 6) & 0x40) + (b2 & 0x3F)) & 0xFF)

    return unic

import lcd, time
import image

lcd.init(freq=15000000)
##lcd.direction(lcd.YX_RLDU)

##img = image.Image("ts.bmp")
img = image.Image(size=(240, 240))
img.draw_rectangle((0,0,240,240), fill=True, color=(150,150,150))
#img.draw_string(60, 100, "hello \nmaixpy", scale=4)
#img.draw_rectangle((120,120,30,30))
#img.draw_circle((150,140, 80))
#img.draw_cross((200,40))
#img.draw_arrow((200,200,20,200), color=(236,36,36))
#img.draw_image(image.Image("test.bmp"), 20, 30)

def draw_string(img, x, y, c, s, string, width, high, fonts, space=1):
    i = 0
    pos = 0
    while i < len(string):
        utfbytes = encode_get_utf8_size(string[i])
        print(i, string[i], utfbytes, string[i:i+utfbytes])
        tmp = encode_utf8_to_unicode(string[i:i+utfbytes])
        i += utfbytes
        pos += 1
        fonts.seek(tmp * int(high*(width/8)))
        img.draw_font(x + (pos * s * (width + space)), y, width, high, fonts.read(int(high*(width/8))), scale=s, color=c)

import os

unicode_dict = open('/sd/unicode_8_8_u_d_l_r.Dzk', 'rb')

draw_string(img, 0, 20, (0,0,0), 3, b'你好，世界', 8, 8, unicode_dict)

draw_string(img, 0, 60, (0,0,0), 2, b'hello world!', 8, 8, unicode_dict)

unicode_dict.close()

unicode_dict = open('/sd/unicode_16_16_u_d_l_r.Dzk', 'rb')

draw_string(img, 0, 100, (0,255,0), 2, b'你好，世界', 16, 16, unicode_dict)

draw_string(img, 0, 140, (0,255,0), 1, b'hello world!', 16, 16, unicode_dict)

unicode_dict.close()

# 8 * 8

tmp = b'\x20\xFC\xFC\x2C\xAC\x4C\x4D\xA3'

img.draw_font(10, 20, 8, 8, tmp, scale=1, color=(0,0,0))
img.draw_font(60, 15, 8, 8, tmp, scale=2, color=(255,0,0))
img.draw_font(110, 10, 8, 8, tmp, scale=3, color=(0,255,0))

img.draw_font(150, 10, 16, 8, b'\x00\x00\x00\x00\x7F\x01\x01\xFF\x00\x00\x00\x78\x80\x00\x04\xFE', scale=2, color=(0,0,255))

img.draw_font(200, 10, 8, 16, b'\x00\x00\x00\x00\x7F\x01\x01\xFF\x01\x01\x01\x01\x01\x01\x01\x01', scale=2, color=(0,0,255))

img.draw_font(200, 10, 8, 10, b'\x01\x02\x04\x08\x10\x20\x40\x80\x01\x02', scale=4, color=(0,0,255))

# 16 * 16

qian = b'\x00\x00\x00\x00\x7F\x01\x01\xFF\x01\x01\x01\x01\x01\x01\x01\x01\x00\x00\x00\x78\x80\x00\x04\xFE\x00\x00\x00\x00\x00\x00\x00\x00'

img.draw_font(10, 50, 16, 16, qian, scale=1, color=(0,0,0))
img.draw_font(10, 100, 16, 16, qian, scale=2, color=(0,0,0))
img.draw_font(10, 150, 16, 16, qian, scale=3, color=(0,0,0))

li = b'\x00\x00\x00\x1F\x11\x11\x1F\x11\x1F\x11\x01\x01\x3F\x01\x01\xFF\x00\x00\x08\xF8\x08\x08\xF8\x08\xF8\x08\x00\x08\xFC\x00\x00\xFE'

img.draw_font(60, 50, 16, 16, li, scale=1, color=(255,0,0))
img.draw_font(60, 100, 16, 16, li, scale=2, color=(255,0,0))
img.draw_font(60, 150, 16, 16, li, scale=3, color=(255,0,0))

zhi = b'\x00\x00\x02\x01\x01\x7F\x00\x00\x00\x00\x01\x06\x08\x30\x4C\x03\x00\x00\x00\x00\x08\xFC\x10\x20\x40\x80\x00\x00\x00\x00\x00\xFE'

img.draw_font(120, 50, 16, 16, zhi, scale=1, color=(0,255,0))
img.draw_font(120, 100, 16, 16, zhi, scale=2, color=(0,255,0))
img.draw_font(120, 150, 16, 16, zhi, scale=3, color=(0,255,0))

wai = b'\x00\x00\x04\x08\x08\x0F\x11\x11\x29\x26\x42\x04\x04\x08\x10\x20\x00\x00\x20\x20\x20\xA0\x20\x38\x24\x22\x20\x20\x20\x20\x20\x20'

img.draw_font(180, 50, 16, 16, wai, scale=1, color=(0,0,255))
img.draw_font(180, 100, 16, 16, wai, scale=2, color=(0,0,255))
img.draw_font(180, 150, 16, 16, wai, scale=3, color=(0,0,255))

lcd.display(img)
