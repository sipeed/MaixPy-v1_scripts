from time import sleep_ms
import image
from micropython import const

IPS_WIDTH = const(240)
IPS_HEIGHT = const(135)
IPS_MODE = const(3) # 0 1 horizontal 2 3 vertical

class SPLCD114:
    def __init__(self, spi, cs, dc, rst, busy, width, height, mode):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.busy = busy
        self.width = width
        self.height = height
        self.mode = mode
        self.init()

    def init(self):
        self.rst.value(0)
        sleep_ms(10)
        self.rst.value(1)
        sleep_ms(10)

        self._command(0x11)
        sleep_ms(10)
        self._command(0x36) # set horizontal or vertical
        if self.mode == 0:
            self._data(0x00)
        elif self.mode == 1:
            self._data(0xc0)
        elif self.mode == 2:
            self._data(0x70)
        else:
            self._data(0xa0)

        self._command(0x3a)
        self._data(0x05)

        self._command(0xb2)
        self._data(0x0c)
        self._data(0x0c)
        self._data(0x00)
        self._data(0x33)
        self._data(0x33)

        self._command(0xb7)
        self._data(0x35)

        self._command(0xBB)
        self._data(0x19)

        self._command(0xC0)
        self._data(0x2C)

        self._command(0xC2)
        self._data(0x01)

        self._command(0xC3)
        self._data(0x12)

        self._command(0xC4)
        self._data(0x20)

        self._command(0xC6)
        self._data(0x0F)

        self._command(0xD0)
        self._data(0xA4)
        self._data(0xA1)

        self._command(0xE0)
        self._data(0xD0)
        self._data(0x04)
        self._data(0x0D)
        self._data(0x11)
        self._data(0x13)
        self._data(0x2B)
        self._data(0x3F)
        self._data(0x54)
        self._data(0x4C)
        self._data(0x18)
        self._data(0x0D)
        self._data(0x0B)
        self._data(0x1F)
        self._data(0x23)

        self._command(0xE1)
        self._data(0xD0)
        self._data(0x04)
        self._data(0x0C)
        self._data(0x11)
        self._data(0x13)
        self._data(0x2C)
        self._data(0x3F)
        self._data(0x44)
        self._data(0x51)
        self._data(0x2F)
        self._data(0x1F)
        self._data(0x1F)
        self._data(0x20)
        self._data(0x23)

        self._command(0x21)

        self._command(0x29)

        self.busy.value(0)

    def _command(self,cmd):
        self.dc.value(0)
        self.cs.value(0)
        self.spi.write(cmd)
        self.cs.value(1)
        self.dc.value(1)

    def _data(self,data):
        self.dc.value(1)
        self.cs.value(0)
        self.spi.write(data)
        self.cs.value(1)

    def _data_16b(self,data):
        self._data(data >> 8)
        self._data(data & 0xff)

    def _address_set(self,x1,y1,x2,y2):
        if self.mode == 0:
            self._command(0x2a) #列地址设置
            self._data_16b(x1 + 52)
            self._data_16b(x2 + 52)
            self._command(0x2b) #行地址设置
            self._data_16b(y1 + 40)
            self._data_16b(y2 + 40)
            self._command(0x2c) #储存器写
        elif self.mode == 1:
            self._command(0x2a) #列地址设置
            self._data_16b(x1 + 53)
            self._data_16b(x2 + 53)
            self._command(0x2b) #行地址设置
            self._data_16b(y1 + 40)
            self._data_16b(y2 + 40)
            self._command(0x2c) #储存器写
        elif self.mode == 2:
            self._command(0x2a) #列地址设置
            self._data_16b(x1 + 40)
            self._data_16b(x2 + 40)
            self._command(0x2b) #行地址设置
            self._data_16b(y1 + 53)
            self._data_16b(y2 + 53)
            self._command(0x2c) #储存器写
        else:
            self._command(0x2a) #列地址设置
            self._data_16b(x1 + 40)
            self._data_16b(x2 + 40)
            self._command(0x2b) #行地址设置
            self._data_16b(y1 + 52)
            self._data_16b(y2 + 52)
            self._command(0x2c) #储存器写

    def display(self,img):
        img1 = image.Image()
        img1 = img1.resize(self.width,self.height)
        img1.draw_image(img, 0, 0)
        img_bytes = img1.to_bytes()
        self._address_set(0,0,self.width-1,self.height-1)
        self._data(img_bytes)

if __name__ == "__main__":
    from Maix import GPIO
    from fpioa_manager import fm
    from machine import SPI
    from micropython import const

    # SPMOD  |MaixCube
    # [7  |VCC] [RST|3V3]
    # [15 | 21] [D/C|SCK]
    # [20 |  8] [CS |SI ]
    # [GND|  6] [GND|BL ]

    ################### config ###################
    SPI_LCD_NUM = SPI.SPI1
    SPI_LCD_DC_PIN_NUM = const(15)
    SPI_LCD_BUSY_PIN_NUM = const(6)
    SPI_LCD_RST_PIN_NUM = const(7)
    SPI_LCD_CS_PIN_NUM = const(20)
    SPI_LCD_SCK_PIN_NUM = const(21)
    SPI_LCD_MOSI_PIN_NUM = const(8)
    SPI_LCD_FREQ_KHZ = const(600)
    ##############################################

    # 21: SPI_LCD_SCK_PIN_NUM; 8: SPI_LCD_MOSI_PIN_NUM;
    spi1 = SPI(SPI_LCD_NUM, mode=SPI.MODE_MASTER, baudrate=SPI_LCD_FREQ_KHZ * 1000,
               polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=SPI_LCD_SCK_PIN_NUM, mosi=SPI_LCD_MOSI_PIN_NUM)

    # 20: SPI_LCD_CS_PIN_NUM;
    fm.register(SPI_LCD_CS_PIN_NUM, fm.fpioa.GPIOHS20, force=True)
    # 15: SPI_LCD_DC_PIN_NUM;
    fm.register(SPI_LCD_DC_PIN_NUM, fm.fpioa.GPIOHS15, force=True)
    # 6: SPI_LCD_BUSY_PIN_NUM;
    fm.register(SPI_LCD_BUSY_PIN_NUM, fm.fpioa.GPIOHS6, force=True)
    # 7: SPI_LCD_RST_PIN_NUM;
    fm.register(SPI_LCD_RST_PIN_NUM, fm.fpioa.GPIOHS7, force=True)

    # set gpiohs work mode to output mode
    cs = GPIO(GPIO.GPIOHS20, GPIO.OUT)
    dc = GPIO(GPIO.GPIOHS15, GPIO.OUT)
    busy = GPIO(GPIO.GPIOHS6, GPIO.OUT)
    rst = GPIO(GPIO.GPIOHS7, GPIO.OUT)

    ips = SPLCD114(spi1, cs, dc, rst, busy, IPS_WIDTH, IPS_HEIGHT, IPS_MODE)
    
    img = image.Image()
    img.draw_line(0, 0, 100, 100)
    img.draw_circle(50, 50, 20)
    img.draw_rectangle(80, 80, 30, 30)
    img.draw_circle(70, 70, 8)
    img.draw_circle(70, 160, 15)
    img.draw_circle(170, 70, 8)
    img.draw_circle(110, 40, 15)

    ips.display(img)
