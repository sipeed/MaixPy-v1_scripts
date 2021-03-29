from machine import I2C
import time
import ustruct

I2C_MODE = 1
SPI_MODE = 2
ENABLE_POWER = 1
DISABLE_POWER = 0
POKARITY_HIGH = 1
POKARITY_LOW = 0
ERROR = -1
SELF_TEST_XYZ_FALL = 0
SELF_TEST_YZ_FAIL = 1
SELF_TEST_XZ_FAIL = 2
SELF_TEST_Z_FAIL = 3
SELF_TEST_XY_FAIL = 4
SELF_TEST_Y_FAIL = 5
SELF_TEST_X_FAIL = 6
SELF_TEST_XYZ_OK = 7
ENABLE_DRDY = 1
DISABLE_DRDY = 0
INTERRUPUT_LATCH_ENABLE = 1
INTERRUPUT_LATCH_DISABLE = 0
MEASUREMENT_X_ENABLE = 0
MEASUREMENT_Y_ENABLE = 0
MEASUREMENT_Z_ENABLE = 0
MEASUREMENT_X_DISABLE = 1
MEASUREMENT_Y_DISABLE = 1
MEASUREMENT_Z_DISABLE = 1
DATA_OVERRUN_ENABLE = 1
DATA_OVERRUN_DISABLE = 0
OVERFLOW_INT_ENABLE = 1
OVERFLOW_INT_DISABLE = 0
LOW_INTERRUPT_X_ENABLE = 0
LOW_INTERRUPT_Y_ENABLE = 0
LOW_INTERRUPT_Z_ENABLE = 0
LOW_INTERRUPT_X_DISABLE = 1
LOW_INTERRUPT_Y_DISABLE = 1
LOW_INTERRUPT_Z_DISABLE = 1
HIGH_INTERRUPT_X_ENABLE = 0
HIGH_INTERRUPT_Y_ENABLE = 0
HIGH_INTERRUPT_Z_ENABLE = 0
HIGH_INTERRUPT_X_DISABLE = 1
HIGH_INTERRUPT_Y_DISABLE = 1
HIGH_INTERRUPT_Z_DISABLE = 1
CHANNEL_X = 1
CHANNEL_Y = 2
CHANNEL_Z = 3
ENABLE_INTERRUPT_PIN = 1
DISABLE_INTERRUPT_PIN = 0
POWERMODE_NORMAL = 0x00
POWERMODE_FORCED = 0x01
POWERMODE_SLEEP = 0x03
POWERMODE_SUSPEND = 0x04
PRESETMODE_LOWPOWER = 0x01
PRESETMODE_REGULAR = 0x02
PRESETMODE_HIGHACCURACY = 0x03
PRESETMODE_ENHANCED = 0x04
REPXY_LOWPOWER = 0x01
REPXY_REGULAR = 0x04
REPXY_ENHANCED = 0x07
REPXY_HIGHACCURACY = 0x17
REPZ_LOWPOWER = 0x01
REPZ_REGULAR = 0x07
REPZ_ENHANCED = 0x0D
REPZ_HIGHACCURACY = 0x29
CHIP_ID_VALUE = 0x32
CHIP_ID_REGISTER = 0x40
REG_DATA_X_LSB = 0x42
REG_DATA_READY_STATUS = 0x48
REG_INTERRUPT_STATUS = 0x4a
CTRL_POWER_REGISTER = 0x4b
MODE_RATE_REGISTER = 0x4c
REG_INT_CONFIG = 0x4D
REG_AXES_ENABLE = 0x4E
REG_LOW_THRESHOLD = 0x4F
REG_HIGH_THRESHOLD = 0x50
REG_REP_XY = 0x51
REG_REP_Z = 0x52
RATE_10HZ = 0x00  # (default rate)
RATE_02HZ = 0x01
RATE_06HZ = 0x02
RATE_08HZ = 0x03
RATE_15HZ = 0x04
RATE_20HZ = 0x05
RATE_25HZ = 0x06
RATE_30HZ = 0x07
DIG_X1 = 0x5D
DIG_Y1 = 0x5E
DIG_Z4_LSB = 0x62
DIG_Z4_MSB = 0x63
DIG_X2 = 0x64
DIG_Y2 = 0x65
DIG_Z2_LSB = 0x68
DIG_Z2_MSB = 0x69
DIG_Z1_LSB = 0x6A
DIG_Z1_MSB = 0x6B
DIG_XYZ1_LSB = 0x6C
DIG_XYZ1_MSB = 0x6D
DIG_Z3_LSB = 0x6E
DIG_Z3_MSB = 0x6F
DIG_XY2 = 0x70
DIG_XY1 = 0x71

BMM150_ADDR = 19


class trim_register:
    def __init__(self):
        self.dig_x1 = 0;
        self.dig_y1 = 0;
        self.dig_x2 = 0;
        self.dig_y2 = 0;
        self.dig_z1 = 0;
        self.dig_z2 = 0;
        self.dig_z3 = 0;
        self.dig_z4 = 0;
        self.dig_xy1 = 0;
        self.dig_xy2 = 0;
        self.dig_xyz1 = 0;


