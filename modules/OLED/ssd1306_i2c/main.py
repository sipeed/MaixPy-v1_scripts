'''
实验名称：I2C总线（OLED显示屏）
版本：v1.0
日期：2019.12
作者：01Studio
实验内容：学习使用MicroPython的I2C总线通讯编程和OLED显示屏的使用。
'''

from machine import I2C
from ssd1306k import SSD1306

#定义I2C接口和OLED对象
i2c = I2C(I2C.I2C0, mode=I2C.MODE_MASTER,scl=27, sda=28)
oled = SSD1306(i2c, addr=0x3c)

#清屏,0x00(白屏)，0xff(黑屏)
oled.fill(0)


#显示字符。参数格式为（str,x,y）,其中x范围是0-127，y范围是0-7（共8行）
oled.text("Hello World!", 0, 0) #写入第 0 行内容
oled.text("MicroPython", 0, 2) #写入第 2 行内容
oled.text("By 01Studio", 0, 5) #写入第 5 行内容
