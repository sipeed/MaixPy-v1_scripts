import network, socket, time
from machine import SPI
from Maix import GPIO
from fpioa_manager import fm

################ config ################
WIZNET5K_SPI_SCK = 21
WIZNET5K_SPI_MOSI = 8
WIZNET5K_SPI_MISO = 15
WIZNET5K_SPI_CS = 20
#######################################

spi1 = SPI(4, mode=SPI.MODE_MASTER, baudrate=600 * 1000,
            polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=WIZNET5K_SPI_SCK, mosi=WIZNET5K_SPI_MOSI, miso = WIZNET5K_SPI_MISO)

#  create wiznet5k nic
nic = network.WIZNET5K(spi = spi1, cs = WIZNET5K_SPI_CS)
# get info
print("Static IP init: ", nic.ifconfig())
# set info
nic.ifconfig(('192.168.0.127', '255.255.255.0', '192.168.0.1', '8.8.8.8'))
print("Static IP after set: ", nic.ifconfig())
#dhcp: Dynamic IP acquisition, It's not necessary
while True:
    if(nic.dhclient()):
        print("DHCP IP:", nic.ifconfig() )
        break;
# check whether it is connected
print(nic.isconnected())

import socket
sock = socket.socket()
# your send or recv
# see other demo_socket_tcp.py / udp / http / mqtt
sock.close()

'''output
>>> Static IP init:  ('192.168.0.117', '255.255.255.0', '192.168.0.1', '8.8.8.8')
Static IP after set:  ('192.168.0.127', '255.255.255.0', '192.168.0.1', '8.8.8.8')
init dhcp
DHCP IP: ('192.168.0.165', '255.255.255.0', '192.168.0.1', '8.8.8.8')
True
'''
