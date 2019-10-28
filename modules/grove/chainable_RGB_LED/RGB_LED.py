
from fpioa_manager import *
from Maix import GPIO
import time

class RGB_LED:
    def __init__(self, clk, data, number_leds, clk_gpiohs=fm.fpioa.GPIOHS0, data_gpiohs=fm.fpioa.GPIOHS1, force_register_io = False ):
        if force_register_io:
            fm.register(clk, clk_gpiohs, force=True)
            fm.register(data, data_gpiohs, force=True)
        else:
            ret = fm.register(clk, clk_gpiohs, force=False)
            if ret != 1:
                raise ValueError("pin %d has been registered to func %d" %(ret[0], ret[1]))
            ret = fm.register(data, data_gpiohs, force=False)
            if ret != 1:
                raise ValueError("pin %d has been registered to func %d" %(ret[0], ret[1]))
        self.clk = GPIO(GPIO.GPIOHS0+clk_gpiohs-fm.fpioa.GPIOHS0, GPIO.OUT)
        self.data = GPIO(GPIO.GPIOHS0+data_gpiohs-fm.fpioa.GPIOHS0, GPIO.OUT)
        self.clk.value(1)
        self.data.value(0)
        self.status = []
        for i in range(number_leds):
            self.status.append([0,0,0])

    def check_RGB(self, value):
        if not value in range(0,256):
            raise ValueError("value: [0, 255]")
    
    def check_HSB(self, value):
        if not value in range(0.0,1.0):
            raise ValueError("value: [0, 1]")

    # red, green, blue
    def set_RGB(self, led, r, g, b):
        self.check_RGB(r)
        self.check_RGB(g)
        self.check_RGB(b)
        
        self.send_byte(0x00)
        self.send_byte(0x00)
        self.send_byte(0x00)
        self.send_byte(0x00)
        for i in range(len(self.status)):
            if i == led:
                self.status[i]=[r, g, b]
            self.send_color(self.status[i][0], self.status[i][1], self.status[i][2])
        self.send_byte(0x00)
        self.send_byte(0x00)
        self.send_byte(0x00)
        self.send_byte(0x00)

    # hue, saturation, brightness
    def set_HSB(self, led, h, s, b):
        self.check_HSB(h)
        self.check_HSB(s)
        self.check_HSB(b)
        if s == 0:
            r = b
            g = b
            b = b
        else:
            q = b*(1.0+s) if b<0.5 else b+s-b*s
            p = 2.0 * b -q
            r = int(self.hue_to_rgb(p, q, h + 1/3)) & 0xFF
            g = int(self.hue_to_rgb(p, q, hue)) & 0xFF
            b = int(self.hue_to_rgb(p, q, hue - 1/3)) & 0xFF
            
        self.set_RGB(led, r, g, b)

    def send_byte(self, data):
        for i in range(8):
            if data & 0x80:
                self.data.value(1)
            else:
                self.data.value(0)
            self.write_clk()
            data <<= 1

    def write_clk(self):
        self.clk.value(0)
        time.sleep_us(20)
        self.clk.value(1)
        time.sleep_us(20)

    def send_color(self, r, g, b):
        prefix = 0xC0
        if (b & 0x80) == 0:
            prefix |= 0x20
        if (b & 0x40) == 0:
            prefix |= 0x10
        if (g & 0x80) == 0:
            prefix |= 0x08
        if (g & 0x40) == 0:
            prefix |= 0x04
        if (r & 0x80) == 0:
            prefix |= 0x02
        if (r & 0x40) == 0:
            prefix |= 0x01
        self.send_byte(prefix)
        self.send_byte(b)
        self.send_byte(g)
        self.send_byte(r)

    def hue_to_rgb(self, p, q, t):
        if t < 0:
            t += 1
        if t > 1:
            t -= 1
        if t < 1/6:
            return p + (q - p) * 6.0 * t
        if t < 1/2:
            return q
        if t < 2/3:
            return p + (q - p) * (2/3 - t) * 6
        return p



