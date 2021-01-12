from machine import I2C
import time
from ustruct import unpack, unpack_from
from array import array

############ QMCX983 config ############
QMC6983_A1_D1       = 0
QMC6983_E1          = 1
QMC7983             = 2
QMC7983_LOW_SETRESET= 3
QMC6983_E1_Metal    = 4
QMC7983_Vertical    = 5
QMC7983_Slope       = 6
# QMCX983 default qmc_address.
QMCX983_I2CADDR = 0x2C

############ BME280 config ############
# BME280 default bme_address.
BME280_I2CADDR = 0x76
# Operating Modes
BME280_OSAMPLE_1 = 1
BME280_OSAMPLE_2 = 2
BME280_OSAMPLE_4 = 3
BME280_OSAMPLE_8 = 4
BME280_OSAMPLE_16 = 5
BME280_REGISTER_CONTROL_HUM = 0xF2
BME280_REGISTER_CONTROL = 0xF4

class SPWEATHER:
    def __init__(self, i2c=None):
        if i2c is None:
            raise ValueError('An I2C object is required.')
        self.i2c = i2c
        self.qmc_init() # Magnetic sensor QMC7983 init 
        self.bme280_init() # Temperature, humidity and pressure sensors BME280 init 

    ################## QMCX983 ##################
    def qmc_init(self, qmc_address=QMCX983_I2CADDR, **kwargs):
        self.qmc_address = qmc_address
        self.mag_chip_id = 0

        self.i2c.writeto_mem(self.qmc_address, 0x09,
                             bytearray([0x1d]))
        chip = self.i2c.readfrom_mem(self.qmc_address, 0x0d, 1)
        #print("chip id: " + str(chip))
        print("chip id:", hex(chip[0]))
        if 0x31 == chip[0]:
            self.mag_chip_id = QMC6983_E1
        elif 0x32 == chip[0]:
            self.i2c.writeto_mem(self.qmc_address, 0x2e, bytearray([0x01]))
            chip = self.i2c.readfrom_mem(self.qmc_address, 0x2f, 1)
            if ((chip[0]&0x04) >>2) != 0:
                self.mag_chip_id = QMC6983_E1_Metal
            else:
                self.i2c.writeto_mem(self.qmc_address, 0x2e, bytearray([0x0f]))
                chip = self.i2c.readfrom_mem(self.qmc_address, 0x2f, 1)
                if (0x02 == ((chip[0]&0x3C)>>2)):
                    self.mag_chip_id = QMC7983_Vertical
                if (0x03 == ((chip[0]&0x3C)>>2)):
                    self.mag_chip_id = QMC7983_Slope
        else:
            return
        print("mag_chip_id: ", self.mag_chip_id)
        self.i2c.writeto_mem(self.qmc_address, 0x21, bytearray([0x01]))
        self.i2c.writeto_mem(self.qmc_address, 0x20, bytearray([0x40]))
        if (self.mag_chip_id != QMC6983_A1_D1):
            self.i2c.writeto_mem(self.qmc_address, 0x29, bytearray([0x80]))
            self.i2c.writeto_mem(self.qmc_address, 0x0a, bytearray([0x0c]))
        if (self.mag_chip_id == QMC6983_E1_Metal or self.mag_chip_id == QMC7983_Slope ):
            self.i2c.writeto_mem(self.qmc_address, 0x1b, bytearray([0x80]))
        self.i2c.writeto_mem(self.qmc_address, 0x0b, bytearray([0x01]))
        self.i2c.writeto_mem(self.qmc_address, 0x09, bytearray([0x1d]))

    @property
    def qmc_read_xyz(self):
        read_data = self.i2c.readfrom_mem(self.qmc_address, 0x00, 6)
        #if (self.mag_chip_id >= 3)
        raw = bytearray(3)
        raw[0] = (read_data[1]<<8) | read_data[0]
        raw[1] = (read_data[3]<<8) | read_data[2]
        raw[2] = (read_data[5]<<8) | read_data[4]
        return (raw[0], raw[1], raw[2])
        # return "({:.1f}|{:.1f}|{:.1f})".format(raw[0]/25.0, raw[1]/25.0, raw[2]/25.0)
    ################## QMCX983 End ##################

    ################## BME280 ##################
    def bme280_init(self, mode=BME280_OSAMPLE_1,
                 bme_address=BME280_I2CADDR):
        # Check that mode is valid.
        if mode not in [BME280_OSAMPLE_1, BME280_OSAMPLE_2, BME280_OSAMPLE_4,
                        BME280_OSAMPLE_8, BME280_OSAMPLE_16]:
            raise ValueError(
                'Unexpected mode value {0}. Set mode to one of '
                'BME280_ULTRALOWPOWER, BME280_STANDARD, BME280_HIGHRES, or '
                'BME280_ULTRAHIGHRES'.format(mode))
        self._mode = mode
        self.bme_address = bme_address

        # load calibration data
        dig_88_a1 = self.i2c.readfrom_mem(self.bme_address, 0x88, 26)
        dig_e1_e7 = self.i2c.readfrom_mem(self.bme_address, 0xE1, 7)
        self.dig_T1, self.dig_T2, self.dig_T3, self.dig_P1, \
            self.dig_P2, self.dig_P3, self.dig_P4, self.dig_P5, \
            self.dig_P6, self.dig_P7, self.dig_P8, self.dig_P9, \
            _, self.dig_H1 = unpack("<HhhHhhhhhhhhBB", dig_88_a1)

        self.dig_H2, self.dig_H3 = unpack("<hB", dig_e1_e7)
        e4_sign = unpack_from("<b", dig_e1_e7, 3)[0]
        self.dig_H4 = (e4_sign << 4) | (dig_e1_e7[4] & 0xF)

        e6_sign = unpack_from("<b", dig_e1_e7, 5)[0]
        self.dig_H5 = (e6_sign << 4) | (dig_e1_e7[4] >> 4)

        self.dig_H6 = unpack_from("<b", dig_e1_e7, 6)[0]

        self.i2c.writeto_mem(self.bme_address, BME280_REGISTER_CONTROL,
                             bytearray([0x3F]))
        self.t_fine = 0

        # temporary data holders which stay allocated
        self._l1_barray = bytearray(1)
        self._l8_barray = bytearray(8)
        self._l3_resultarray = array("i", [0, 0, 0])

    def read_raw_data(self, result):
        """ Reads the raw (uncompensated) data from the sensor.
            Args:
                result: array of length 3 or alike where the result will be
                stored, in temperature, pressure, humidity order
            Returns:
                None
        """

        self._l1_barray[0] = self._mode
        self.i2c.writeto_mem(self.bme_address, BME280_REGISTER_CONTROL_HUM,
                             self._l1_barray)
        self._l1_barray[0] = self._mode << 5 | self._mode << 2 | 1
        self.i2c.writeto_mem(self.bme_address, BME280_REGISTER_CONTROL,
                             self._l1_barray)

        sleep_time = 1250 + 2300 * (1 << self._mode)
        sleep_time = sleep_time + 2300 * (1 << self._mode) + 575
        sleep_time = sleep_time + 2300 * (1 << self._mode) + 575
        time.sleep_us(sleep_time)  # Wait the required time

        # burst readout from 0xF7 to 0xFE, recommended by datasheet
        self.i2c.readfrom_mem_into(self.bme_address, 0xF7, self._l8_barray)
        readout = self._l8_barray
        # pressure(0xF7): ((msb << 16) | (lsb << 8) | xlsb) >> 4
        raw_press = ((readout[0] << 16) | (readout[1] << 8) | readout[2]) >> 4
        # temperature(0xFA): ((msb << 16) | (lsb << 8) | xlsb) >> 4
        raw_temp = ((readout[3] << 16) | (readout[4] << 8) | readout[5]) >> 4
        # humidity(0xFD): (msb << 8) | lsb
        raw_hum = (readout[6] << 8) | readout[7]

        result[0] = raw_temp
        result[1] = raw_press
        result[2] = raw_hum

    def read_compensated_data(self, result=None):
        """ Reads the data from the sensor and returns the compensated data.
            Args:
                result: array of length 3 or alike where the result will be
                stored, in temperature, pressure, humidity order. You may use
                this to read out the sensor without allocating heap memory
            Returns:
                array with temperature, pressure, humidity. Will be the one from
                the result parameter if not None
        """
        self.read_raw_data(self._l3_resultarray)
        raw_temp, raw_press, raw_hum = self._l3_resultarray
        # temperature
        var1 = ((raw_temp >> 3) - (self.dig_T1 << 1)) * (self.dig_T2 >> 11)
        var2 = (((((raw_temp >> 4) - self.dig_T1) *
                  ((raw_temp >> 4) - self.dig_T1)) >> 12) * self.dig_T3) >> 14
        self.t_fine = var1 + var2
        temp = (self.t_fine * 5 + 128) >> 8

        # pressure
        var1 = self.t_fine - 128000
        var2 = var1 * var1 * self.dig_P6
        var2 = var2 + ((var1 * self.dig_P5) << 17)
        var2 = var2 + (self.dig_P4 << 35)
        var1 = (((var1 * var1 * self.dig_P3) >> 8) +
                ((var1 * self.dig_P2) << 12))
        var1 = (((1 << 47) + var1) * self.dig_P1) >> 33
        if var1 == 0:
            pressure = 0
        else:
            p = 1048576 - raw_press
            p = (((p << 31) - var2) * 3125) // var1
            var1 = (self.dig_P9 * (p >> 13) * (p >> 13)) >> 25
            var2 = (self.dig_P8 * p) >> 19
            pressure = ((p + var1 + var2) >> 8) + (self.dig_P7 << 4)

        # humidity
        h = self.t_fine - 76800
        h = (((((raw_hum << 14) - (self.dig_H4 << 20) -
                (self.dig_H5 * h)) + 16384)
              >> 15) * (((((((h * self.dig_H6) >> 10) *
                            (((h * self.dig_H3) >> 11) + 32768)) >> 10) +
                          2097152) * self.dig_H2 + 8192) >> 14))
        h = h - (((((h >> 15) * (h >> 15)) >> 7) * self.dig_H1) >> 4)
        h = 0 if h < 0 else h
        h = 419430400 if h > 419430400 else h
        humidity = h >> 12

        if result:
            result[0] = temp
            result[1] = pressure
            result[2] = humidity
            return result

        return array("i", (temp, pressure, humidity))

    @property
    def bme_values(self):
        """ human readable values """

        t, p, h = self.read_compensated_data()

        p = p // 256
        pi = p // 100
        pd = p - pi * 100

        hi = h // 1024
        hd = h * 100 // 1024 - hi * 100
        return ("{}C".format(t / 100), "{}.{:02d}hPa".format(pi, pd),
                "{}.{:02d}%".format(hi, hd))
    ################## BME280 End ##################


################## SP_WEATHER Demo ##################
if __name__ == "__main__":
    from machine import I2C
    from fpioa_manager import fm
    import time

    ############# config #############
    WEATHER_I2C_NUM = I2C.I2C_SOFT
    WEATHER_I2C_FREQ_KHZ = 100
    WEATHER_I2C_SCL = 30
    WEATHER_I2C_SDA = 31
    ##################################
    
    i2c_bus = I2C(WEATHER_I2C_NUM, freq=WEATHER_I2C_FREQ_KHZ*1000, 
    scl=WEATHER_I2C_SCL, sda=WEATHER_I2C_SDA, gscl = fm.fpioa.GPIOHS1,
    gsda = fm.fpioa.GPIOHS2)
    i2c_devs_list = i2c_bus.scan()
    print("I2C devices:" + str(i2c_devs_list))

    weather=SPWEATHER(i2c=i2c_bus) # create sp_weather

    while 1:
        time.sleep_ms(500)
        print(weather.qmc_read_xyz) # QMC7983 read data
        print(weather.bme_values) # BME280 read data
