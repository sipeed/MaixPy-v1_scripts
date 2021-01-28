# DATE: 2020-12-3
from machine import I2C
from fpioa_manager import fm
from micropython import const
import struct
import time, utime
from Maix import GPIO
import ustruct

_IO_TIMEOUT = 1000
_SYSRANGE_START = const(0x00)
_EXTSUP_HV = const(0x89)
_MSRC_CONFIG = const(0x60)
_FINAL_RATE_RTN_LIMIT = const(0x44)
_SYSTEM_SEQUENCE = const(0x01)
_SPAD_REF_START = const(0x4f)
_SPAD_ENABLES = const(0xb0)
_REF_EN_START_SELECT = const(0xb6)
_SPAD_NUM_REQUESTED = const(0x4e)
_INTERRUPT_GPIO = const(0x0a)
_INTERRUPT_CLEAR = const(0x0b)
_GPIO_MUX_ACTIVE_HIGH = const(0x84)
_RESULT_INTERRUPT_STATUS = const(0x13)
_RESULT_RANGE_STATUS = const(0x14)
_OSC_CALIBRATE = const(0xf8)
_MEASURE_PERIOD = const(0x04)

class TimeoutError(RuntimeError):
	pass

class VL53L0X:
	def __init__(self, i2c, address=0x29):
		self.i2c = i2c
		self.address = address
		self.init()
		self._started = False

	def _registers(self, register, values=None, struct='B'):
		if values is None:
			size = ustruct.calcsize(struct)
			data = self.i2c.readfrom_mem(self.address, register, size)
			values = ustruct.unpack(struct, data)
			return values
		data = ustruct.pack(struct, *values)
		self.i2c.writeto_mem(self.address, register, data)

	def _register(self, register, value=None, struct='B'):
		if value is None:
			return self._registers(register, struct=struct)[0]
		self._registers(register, (value,), struct=struct)

	def _flag(self, register=0x00, bit=0, value=None):
		data = self._register(register)
		mask = 1 << bit
		if value is None:
			return bool(data & mask)
		elif value:
			data |= mask
		else:
			data &= ~mask
		self._register(register, data)

	def _config(self, *config):
		for register, value in config:
			self._register(register, value)

	def init(self, power2v8=True):
		self._flag(_EXTSUP_HV, 0, power2v8)
		self._config(
			(0x88, 0x00),
			(0x80, 0x01),
			(0xff, 0x01),
			(0x00, 0x00),
		)
		self._stop_variable = self._register(0x91)
		self._config(
			(0x00, 0x01),
			(0xff, 0x00),
			(0x80, 0x00),
		)
		self._flag(_MSRC_CONFIG, 1, True)
		self._flag(_MSRC_CONFIG, 4, True)
		self._register(_FINAL_RATE_RTN_LIMIT, int(0.25 * (1 << 7)),
					   struct='>H')
		self._register(_SYSTEM_SEQUENCE, 0xff)
		spad_count, is_aperture = self._spad_info()
		spad_map = bytearray(self._registers(_SPAD_ENABLES, struct='6B'))
		self._config(
			(0xff, 0x01),
			(_SPAD_REF_START, 0x00),
			(_SPAD_NUM_REQUESTED, 0x2c),
			(0xff, 0x00),
			(_REF_EN_START_SELECT, 0xb4),
		)
		spads_enabled = 0
		for i in range(48):
			if i < 12 and is_aperture or spads_enabled >= spad_count:
				spad_map[i // 8] &= ~(1 << (i >> 2))
			elif spad_map[i // 8] & (1 << (i >> 2)):
				spads_enabled += 1
		self._registers(_SPAD_ENABLES, spad_map, struct='6B')
		self._config(
			(0xff, 0x01),
			(0x00, 0x00),
			(0xff, 0x00),
			(0x09, 0x00),
			(0x10, 0x00),
			(0x11, 0x00),
			(0x24, 0x01),
			(0x25, 0xFF),
			(0x75, 0x00),
			(0xFF, 0x01),
			(0x4E, 0x2C),
			(0x48, 0x00),
			(0x30, 0x20),
			(0xFF, 0x00),
			(0x30, 0x09),
			(0x54, 0x00),
			(0x31, 0x04),
			(0x32, 0x03),
			(0x40, 0x83),
			(0x46, 0x25),
			(0x60, 0x00),
			(0x27, 0x00),
			(0x50, 0x06),
			(0x51, 0x00),
			(0x52, 0x96),
			(0x56, 0x08),
			(0x57, 0x30),
			(0x61, 0x00),
			(0x62, 0x00),
			(0x64, 0x00),
			(0x65, 0x00),
			(0x66, 0xA0),
			(0xFF, 0x01),
			(0x22, 0x32),
			(0x47, 0x14),
			(0x49, 0xFF),
			(0x4A, 0x00),
			(0xFF, 0x00),
			(0x7A, 0x0A),
			(0x7B, 0x00),
			(0x78, 0x21),
			(0xFF, 0x01),
			(0x23, 0x34),
			(0x42, 0x00),
			(0x44, 0xFF),
			(0x45, 0x26),
			(0x46, 0x05),
			(0x40, 0x40),
			(0x0E, 0x06),
			(0x20, 0x1A),
			(0x43, 0x40),
			(0xFF, 0x00),
			(0x34, 0x03),
			(0x35, 0x44),
			(0xFF, 0x01),
			(0x31, 0x04),
			(0x4B, 0x09),
			(0x4C, 0x05),
			(0x4D, 0x04),
			(0xFF, 0x00),
			(0x44, 0x00),
			(0x45, 0x20),
			(0x47, 0x08),
			(0x48, 0x28),
			(0x67, 0x00),
			(0x70, 0x04),
			(0x71, 0x01),
			(0x72, 0xFE),
			(0x76, 0x00),
			(0x77, 0x00),
			(0xFF, 0x01),
			(0x0D, 0x01),
			(0xFF, 0x00),
			(0x80, 0x01),
			(0x01, 0xF8),
			(0xFF, 0x01),
			(0x8E, 0x01),
			(0x00, 0x01),
			(0xFF, 0x00),
			(0x80, 0x00),
		)
		self._register(_INTERRUPT_GPIO, 0x04)
		self._flag(_GPIO_MUX_ACTIVE_HIGH, 4, False)
		self._register(_INTERRUPT_CLEAR, 0x01)
		self._register(_SYSTEM_SEQUENCE, 0x01)
		self._calibrate(0x40)
		self._register(_SYSTEM_SEQUENCE, 0x02)
		self._calibrate(0x00)
		self._register(_SYSTEM_SEQUENCE, 0xe8)

	def _spad_info(self):
		self._config(
			(0x80, 0x01),
			(0xff, 0x01),
			(0x00, 0x00),
			(0xff, 0x06),
		)
		self._flag(0x83, 3, True)
		self._config(
			(0xff, 0x07),
			(0x81, 0x01),
			(0x80, 0x01),
			(0x94, 0x6b),
			(0x83, 0x00),
		)
		for timeout in range(_IO_TIMEOUT):
			if self._register(0x83):
				break
			utime.sleep_ms(1)
		else:
			raise TimeoutError()
		self._config(
			(0x83, 0x01),
		)
		value = self._register(0x92)
		self._config(
			(0x81, 0x00),
			(0xff, 0x06),
		)
		self._flag(0x83, 3, False)
		self._config(
			(0xff, 0x01),
			(0x00, 0x01),
			(0xff, 0x00),
			(0x80, 0x00),
		)
		count = value & 0x7f
		is_aperture = bool(value & 0b10000000)
		return count, is_aperture

	def _calibrate(self, vhv_init_byte):
		self._register(_SYSRANGE_START, 0x01 | vhv_init_byte)
		for timeout in range(_IO_TIMEOUT):
			if self._register(_RESULT_INTERRUPT_STATUS) & 0x07:
				break
			utime.sleep_ms(1)
		else:
			raise TimeoutError()
		self._register(_INTERRUPT_CLEAR, 0x01)
		self._register(_SYSRANGE_START, 0x00)

	def start(self, period=0):
		self._config(
		  (0x80, 0x01),
		  (0xFF, 0x01),
		  (0x00, 0x00),
		  (0x91, self._stop_variable),
		  (0x00, 0x01),
		  (0xFF, 0x00),
		  (0x80, 0x00),
		)
		if period:
			oscilator = self._register(_OSC_CALIBRATE, struct='>H')
			if oscilator:
				period *= oscilator
			self._register(_MEASURE_PERIOD, period, struct='>H')
			self._register(_SYSRANGE_START, 0x04)
		else:
			self._register(_SYSRANGE_START, 0x02)
		self._started = True

	def stop(self):
		self._register(_SYSRANGE_START, 0x01)
		self._config(
		  (0xFF, 0x01),
		  (0x00, 0x00),
		  (0x91, self._stop_variable),
		  (0x00, 0x01),
		  (0xFF, 0x00),
		)
		self._started = False
		
	def read(self):
		if not self._started:
			self._config(
			  (0x80, 0x01),
			  (0xFF, 0x01),
			  (0x00, 0x00),
			  (0x91, self._stop_variable),
			  (0x00, 0x01),
			  (0xFF, 0x00),
			  (0x80, 0x00),
			  (_SYSRANGE_START, 0x01),
			)
			for timeout in range(_IO_TIMEOUT):
				if not self._register(_SYSRANGE_START) & 0x01:
					break
				utime.sleep_ms(1)
			else:
				raise TimeoutError()
		for timeout in range(_IO_TIMEOUT):
			if self._register(_RESULT_INTERRUPT_STATUS) & 0x07:
				break
			utime.sleep_ms(1)
		else:
			raise TimeoutError()
		value = self._register(_RESULT_RANGE_STATUS + 10, struct='>H')
		self._register(_INTERRUPT_CLEAR, 0x01)
		return value

if __name__ == "__main__":
	################### config ###################
	VL53L0X_I2C_NUM = I2C.I2C0
	VL53L0X_FREQ = const(100000)
	VL53L0X_SCL = const(6)
	VL53L0X_SDA = const(7)
	VL53L0X_SHT = const(8)
	##############################################

	# io configure
	fm.register(VL53L0X_SHT, fm.fpioa.GPIOHS0, force=True)
	XSHUT = GPIO(GPIO.GPIOHS0, GPIO.OUT)
	XSHUT.value(1)

	# i2c init
	i2c = I2C(VL53L0X_I2C_NUM, freq=VL53L0X_FREQ, scl=VL53L0X_SCL, sda=VL53L0X_SDA)
	devices = i2c.scan()
	print(devices)

	# create obj and read distance
	tof = VL53L0X(i2c)
	while True:
		mm = tof.read()
		utime.sleep_ms(100)
		print("{}mm".format(mm))
