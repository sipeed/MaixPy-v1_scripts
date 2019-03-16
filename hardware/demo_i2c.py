from machine import I2C

i2c = I2C(I2C.I2C0, freq=100000, scl=28, sda=29)
devices = i2c.scan()
print(devices)

for device in devices:
    i2c.writeto(device, b'123')
    i2c.readfrom(device, 3)

