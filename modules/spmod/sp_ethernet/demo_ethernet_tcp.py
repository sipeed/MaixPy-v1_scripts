import network, socket, time
from machine import SPI
from Maix import GPIO
from fpioa_manager import fm

################ config ################
server_ip      = "192.168.0.141"
server_port    = 8000

WIZNET5K_SPI_SCK = 21
WIZNET5K_SPI_MOSI = 8
WIZNET5K_SPI_MISO = 15
WIZNET5K_SPI_CS = 20
#######################################

addr = (server_ip, server_port)
spi1 = SPI(4, mode=SPI.MODE_MASTER, baudrate=600 * 1000,
            polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=WIZNET5K_SPI_SCK, mosi=WIZNET5K_SPI_MOSI, miso = WIZNET5K_SPI_MISO)

#  create wiznet5k nic
nic = network.WIZNET5K(spi = spi1, cs = WIZNET5K_SPI_CS)
print("Static IP: ", nic.ifconfig())


############################## TCP Test ##############################
# The TCP server needs to be pre-started
sock = socket.socket()
sock.connect(addr)
while 1:
    sock.send("Client send: Hello TCP\n")
    try:
          data = sock.recv(10)
          print("Recv from Server: ", data)
    except Exception as e:
          print(e)
    time.sleep(500)
sock.close()
############################ TCP Test end ############################