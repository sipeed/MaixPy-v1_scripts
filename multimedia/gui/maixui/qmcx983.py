from machine import I2C
import lcd
import time
from ustruct import unpack, unpack_from
from array import array

#I2C devices:[44, 118]
# i2c_bus = I2C(I2C.I2C0, freq=100*1000, scl=6, sda=7)
# i2c_devs_list = i2c_bus.scan()
# print("I2C devices:" + str(i2c_devs_list))

QMC6983_A1_D1       = 0
QMC6983_E1          = 1
QMC7983             = 2
QMC7983_LOW_SETRESET= 3
QMC6983_E1_Metal    = 4
QMC7983_Vertical    = 5
QMC7983_Slope       = 6

# QMCX983 default address.
QMCX983_I2CADDR = 0x2C

class QMCX983:

    def __init__(self, i2c=None,
                 address=QMCX983_I2CADDR,
                 **kwargs):
        self.address = address
        if i2c is None:
            raise ValueError('An I2C object is required.')
        self.i2c = i2c
        self.mag_chip_id = 0

        self.i2c.writeto_mem(self.address, 0x09,
                             bytearray([0x1d]))
        chip = self.i2c.readfrom_mem(self.address, 0x0d, 1)
        #print("chip id: " + str(chip))
        print(hex(chip[0]))
        if 0x31 == chip[0]:
            self.mag_chip_id = QMC6983_E1
        elif 0x32 == chip[0]:
            self.i2c.writeto_mem(self.address, 0x2e, bytearray([0x01]))
            chip = self.i2c.readfrom_mem(self.address, 0x2f, 1)
            if ((chip[0]&0x04) >>2) != 0:
                self.mag_chip_id = QMC6983_E1_Metal
            else:
                self.i2c.writeto_mem(self.address, 0x2e, bytearray([0x0f]))
                chip = self.i2c.readfrom_mem(self.address, 0x2f, 1)
                if (0x02 == ((chip[0]&0x3C)>>2)):
                    self.mag_chip_id = QMC7983_Vertical
                if (0x03 == ((chip[0]&0x3C)>>2)):
                    self.mag_chip_id = QMC7983_Slope
        else:
            return
        print(self.mag_chip_id)
        self.i2c.writeto_mem(self.address, 0x21, bytearray([0x01]))
        self.i2c.writeto_mem(self.address, 0x20, bytearray([0x40]))
        if (self.mag_chip_id != QMC6983_A1_D1):
            self.i2c.writeto_mem(self.address, 0x29, bytearray([0x80]))
            self.i2c.writeto_mem(self.address, 0x0a, bytearray([0x0c]))
        if (self.mag_chip_id == QMC6983_E1_Metal or self.mag_chip_id == QMC7983_Slope ):
            self.i2c.writeto_mem(self.address, 0x1b, bytearray([0x80]))
        self.i2c.writeto_mem(self.address, 0x0b, bytearray([0x01]))
        self.i2c.writeto_mem(self.address, 0x09, bytearray([0x1d]))

    def read_xyz(self):
        read_data = self.i2c.readfrom_mem(self.address, 0x00, 6)
        #if (self.mag_chip_id >= 3)
        raw = bytearray(3)
        raw[0] = (read_data[1]<<8) | read_data[0]
        raw[1] = (read_data[3]<<8) | read_data[2]
        raw[2] = (read_data[5]<<8) | read_data[4]
        return (raw[0], raw[1], raw[2])
        # return "({:.1f}|{:.1f}|{:.1f})".format(raw[0]/25.0, raw[1]/25.0, raw[2]/25.0)

if __name__ == "__main__":

    from machine import I2C
    import lcd, time
    import micropython, gc

    i2c_bus = I2C(I2C.I2C0, freq=100*1000, scl=6, sda=7)
    i2c_devs_list = i2c_bus.scan()
    print("I2C devices:" + str(i2c_devs_list))

    bme=QMCX983(i2c=i2c_bus)
    lcd.init()
    while 1:
        time.sleep_ms(500)
        data = bme.read_xyz()
        print(data)
