# ADXL345 Python library for Raspberry Pi 
#
# author:  Jonathan Williamson
# license: BSD, see LICENSE.txt included in this package
# 
# This is a Raspberry Pi Python implementation to help you get started with
# the Adafruit Triple Axis ADXL345 breakout board:
# http://shop.pimoroni.com/products/adafruit-triple-axis-accelerometer

from time import sleep
import ustruct
# ADXL345 constants
EARTH_GRAVITY_MS2   = 9.80665
SCALE_MULTIPLIER    = 0.004

DATA_FORMAT         = 0x31
BW_RATE             = 0x2C
POWER_CTL           = 0x2D

BW_RATE_1600HZ      = 0x0F
BW_RATE_800HZ       = 0x0E
BW_RATE_400HZ       = 0x0D
BW_RATE_200HZ       = 0x0C
BW_RATE_100HZ       = 0x0B
BW_RATE_50HZ        = 0x0A
BW_RATE_25HZ        = 0x09

RANGE_2G            = 0x00
RANGE_4G            = 0x01
RANGE_8G            = 0x02
RANGE_16G           = 0x03

MEASURE             = 0x08
AXES_DATA           = 0x32

class ADXL345:

    address = None

    def __init__(self, i2c = None, address = 0x53):        
        self.address = address
        self.bus = i2c
        self.setBandwidthRate(BW_RATE_100HZ)
        self.setRange(RANGE_8G)
        self.enableMeasurement()
        
    def enableMeasurement(self):
        self.bus.writeto_mem(self.address, POWER_CTL, MEASURE)

    def setBandwidthRate(self, rate_flag):
        self.bus.writeto_mem(self.address, BW_RATE, rate_flag)

    # set the measurement range for 10-bit readings
    def setRange(self, range_flag):
        bs = self.bus.readfrom_mem(self.address, DATA_FORMAT, 1)
        value = ustruct.unpack('<B',bs)[0]
        value &= ~0x0F;
        value |= range_flag;  
        value |= 0x08;
        bs = ustruct.pack('<B', value)
        self.bus.writeto_mem(self.address, DATA_FORMAT, value)
    
    # returns the current reading from the sensor for each axis
    #
    # parameter gforce:
    #    False (default): result is returned in m/s^2
    #    True           : result is returned in gs
    def getAxes(self, gforce = False):
        bytes = self.bus.readfrom_mem(self.address, AXES_DATA, 6)
        
        x = bytes[0] | (bytes[1] << 8)
        if(x & (1 << 16 - 1)):
            x = x - (1<<16)

        y = bytes[2] | (bytes[3] << 8)
        if(y & (1 << 16 - 1)):
            y = y - (1<<16)

        z = bytes[4] | (bytes[5] << 8)
        if(z & (1 << 16 - 1)):
            z = z - (1<<16)

        x = x * SCALE_MULTIPLIER 
        y = y * SCALE_MULTIPLIER
        z = z * SCALE_MULTIPLIER

        if gforce == False:
            x = x * EARTH_GRAVITY_MS2
            y = y * EARTH_GRAVITY_MS2
            z = z * EARTH_GRAVITY_MS2

        x = round(x, 4)
        y = round(y, 4)
        z = round(z, 4)

        return {"x": x, "y": y, "z": z}

if __name__ == "__main__":
    # if run directly we'll just create an instance of the class and output 
    # the current readings
    from machine import I2C
    from fpioa_manager import fm
    import time

    i2c = I2C(I2C.I2C1, mode=I2C.MODE_MASTER, scl=23, sda=24, gscl=fm.fpioa.GPIOHS3, 
            gsda=fm.fpioa.GPIOHS4, freq=100000, timeout=1000, addr=0, addr_size=7)

    adxl345 = ADXL345(i2c)
    while True:
        axes = adxl345.getAxes(True)
        print("ADXL345 on address 0x%x:" % (adxl345.address))
        print("   x = %.3fG" % ( axes['x'] ))
        print("   y = %.3fG" % ( axes['y'] ))
        print("   z = %.3fG" % ( axes['z'] ))
        time.sleep_ms(100)