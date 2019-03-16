from machine import SPI

spi1 = SPI(SPI.SPI1, mode=SPI.MODE_MASTER, baudrate=10000000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=28, mosi=29, miso=30, cs0=27)
w = b'1234'
r = bytearray(4)
spi1.write(w)
spi1.write(w, cs=SPI.CS0)
spi1.write_readinto(w, r)
spi1.read(5, write=0x00)
spi1.readinto(r, write=0x00)

