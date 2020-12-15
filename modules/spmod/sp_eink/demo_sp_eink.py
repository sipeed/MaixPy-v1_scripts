from micropython import const
from time import sleep_ms
import ustruct
import image

# Display resolution
SPEINK_WIDTH = const(200)
SPEINK_HEIGHT = const(200)
SPEINK_ROTATION = const(180) # 0, 90, 180, 270
BUSY = const(1)  # 1=busy, 0=idle

class SPEINK:
    def __init__(self, spi, cs, dc, rst, busy, width, height, rotation):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.busy = busy
        self.cs.value(0)
        self.dc.value(0)
        self.rst.value(1)
        self.width = width
        self.height = height
        self.rotation = rotation

    lut_vcom0 = bytearray(
        b'\x0E\x14\x01\x0A\x06\x04\x0A\x0A\x0F\x03\x03\x0C\x06\x0A\x00')
    lut_w = bytearray(
        b'\x0E\x14\x01\x0A\x46\x04\x8A\x4A\x0F\x83\x43\x0C\x86\x0A\x04')
    lut_b = bytearray(
        b'\x0E\x14\x01\x8A\x06\x04\x8A\x4A\x0F\x83\x43\x0C\x06\x4A\x04')
    lut_g1 = bytearray(
        b'\x8E\x94\x01\x8A\x06\x04\x8A\x4A\x0F\x83\x43\x0C\x06\x0A\x04')
    lut_g2 = bytearray(
        b'\x8E\x94\x01\x8A\x06\x04\x8A\x4A\x0F\x83\x43\x0C\x06\x0A\x04')
    lut_vcom1 = bytearray(
        b'\x03\x1D\x01\x01\x08\x23\x37\x37\x01\x00\x00\x00\x00\x00\x00')
    lut_red0 = bytearray(
        b'\x83\x5D\x01\x81\x48\x23\x77\x77\x01\x00\x00\x00\x00\x00\x00')
    lut_red1 = bytearray(
        b'\x03\x1D\x01\x01\x08\x23\x37\x37\x01\x00\x00\x00\x00\x00\x00')

    def _command(self, command, data=None):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([command]))
        self.cs(1)
        if data is not None:
            self._data(data)
        self.dc(1)

    def _data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(data)
        self.cs(1)

    def reset(self):
        self.dc(0)
        sleep_ms(200)
        self.dc(1)
        self.rst(0)
        sleep_ms(100)
        self.rst(1)
        sleep_ms(200)

    def init(self):
        self.reset()
        self._command(0x01)
        self._data(0x07)  # 设置高低电压
        self._data(0x00)
        self._data(0x0f)  # 红色电压设置，值越大红色越深
        self._data(0x00)
        self._command(0x06)
        self._data(0x07)
        self._data(0x07)
        self._data(0x07)
        self._command(0x04)  # 上电

        if self.wait_until_idle() == False:
            pass

        self._command(0X00)
        self._data(0xcf)  # 选择最大分辨率

        self._command(0X50)
        self._data(0x37)

        self._command(0x30)
        self._data(0x39)  # PLL设定

        self._command(0x61)  # 像素设定
        self._data(0xC8)  # 200像素
        self._data(0x00)  # 200像素
        self._data(0xC8)

        self._command(0x82)  # vcom设定
        self._data(0x18)

        self.lut_bw()
        self.lut_red()

    # brief: display image on eink
    # img_r: red image
    # img_bw: b/w image
    def display(self, img_r, img_bw = None):
        img1 = image.Image()  # handle image
        img1 = img1.resize(self.width, self.height)

        if(img_bw == None):
            self._command(0x10)  # write "B/W" data to SRAM. 0x00:black
            for i in range(10000):
                self._data(0xff)
        else:
            img1.draw_image(img_bw, 0, 0)
            # Parameter 'fov' is to slove data loss issues
            img1.rotation_corr(x_rotation=self.rotation, fov=2)
            img_bytes = img1.to_bytes()  # That's "self.width*self.height*2" bytes
            self._command(0x10)  # write "B/W" data to SRAM 0x00:black,0xff:white
            for i in range(0, self.width*self.height*2, 16):
                b = 0
                for j in range(0, 8, 2):
                    if img_bytes[i+j] or img_bytes[i+j+1]:
                        b = b | (0xc0 >> j)
                self._data(~b)
                b = 0
                for j in range(8, 16, 2):
                    if img_bytes[i+j] or img_bytes[i+j+1]:
                        b = b | (0xc0 >> j-8)
                self._data(~b)

        img1.draw_image(img_r, 0, 0)
        # Parameter 'fov' is to slove data loss issues
        img1.rotation_corr(x_rotation=180, fov=2)
        img_bytes = img1.to_bytes()  # That's "self.width*self.height*2" bytes
        self._command(0x13)  # write "RED" data to SRAM 0x00:red,0xff:white
        for i in range(0, self.width*self.height*2, 16):
            b = 0
            for j in range(0, 16, 2):
                if img_bytes[i+j] or img_bytes[i+j+1]:
                    b = b | (0x80 >> j//2)
            self._data(~b)

        self._command(0x12)  # display refresh
        self.wait_until_idle()

    def wait_until_idle(self):
        for i in range(10):
            sleep_ms(100)
            if self.busy.value() != BUSY:
                return True
        print('self.busy', self.busy.value())
        return False

    def lut_bw(self):
        self._command(0x20, SPEINK.lut_vcom0)
        self._command(0x21, SPEINK.lut_w)
        self._command(0x22, SPEINK.lut_b)
        self._command(0x23, SPEINK.lut_g1)
        self._command(0x24, SPEINK.lut_g2)

    def lut_red(self):
        self._command(0x25, SPEINK.lut_vcom1)
        self._command(0x26, SPEINK.lut_red0)
        self._command(0x27, SPEINK.lut_red1)

    # enter deep sleep A0=1, A0=0 power on
    def sleep(self):
        self._command(0x50)
        self._data(0xf7)

        self._command(0x02)
        self.wait_until_idle()
        self._data(0x07)
        self._command(0xa5)


if __name__ == "__main__":
    from Maix import GPIO
    from fpioa_manager import fm
    from machine import SPI

    #  MaixCube | SPMOD
    # [7  |VCC] [RST|3V3]
    # [15 | 21] [D/C|SCK]
    # [20 |  8] [CS |SI ]
    # [GND|  6] [GND|BL ]
    ################### config ###################
    SPI_EINK_NUM = SPI.SPI1
    SPI_EINK_DC_PIN_NUM = const(15)
    SPI_EINK_BUSY_PIN_NUM = const(6)
    SPI_EINK_RST_PIN_NUM = const(7)
    SPI_EINK_CS_PIN_NUM = const(20)
    SPI_EINK_SCK_PIN_NUM = const(21)
    SPI_EINK_MOSI_PIN_NUM = const(8)
    SPI_EINK_FREQ_KHZ = const(600)
    ##############################################

    spi1 = SPI(SPI_EINK_NUM, mode=SPI.MODE_MASTER, baudrate=SPI_EINK_FREQ_KHZ * 1000,
               polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=SPI_EINK_SCK_PIN_NUM, mosi=SPI_EINK_MOSI_PIN_NUM)

    fm.register(SPI_EINK_CS_PIN_NUM, fm.fpioa.GPIOHS20, force=True)
    fm.register(SPI_EINK_DC_PIN_NUM, fm.fpioa.GPIOHS15, force=True)
    fm.register(SPI_EINK_BUSY_PIN_NUM, fm.fpioa.GPIOHS6, force=True)
    fm.register(SPI_EINK_RST_PIN_NUM, fm.fpioa.GPIOHS7, force=True)

    cs = GPIO(GPIO.GPIOHS20, GPIO.OUT)
    dc = GPIO(GPIO.GPIOHS15, GPIO.OUT)
    busy = GPIO(GPIO.GPIOHS6, GPIO.IN, GPIO.PULL_DOWN)
    rst = GPIO(GPIO.GPIOHS7, GPIO.OUT)

    epd = SPEINK(spi1, cs, dc, rst, busy, SPEINK_WIDTH, SPEINK_HEIGHT, SPEINK_ROTATION)
    epd.init()

    # red image 
    img_r = image.Image()
    img_r = img_r.resize(SPEINK_WIDTH, SPEINK_HEIGHT)
    img_r.draw_line(0, 0, 100, 100)
    img_r.draw_circle(50, 50, 20)
    img_r.draw_rectangle(80, 80, 30, 30)

    # bw image
    img_bw = image.Image()
    img_bw = img_bw.resize(SPEINK_WIDTH, SPEINK_HEIGHT)
    img_bw.draw_line(100, 50, 200, 100)
    img_bw.draw_circle(80, 80, 30)
    img_bw.draw_rectangle(10, 10, 60, 60)

    epd.display(img_r, img_bw)
    epd.sleep()
