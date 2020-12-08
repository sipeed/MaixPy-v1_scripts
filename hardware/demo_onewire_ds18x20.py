from fpioa_manager import *
from modules import onewire
from micropython import const
from board import board_info
import time

class DS18X20:
    _CONVERT = const(0x44)
    _RD_SCRATCH = const(0xBE)
    _WR_SCRATCH = const(0x4E)
    _SKIP_ROM = const(0xCC)
    def __init__(self, pin):
        self.device = onewire(pin)
        self.buf = bytearray(9)

    def scan(self):
        return self.device.search(65)

    def convert_temp(self):
        self.device.reset()
        self.device.writebyte(_SKIP_ROM)
        self.device.writebyte(_CONVERT)

    def read_scratch(self, rom):
        self.device.reset()
        self.convert_temp()
        self.device.select(rom)
        self.device.writebyte(_RD_SCRATCH)
        self.buf = self.device.readbuffer(len(self.buf))
        if self.device.crc8(self.buf):
            raise Exception("CRC error")
        return self.buf

    def write_scratch(self, rom, buf):
        self.device.reset()
        self.device.select(rom)
        self.device.writebyte(_WR_SCRATCH)
        self.device.writebuffer(buf)

    def read_temp(self, rom):
        temp = []
        for _rom in rom:
            buf = self.read_scratch(_rom)
            if _rom[0] == 0x10:
                if buf[1]:
                    t = buf[0] >> 1 | 0x80
                    t = -((~t + 1) & 0xFF)
                else:
                    t = buf[0] >> 1
                temp.append(t - 0.25 + (buf[7] - buf[6]) / buf[7])
            else:
                t = buf[1] << 8 | buf[0]
                if t & 0x8000:  # sign bit set
                    t = -((t ^ 0xFFFF) + 1)
                temp.append(t / 16)
        if len(temp) < 1:
            return -1
        if len(temp) < 2:
            return temp[0]
        return tuple(temp)


fm.register(14, fm.fpioa.GPIOHS2, force=True)
ds18b20_2 = DS18X20(fm.fpioa.GPIOHS2)
while True:
    print(ds18b20_2.read_temp(rom_2))
    time.sleep_ms(100)
