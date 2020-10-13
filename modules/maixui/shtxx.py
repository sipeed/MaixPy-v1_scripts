
import sys
import time
from machine import I2C

SHT3x_ADDR = 0x45
SHT31_ADDR = 0x44

class SHT3x:

    def __init__(self, i2c, addr = SHT31_ADDR):
        self.i2c = i2c
        #addrs = self.i2c.scan()
        #print(addrs)
        #if SHT3x_ADDR not in addrs or SHT31_ADDR not in addrs:
            #raise Exception('no SHT3X found at bus on %s' % (str(self.i2c)))
        self.addr = addr
        self.last = 0
        self.cache = [0, 0]

    def read_temp_humd(self):
        if self.last == 0:
            status = self.i2c.writeto(self.addr, b'\x24\x00')
            self.last = time.ticks_ms() + 2000
        elif time.ticks_ms() > self.last:
            self.last = 0
            ## delay (20 slow)
            #utime.sleep_ms(20)
            # read 6 bytes
            databytes = self.i2c.readfrom(self.addr, 6)
            dataset = [databytes[0], databytes[1]]
            dataset = [databytes[3], databytes[4]]
            temperature_raw = databytes[0] << 8 | databytes[1]
            temperature = (175.0 * float(temperature_raw) / 65535.0) - 45
            # fahreheit
            # temperature = (315.0 * float(temperature_raw) / 65535.0) - 49
            humidity_raw = databytes[3] << 8 | databytes[4]
            humidity = (100.0 * float(humidity_raw) / 65535.0)
            self.cache = [temperature, humidity]
        return self.cache


if __name__ == "__main__":

    #sht3x = SHT3x(I2C(I2C.I2C0, freq=100*1000, scl=24, sda=25))
    sht3x = SHT3x(I2C(I2C.I2C0, freq=100*1000, scl=24, sda=27))
    #sht3x = SHT3x(I2C(I2C.I2C0, freq=100*1000, scl=23, sda=20))
    #sht3x = SHT3x(I2C(I2C.I2C0, freq=100*1000, scl=9, sda=7))
    while True:
        try:
            print(sht3x.read_temp_humd())
            time.sleep(1)
        except Exception as e:
            print(e)