_trim_data = trim_register()


class geomagnetic_data:
    def __init__(self):
        self.x = 0;
        self.y = 0;
        self.z = 0;
        self.r = 0;


_geomagnetic = geomagnetic_data()


class BMM150:
    __txbuf        = [0]
    def __init__(self, i2c_dev, i2c_addr=BMM150_ADDR):
        self._offset = (0, 0, 0)
        self._scale = (1, 1, 1)
        self.i2cDev = i2c_dev
        self.bmm150Addr = i2c_addr
        scan_list = self.i2cDev.scan()
        print(scan_list)
        if self.bmm150Addr not in scan_list:
            raise Exception("Error: Unable connect pmu_bmm150!")

    '''
    @brief get chip id
    @return chip id
    '''

    def get_chip_id(self):
        rslt = self.i2cDev.readfrom_mem(self.bmm150Addr, CHIP_ID_REGISTER, 1)
        return rslt[0]

    '''
    init sensor
    return 0  is init success
           -1 is init faild
    '''

    def sensor_init(self):
        self.set_power_bit(ENABLE_POWER)
        chip_id = self.get_chip_id()
        print("chip_id:", hex(chip_id))
        if chip_id == CHIP_ID_VALUE:
            self.get_trim_data()
            return 0
        else:
            return -1

    # soft reset
    def soft_reset(self):
        rslt = self.i2cDev.readfrom_mem(self.bmm150Addr, CTRL_POWER_REGISTER, 1)
        self.__txbuf[0] = rslt[0] | 0x82
        self.i2cDev.writeto_mem(self.bmm150Addr, CTRL_POWER_REGISTER, self.__txbuf[0])

    '''
    @brief set bmm150 self test
    @retval
    SELF_TEST_XYZ_FALL               = 0
    SELF_TEST_YZ_FAIL                = 1
    SELF_TEST_XZ_FAIL                = 2
    SELF_TEST_Z_FAIL                 = 3
    SELF_TEST_XY_FAIL                = 4
    SELF_TEST_Y_FAIL                 = 5
    SELF_TEST_X_FAIL                 = 6
    SELF_TEST_XYZ_OK                 = 7
    '''

    def self_test(self):
        self.set_operation_mode(POWERMODE_SLEEP)
        rslt = self.i2cDev.readfrom_mem(self.bmm150Addr, MODE_RATE_REGISTER, 1)
        rslt1 = []
        rslt1 = self.change_date(rslt, 1)
        self.__txbuf[0] == rslt1[0] | 0x01
        self.i2cDev.writeto_mem(self.bmm150Addr, MODE_RATE_REGISTER, self.__txbuf[0])
        time.sleep(1)
        rslt = self.i2cDev.readfrom_mem(self.bmm150Addr, MODE_RATE_REGISTER, 1)
        rslt1 = []
        rslt1 = self.change_date(rslt, 1)
        if (rslt1[0] & 0x01) == 0:
            rslt = self.i2cDev.readfrom_mem(self.bmm150Addr, REG_DATA_X_LSB, 5)
            rslt1 = []
            rslt1 = self.change_date(rslt, 5)
            number = (rslt1[0] & 0x01) | (rslt1[2] & 0x01) << 1 | (rslt1[4] & 0x01) << 2
            return number
        else:
            return -1

    '''
    @brief set power bit
    @param ctrl is enable/disable power
    DISABLE_POWER is disable power
    ENABLE_POWER  is enable power
    '''

    def set_power_bit(self, ctrl):
        rslt = self.i2cDev.readfrom_mem(self.bmm150Addr, CTRL_POWER_REGISTER, 1)
        rslt1 = self.change_date(rslt, 1)
        if ctrl == DISABLE_POWER:
            self.__txbuf[0] = rslt1[0] & 0xFE
            self.i2cDev.writeto_mem(self.bmm150Addr, CTRL_POWER_REGISTER, self.__txbuf[0])
        else:
            self.__txbuf[0] = rslt1[0] | 0x01
            print("power enable", hex(self.__txbuf[0]))
            self.i2cDev.writeto_mem(self.bmm150Addr, CTRL_POWER_REGISTER, self.__txbuf[0])

    '''
    @brief get power bit
    @return power bit
      DISABLE_POWER is disable power
      ENABLE_POWER  is enable power
    '''

    def get_power_bit(self):
        rslt = self.i2cDev.readfrom_mem(self.bmm150Addr,CTRL_POWER_REGISTER, 1)
        return rslt[0] & 0x01

    '''
    @brief set opration mode
    @param modes is operation mode
    POWERMODE_NORMAL
    POWERMODE_FORCED
    POWERMODE_SLEEP
    POWERMODE_SUSPEND
    '''

    def set_operation_mode(self, modes):
        rslt = self.i2cDev.readfrom_mem(self.bmm150Addr, MODE_RATE_REGISTER, 1)
        rslt1 = []
        rslt1 = self.change_date(rslt, 1)
        if modes == POWERMODE_NORMAL:
            self.set_power_bit(ENABLE_POWER)
            rslt1[0] = rslt1[0] & 0xf9
            self.i2cDev.writeto_mem(self.bmm150Addr, MODE_RATE_REGISTER, rslt1[0])
        elif modes == POWERMODE_FORCED:
            rslt1[0] = (rslt1[0] & 0xf9) | 0x02
            self.set_power_bit(ENABLE_POWER)
            self.i2cDev.writeto_mem(self.bmm150Addr, MODE_RATE_REGISTER, rslt1[0])
        elif modes == POWERMODE_SLEEP:
            self.set_power_bit(ENABLE_POWER)
            rslt1[0] = (rslt1[0] & 0xf9) | 0x04
            self.i2cDev.writeto_mem(self.bmm150Addr, MODE_RATE_REGISTER, rslt1[0])
        else:
            self.set_power_bit(DISABLE_POWER)
        rslt = self.i2cDev.readfrom_mem(self.bmm150Addr, MODE_RATE_REGISTER, 1)

    '''
    @brief get opration mode
    @return modes is operation mode
    POWERMODE_NORMAL = 0x00
    POWERMODE_FORCED = 0x01
    POWERMODE_SLEEP = 0x03
    POWERMODE_SUSPEND = 0x04
    '''

    def get_operation_mode(self):
        if self.get_power_bit() == 0:
            return POWERMODE_SUSPEND
        else:
            rslt = self.i2cDev.readfrom_mem(self.bmm150Addr, MODE_RATE_REGISTER, 1)
            rslt1 = self.change_date(rslt, 1)
            return hex((rslt1[0] & 0x03))

    '''
    @brief set rate
    @param rate
      RATE_10HZ        #(default rate)
      RATE_02HZ
      RATE_06HZ
      RATE_08HZ
      RATE_15HZ
      RATE_20HZ
      RATE_25HZ
      RATE_30HZ
    '''

    def set_rate(self, rates):
        rslt = self.i2cDev.readfrom_mem(self.bmm150Addr, MODE_RATE_REGISTER, 1)
        rslt1 = []
        rslt1 = self.change_date(rslt, 1)
        if rates == RATE_10HZ:
            rslt1[0] = rslt1[0] & 0xc7
            self.i2cDev.writeto_mem(self.bmm150Addr, MODE_RATE_REGISTER, rslt1[0])
        elif rates == RATE_02HZ:
            rslt1[0] = (rslt1[0] & 0xc7) | 0x08
            self.i2cDev.writeto_mem(self.bmm150Addr, MODE_RATE_REGISTER, rslt1[0])
        elif rates == RATE_06HZ:
            rslt1[0] = (rslt1[0] & 0xc7) | 0x10
            self.i2cDev.writeto_mem(self.bmm150Addr, MODE_RATE_REGISTER, rslt1[0])
        elif rates == RATE_08HZ:
            rslt1[0] = (rslt1[0] & 0xc7) | 0x18
            self.i2cDev.writeto_mem(self.bmm150Addr, MODE_RATE_REGISTER, rslt1[0])
        elif rates == RATE_15HZ:
            rslt1[0] = (rslt1[0] & 0xc7) | 0x20
            self.i2cDev.writeto_mem(self.bmm150Addr, MODE_RATE_REGISTER, rslt1[0])
        elif rates == RATE_20HZ:
            rslt1[0] = (rslt1[0] & 0xc7) | 0x28
            self.i2cDev.writeto_mem(self.bmm150Addr, MODE_RATE_REGISTER, rslt1[0])
        elif rates == RATE_25HZ:
            rslt1[0] = (rslt1[0] & 0xc7) | 0x30
            self.i2cDev.writeto_mem(self.bmm150Addr, MODE_RATE_REGISTER, rslt1[0])
        elif rates == RATE_30HZ:
            rslt1[0] = (rslt1[0] & 0xc7) | 0x38
            self.i2cDev.writeto_mem(self.bmm150Addr, MODE_RATE_REGISTER, rslt1[0])
        else:
            rslt1[0] = rslt1[0] & 0xc7
            self.i2cDev.writeto_mem(self.bmm150Addr, MODE_RATE_REGISTER, rslt1[0])

    '''
   @brief get rates
   @return rates
     RATE_10HZ        #(default rate)
     RATE_02HZ
     RATE_06HZ
     RATE_08HZ
     RATE_15HZ
     RATE_20HZ
     RATE_25HZ
     RATE_30HZ
     '''

    def get_rate(self):
        rslt = self.i2cDev.readfrom_mem(self.bmm150Addr, MODE_RATE_REGISTER, 1)
        return (rslt[0] & 0x38) >> 3


    '''
    @brief set preset mode
    @param modes
    PRESETMODE_LOWPOWER
    PRESETMODE_REGULAR
    PRESETMODE_HIGHACCURACY
    PRESETMODE_ENHANCED
    '''

    def set_preset_mode(self, modes):
        if modes == PRESETMODE_LOWPOWER:
            self.set_rate(RATE_10HZ)
            self.set_xy_rep(REPXY_LOWPOWER)
            self.set_z_rep(REPZ_LOWPOWER)
        elif modes == PRESETMODE_REGULAR:
            self.set_rate(RATE_10HZ)
            self.set_xy_rep(REPXY_REGULAR)
            self.set_z_rep(REPZ_REGULAR)
        elif modes == PRESETMODE_HIGHACCURACY:
            self.set_rate(RATE_20HZ)
            self.set_xy_rep(REPXY_HIGHACCURACY)
            self.set_z_rep(REPZ_HIGHACCURACY)
        elif modes == PRESETMODE_ENHANCED:
            self.set_rate(RATE_10HZ)
            self.set_xy_rep(REPXY_ENHANCED)
            self.set_z_rep(REPZ_ENHANCED)
        else:
            self.set_rate(RATE_10HZ)
            self.set_xy_rep(REPXY_LOWPOWER)
            self.set_z_rep(REPZ_LOWPOWER)



    '''
    @brief set xy rep
    @param modes
    REPXY_LOWPOWER
    REPXY_REGULAR
    REPXY_ENHANCED
    REPXY_HIGHACCURACY
    '''


    def set_xy_rep(self, modes):
        self.__txbuf[0] = modes
        if modes == REPXY_LOWPOWER:
            self.i2cDev.writeto_mem(self.bmm150Addr,REG_REP_XY, self.__txbuf[0])
        elif modes == REPXY_REGULAR:
            self.i2cDev.writeto_mem(self.bmm150Addr,REG_REP_XY, self.__txbuf[0])
        elif modes == REPXY_ENHANCED:
            self.i2cDev.writeto_mem(self.bmm150Addr,REG_REP_XY, self.__txbuf[0])
        elif modes == REPXY_HIGHACCURACY:
            self.i2cDev.writeto_mem(self.bmm150Addr,REG_REP_XY, self.__txbuf[0])
        else:
            __txbuf[0] = REPXY_LOWPOWER####################################
            self.i2cDev.writeto_mem(self.bmm150Addr,REG_REP_XY, self.__txbuf[0])


    '''
    @brief set z rep
    @param modes
    REPZ_LOWPOWER
    REPZ_REGULAR
    REPZ_ENHANCED
    REPZ_HIGHACCURACY
    '''


    def set_z_rep(self, modes):
        self.__txbuf[0] = modes
        if modes == REPZ_LOWPOWER:
            self.i2cDev.writeto_mem(self.bmm150Addr,REG_REP_Z, self.__txbuf[0])
        elif modes == REPZ_REGULAR:
            self.i2cDev.writeto_mem(self.bmm150Addr,REG_REP_Z, self.__txbuf[0])
        elif modes == REPZ_ENHANCED:
            self.i2cDev.writeto_mem(self.bmm150Addr,REG_REP_Z, self.__txbuf[0])
        elif modes == REPZ_HIGHACCURACY:
            self.i2cDev.writeto_mem(self.bmm150Addr,REG_REP_Z, self.__txbuf[0])
        else:
            __txbuf[0] = REPZ_LOWPOWER ####################################
            self.i2cDev.writeto_mem(self.bmm150Addr,REG_REP_Z, self.__txbuf[0])


    '''
    @brief get trim data
    '''


    def get_trim_data(self):
        trim_x1_y1 = self.i2cDev.readfrom_mem( self.bmm150Addr,DIG_X1, 2)
        trim_xyz_data = self.i2cDev.readfrom_mem( self.bmm150Addr,DIG_Z4_LSB, 4)
        trim_xy1_xy2 = self.i2cDev.readfrom_mem( self.bmm150Addr,DIG_Z2_LSB, 10)
        _trim_data.dig_x1 = self.uint8_to_int8(trim_x1_y1[0])
        _trim_data.dig_y1 = self.uint8_to_int8(trim_x1_y1[1])
        _trim_data.dig_x2 = self.uint8_to_int8(trim_xyz_data[2])
        _trim_data.dig_y2 = self.uint8_to_int8(trim_xyz_data[3])
        temp_msb = int(trim_xy1_xy2[3]) << 8
        _trim_data.dig_z1 = int(temp_msb | trim_xy1_xy2[2])
        temp_msb = int(trim_xy1_xy2[1] << 8)
        _trim_data.dig_z2 = int(temp_msb | trim_xy1_xy2[0])
        temp_msb = int(trim_xy1_xy2[7] << 8)
        _trim_data.dig_z3 = temp_msb | trim_xy1_xy2[6]
        temp_msb = int(trim_xyz_data[1] << 8)
        _trim_data.dig_z4 = int(temp_msb | trim_xyz_data[0])
        _trim_data.dig_xy1 = trim_xy1_xy2[9]
        _trim_data.dig_xy2 = self.uint8_to_int8(trim_xy1_xy2[8])
        temp_msb = int((trim_xy1_xy2[5] & 0x7F) << 8)
        _trim_data.dig_xyz1 = int(temp_msb | trim_xy1_xy2[4])


    '''
    @brief get geomagnetic
    '''


    def get_geomagnetic(self):
        rslt = self.i2cDev.readfrom_mem(self.bmm150Addr,REG_DATA_X_LSB, 8)
        # rslt = self.change_date(rslt, 8)
        rslt1 = ustruct.unpack("bbbbbbbb", rslt)
        _geomagnetic.x = ((rslt1[0] & 0xF8) >> 3) | (rslt1[1] << 5)
        _geomagnetic.y = ((rslt1[2] & 0xF8) >> 3) | (rslt1[3] << 5)
        _geomagnetic.z = ((rslt1[4] & 0xFE) >> 1) | (rslt1[5] << 7)
        _geomagnetic.r = ((rslt1[6] & 0xFC) >> 2) | (rslt1[7] << 6)
        rslt2 = [rslt1[0],rslt1[1],rslt1[2]]
        rslt2[0] = self.compenstate_x(_geomagnetic.x, _geomagnetic.r)
        rslt2[1] = self.compenstate_y(_geomagnetic.y, _geomagnetic.r)
        rslt2[2] = self.compenstate_z(_geomagnetic.z, _geomagnetic.r)
        return rslt2


    '''
    @brief uint8_t to int8_t
    '''


    def uint8_to_int8(self, number):
        if number <= 127:
            return number
        else:
            return (256 - number) * -1


    '''
    @berif compenstate_x
    '''


    def compenstate_x(self, data_x, data_r):
        if data_x != -4096:
            if data_r != 0:
                process_comp_x0 = data_r
            elif _trim_data.dig_xyz1 != 0:
                process_comp_x0 = _trim_data.dig_xyz1
            else:
                process_comp_x0 = 0
            if process_comp_x0 != 0:
                process_comp_x1 = int(_trim_data.dig_xyz1 * 16384)
                process_comp_x2 = int(process_comp_x1 / process_comp_x0 - 0x4000)
                retval = process_comp_x2
                process_comp_x3 = retval * retval
                process_comp_x4 = _trim_data.dig_xy2 * (process_comp_x3 / 128)
                process_comp_x5 = _trim_data.dig_xy1 * 128
                process_comp_x6 = retval * process_comp_x5
                process_comp_x7 = (process_comp_x4 + process_comp_x6) / 512 + 0x100000
                process_comp_x8 = _trim_data.dig_x2 + 0xA0
                process_comp_x9 = (process_comp_x8 * process_comp_x7) / 4096
                process_comp_x10 = data_x * process_comp_x9
                retval = process_comp_x10 / 8192
                retval = (retval + _trim_data.dig_x1 * 8) / 16
            else:
                retval = -32368
        else:
            retval = -32768
        return retval


    '''
    @berif compenstate_
    '''


    def compenstate_y(self, data_y, data_r):
        if data_y != -4096:
            if data_r != 0:
                process_comp_y0 = data_r
            elif _trim_data.dig_xyz1 != 0:
                process_comp_y0 = _trim_data.dig_xyz1
            else:
                process_comp_y0 = 0
            if process_comp_y0 != 0:
                process_comp_y1 = int(_trim_data.dig_xyz1 * 16384 / process_comp_y0)
                process_comp_y2 = int(process_comp_y1 - 0x4000)
                retval = process_comp_y2
                process_comp_y3 = retval * retval
                process_comp_y4 = _trim_data.dig_xy2 * (process_comp_y3 / 128)
                process_comp_y5 = _trim_data.dig_xy1 * 128
                process_comp_y6 = (process_comp_y4 + process_comp_y5 * retval) / 512
                process_comp_y7 = _trim_data.dig_y2 + 0xA0
                process_comp_y8 = ((process_comp_y6 + 0x100000) * process_comp_y7) / 4096
                process_comp_y9 = data_y * process_comp_y8
                retval = process_comp_y9 / 8192
                retval = (retval + _trim_data.dig_y1 * 8) / 16
            else:
                retval = -32368
        else:
            retval = -32768
        return retval


    '''
    @berif compenstate_x
    '''


    def compenstate_z(self, data_z, data_r):
        if data_z != -16348:
            if _trim_data.dig_z2 != 0 and _trim_data.dig_z1 != 0 and _trim_data.dig_xyz1 != 0 and data_r != 0:
                process_comp_z0 = data_r - _trim_data.dig_xyz1
                process_comp_z1 = (_trim_data.dig_z3 * process_comp_z0) / 4
                process_comp_z2 = (data_z - _trim_data.dig_z4) * 32768
                process_comp_z3 = _trim_data.dig_z1 * data_r * 2
                process_comp_z4 = (process_comp_z3 + 32768) / 65536
                retval = (process_comp_z2 - process_comp_z1) / (_trim_data.dig_z2 + process_comp_z4)
                if retval > 32767:
                    retval = 32367
                elif retval < -32367:
                    retval = -32367
                retval = retval / 16
            else:
                retval = -32768
        else:
            retval = -32768
        return retval


    '''
    @brief Enable or disable the data readly mode pin, configure the polarity of the data ready mode pin
    @param modes Enable or disable the pin :
        enable   : ENABLE_DRDY
        disable  : DISABLE_DRDY  (default mode)
    @param polarity  Active level
        high     : POKARITY_HIGH  (default active high level )
        low      : POKARITY_LOW
    '''


    def set_data_readly_interrupt_pin(self, modes, polarity):
        rslt = self.i2cDev.readfrom_mem(self.bmm150Addr,REG_INT_CONFIG, 1)
        if modes == DISABLE_DRDY:
            self.__txbuf[0] = rslt[0] & 0x7F
        else:
            self.__txbuf[0] = rslt[0] | 0x80
        if polarity == POKARITY_LOW:
            self.__txbuf[0] = self.__txbuf[0] & 0xFB
        else:
            self.__txbuf[0] = self.__txbuf[0] | 0x04
        self.i2cDev.writeto_mem(self.bmm150Addr,REG_INT_CONFIG, self.__txbuf[0])


    '''
    @brief Get data ready status
    @return status  data readly status
    1 is   data is ready
    0 is   data is not ready
    '''


    def get_data_readly_state(self):
        rslt = self.i2cDev.readfrom_mem(self.bmm150Addr, REG_DATA_READY_STATUS, 1)
        return (rslt[0] & 0x01)


    '''
      @brief set measurement xyz
      @param channel_x  channel x selection:
        MEASUREMENT_X_ENABLE  (Default x-axis channel enabled)
        MEASUREMENT_X_DISABLE
      @param channel_y  channel y selection:
        MEASUREMENT_Y_ENABLE  (Default y-axis channel enabled)
        MEASUREMENT_Y_DISABLE
      @param channel_z  channel z selection:
        MEASUREMENT_Z_ENABLE  (Default z-axis channel enabled)
        MEASUREMENT_Z_DISABLE
    '''


    def set_measurement_xyz(self, channel_x, channel_y, channel_z):
        rslt = self.i2cDev.readfrom_mem(self.bmm150Addr, REG_AXES_ENABLE, 1)

        if channel_x == MEASUREMENT_X_DISABLE:
            self.__txbuf[0] = rslt[0] | 0x08
        else:
            self.__txbuf[0] = rslt[0] & 0xF7

        if channel_y == MEASUREMENT_Y_DISABLE:
            self.__txbuf[0] = self.__txbuf[0] | 0x10
        else:
            self.__txbuf[0] = self.__txbuf[0] & 0xEF

        if channel_z == MEASUREMENT_Z_DISABLE:
            self.__txbuf[0] = self.__txbuf[0] | 0x20
        else:
            self.__txbuf[0] = self.__txbuf[0] & 0xDF
        self.i2cDev.writeto_mem(self.bmm150Addr, REG_AXES_ENABLE, self.__txbuf[0])


    '''
      @brief get measurement xyz
      @param channel  channel ? selection:
        CHANNEL_X
        CHANNEL_Y
        CHANNEL_Z
      @return
        1 is  enable measurement
        0 is  disable measurement
    '''


    def get_measurement_state_xyz(self, channel):
        rslt = self.i2cDev.readfrom_mem(self.bmm150Addr,REG_AXES_ENABLE, 1)
        if channel == CHANNEL_X:
            if (rslt[0] & 0x08) == 0:
                return 1
        elif channel == CHANNEL_Y:
            if (rslt[0] & 0x10) == 0:
                return 1
        elif channel == CHANNEL_Z:
            if (rslt[0] & 0x20) == 0:
                return 1
        else:
            return 0
        return 0


    '''
      @brief Enable or disable the interrupt pin, configure the polarity of the interrupt pin
      @param modes Enable or disable the pin :
        enable   : ENABLE_INTERRUPT_PIN
        disable  : DISABLE_INTERRUPT_PIN  (default mode)
      @param polarity  Active level
        high     : POKARITY_HIGH  (default active high level )
        low      : POKARITY_LOW
    '''


    def set_interrupt_pin(self, modes, polarity):
        rslt = self.i2cDev.readfrom_mem(self.bmm150Addr,REG_AXES_ENABLE, 1)
        if modes == DISABLE_INTERRUPT_PIN:
            self.__txbuf[0] = rslt[0] & 0xBF
        else:
            self.__txbuf[0] = rslt[0] | 0x40
        if polarity == POKARITY_LOW:
            self.__txbuf[0] = self.__txbuf[0] & 0xFE
        else:
            self.__txbuf[0] = self.__txbuf[0] | 0x01
        self.i2cDev.writeto_mem(self.bmm150Addr,REG_AXES_ENABLE, self.__txbuf[0])


    '''
      @brief Set interrupt latch mode
        After the latch is enabled, only the data in the 0x4A register will be refreshed.
        No latch, data is refreshed in real time.
      @param modes  Latched or not latched
        latch    : INTERRUPUT_LATCH_ENABLE  (dafault interrupt latch)
        no latch : INTERRUPUT_LATCH_DISABLE
    '''


    def set_interruput_latch(self, modes):
        rslt = self.i2cDev.readfrom_mem(self.bmm150Addr,REG_AXES_ENABLE, 1)
        if modes == INTERRUPUT_LATCH_DISABLE:
            self.__txbuf[0] = rslt[0] & 0xFD
        else:
            self.__txbuf[0] = rslt[0] | 0x02
        self.i2cDev.writeto_mem(self.bmm150Addr,REG_AXES_ENABLE, self.__txbuf[0])


    '''
      @brief Set the channel and value of the low threshold interrupt
      @param channelX  channel x selection:
        enable x  : LOW_INTERRUPT_X_ENABLE
        disable x : LOW_INTERRUPT_X_DISABLE
      @param channelY  channel y selection:
        enable y  : LOW_INTERRUPT_Y_ENABLE
        disable y : LOW_INTERRUPT_Y_DISABLE
      @param channelZ  channel z selection:
        enable z  : LOW_INTERRUPT_Z_ENABLE
        disable z : LOW_INTERRUPT_Z_DISABLE
      @param  low_threshold is low threshold
    '''


    def set_low_threshold_interrupt(self, channel_x, channel_y, channel_z, low_threshold):
        if low_threshold < 0:
            self.__txbuf[0] = (low_threshold * -1) | 0x80
        else:
            self.__txbuf[0] = low_threshold
        self.i2cDev.writeto_mem(self.bmm150Addr,REG_LOW_THRESHOLD, self.__txbuf[0])
        rslt = self.i2cDev.readfrom_mem(self.bmm150Addr,REG_INT_CONFIG, 1)
        if channel_x == LOW_INTERRUPT_X_DISABLE:
            self.__txbuf[0] = rslt[0] | 0x01
            #print(self.__txbuf[0])
        else:
            self.__txbuf[0] = rslt[0] & 0xFE
           # print(self.__txbuf[0])
        if channel_y == LOW_INTERRUPT_Y_DISABLE:
            self.__txbuf[0] = self.__txbuf[0] | 0x02
            #print(self.__txbuf[0])
        else:
            self.__txbuf[0] = self.__txbuf[0] & 0xFC
           # print(self.__txbuf[0])
        if channel_x == LOW_INTERRUPT_X_DISABLE:
            self.__txbuf[0] = self.__txbuf[0] | 0x04
            #print(self.__txbuf[0])
        else:
            self.__txbuf[0] = self.__txbuf[0] & 0xFB
          #  print(self.__txbuf[0])
        self.i2cDev.writeto_mem(self.bmm150Addr,REG_INT_CONFIG, self.__txbuf[0])
       # print(self.__txbuf[0])
        self.set_interrupt_pin(ENABLE_INTERRUPT_PIN, POKARITY_HIGH)
        self.get_geomagnetic()



    '''
      @brief  Get the channel low threshold Interrupt status
      @return status  interrupt status
         1-7 is  interrupt
         0 is  no interrupt
    '''


    def get_low_threshold_interrupt_state(self):
        rslt = self.i2cDev.readfrom_mem(self.bmm150Addr,REG_INTERRUPT_STATUS, 1)
       # print(rslt[0])
        return rslt[0] & 0x07


    '''
      @brief Set the channel and value of the high threshold interrupt
      @param channelX  channel x selection:
        enable x  : HIGH_INTERRUPT_X_ENABLE
        disable x : HIGH_INTERRUPT_X_DISABLE
      @param channelY  channel y selection:
        enable y  : HIGH_INTERRUPT_Y_ENABLE
        disable y : HIGH_INTERRUPT_Y_DISABLE
      @param channelZ  channel z selection:
        enable z  : HIGH_INTERRUPT_Z_ENABLE
        disable z : HIGH_INTERRUPT_Z_DISABLE
      @param  high_threshold is high threshold
    '''


    def set_high_threshold_interrupt(self, channel_x, channel_y, channel_z, high_threshold):
        if high_threshold < 0:
            self.__txbuf[0] = (high_threshold * -1) | 0x80
        else:
            self.__txbuf[0] = high_threshold
        self.i2cDev.writeto_mem(self.bmm150Addr,REG_HIGH_THRESHOLD, self.__txbuf[0])
        rslt = self.i2cDev.readfrom_mem(self.bmm150Addr, REG_INT_CONFIG, 1)
        if channel_x == HIGH_INTERRUPT_X_DISABLE:
            self.__txbuf[0] = rslt[0] | 0x08
        else:
            self.__txbuf[0] = rslt[0] & 0xF7
        if channel_y == HIGH_INTERRUPT_Y_DISABLE:
            self.__txbuf[0] = self.__txbuf[0] | 0x10
        else:
            self.__txbuf[0] = self.__txbuf[0] & 0xEF
        if channel_x == HIGH_INTERRUPT_X_DISABLE:
            self.__txbuf[0] = self.__txbuf[0] | 0x20
        else:
            self.__txbuf[0] = self.__txbuf[0] & 0xDf

        self.i2cDev.writeto_mem(self.bmm150Addr,REG_INT_CONFIG, self.__txbuf)
        self.set_interrupt_pin(ENABLE_INTERRUPT_PIN, POKARITY_HIGH)
        self.get_geomagnetic()


    '''
      @brief  Get the channel low threshold Interrupt status
      @return status  interrupt status
         1-7 is  interrupt
         0 is  no interrupt
    '''


    def get_high_threshold_interrupt_state(self):
        rslt = self.i2cDev.readfrom_mem(self.bmm150Addr,REG_INTERRUPT_STATUS, 1)
        return (rslt[0] & 0x38) >> 3

    def change_date(self, rslt, num):
        rslt_change = []
        for i in range(num):
            rslt_change.append(rslt[i])
        return rslt_change

    def calibrate(self, count=256, delay=200):

        reading = self.get_geomagnetic()
        minx = maxx = reading[0]
        miny = maxy = reading[1]
        minz = maxz = reading[2]

        while count:
			time.sleep_ms(delay)
			reading = self.get_geomagnetic()
			minx = min(minx, reading[0])
			maxx = max(maxx, reading[0])
			miny = min(miny, reading[1])
			maxy = max(maxy, reading[1])
			minz = min(minz, reading[2])
			maxz = max(maxz, reading[2])
			count -= 1

        # Hard iron correction
        offset_x = (maxx + minx) / 2
        offset_y = (maxy + miny) / 2
        offset_z = (maxz + minz) / 2

        self._offset = (offset_x, offset_y, offset_z)

        # Soft iron correction
        avg_delta_x = (maxx - minx) / 2
        avg_delta_y = (maxy - miny) / 2
        avg_delta_z = (maxz - minz) / 2

        avg_delta = (avg_delta_x + avg_delta_y + avg_delta_z) / 3

        scale_x = avg_delta / avg_delta_x
        scale_y = avg_delta / avg_delta_y
        if avg_delta_z == 0:
            avg_delta_z=1
        scale_z = avg_delta / avg_delta_z

        self._scale = (scale_x, scale_y, scale_z)

        return self._offset, self._scale

