from machine import I2C
from fpioa_manager import fm

# i2c = I2C(I2C.I2C0, freq=100000, scl=28, sda=29) # hardware i2c
i2c = I2C(I2C.I2C3, freq=100000, scl=28, sda=29) # software i2c
#i2c = I2C(I2C.I2C_SOFT, freq=100000, scl=28, sda=29,
          #gscl = fm.fpioa.GPIOHS1, gsda = fm.fpioa.GPIOHS2) # software i2c for the latest firmware
          
devices = i2c.scan()
print(devices)

for device in devices:
    i2c.writeto(device, b'123')
    i2c.readfrom(device, 3)
    # tmp = bytearray(6)
    # i2c.readfrom_into(device, tmp, True)

