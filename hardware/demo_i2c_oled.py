import time
from machine import I2C

SSD1306_CMD  = 0
SSD1306_DATA = 1
SSD1306_ADDR = 0x3c

def oled_init(i2c):
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0xAE, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0x20, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0x10, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0xb0, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0xc8, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0x00, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0x10, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0x40, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0x81, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0xff, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0xa1, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0xa6, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0xa8, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0x3F, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0xa4, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0xd3, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0x00, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0xd5, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0xf0, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0xd9, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0x22, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0xda, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0x12, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0xdb, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0x20, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0x8d, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0x14, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0xaf, mem_size=8)



def oled_on(i2c):
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0X8D, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0X14, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0XAF, mem_size=8)

def oled_off(i2c):
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0X8D, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0X10, mem_size=8)
    i2c.writeto_mem(SSD1306_ADDR, 0x00, 0XAE, mem_size=8)

def oled_fill(i2c, data):
    for i in range(0,8):
        i2c.writeto_mem(SSD1306_ADDR, 0x00, 0xb0+i, mem_size=8)
        i2c.writeto_mem(SSD1306_ADDR, 0x00, 0x10, mem_size=8)
        i2c.writeto_mem(SSD1306_ADDR, 0x00, 0x01, mem_size=8)
        for j in range(0,128):
            i2c.writeto_mem(SSD1306_ADDR, 0x40, data, mem_size=8)

i2c = I2C(I2C.I2C0, mode=I2C.MODE_MASTER, freq=400000, scl=28, sda=29, addr_size=7)

time.sleep(1)
oled_init(i2c)
oled_fill(i2c, 0xff)