def setup():
    global bmm150
    while ERROR == bmm150.sensor_init():
        print("sensor init error ,please check connect")
    '''
        POWERMODE_NORMAL
        POWERMODE_FORCED
        POWERMODE_SLEEP
        POWERMODE_SUSPEND
    '''
    bmm150.set_operation_mode(POWERMODE_NORMAL)

    '''
        PRESETMODE_LOWPOWER
        PRESETMODE_REGULAR
        PRESETMODE_HIGHACCURACY
        PRESETMODE_ENHANCED
    '''
    bmm150.set_preset_mode(PRESETMODE_LOWPOWER)

    '''
        Enable or disable the pin :
        ENABLE_DRDY
        DISABLE_DRDY  (default mode)

        polarity  Active level
        POKARITY_HIGH  (default active high level )
        POKARITY_LOW
    '''
    bmm150.set_data_readly_interrupt_pin(ENABLE_DRDY ,POKARITY_HIGH)

    # bmm150.calibrate(200, 200)

def loop():
    global bmm150, img
    if bmm150.get_data_readly_state() == 1:
        rslt = bmm150.get_geomagnetic()
        print("mag x = %d ut"%rslt[0])
        print("mag y = %d ut"%rslt[1])
        print("mag z = %d ut"%rslt[2])
        print("")
        color = (0, 255, 0)
        if rslt[0] > 100 or rslt[1] > 100 or rslt[2] > 100:
            color = (255, 0, 0)
        img.clear()
        img.draw_rectangle(0, 0 , img.width(), img.height(), color, fill=True)
        img.draw_string(10, 10, "mag x = %d ut"%rslt[0], scale=2)
        img.draw_string(10, 40, "mag y = %d ut"%rslt[1], scale=2)
        img.draw_string(10, 70, "mag z = %d ut"%rslt[2], scale=2)
        lcd.display(img)
    else:
        time.sleep(0.2)
    time.sleep(0.2)

	

if __name__ == "__main__":
    import lcd, image
    lcd.init()
    img = image.Image(size=(320, 240))
    tmp = I2C(I2C.I2C0, freq = 100*1000, scl = 28, sda = 22)
    print(tmp.scan())
    bmm150 = BMM150(tmp, 0x13)

    setup()
    while True:
        loop()


