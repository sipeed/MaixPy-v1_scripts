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

############################# UDP Test ##############################
# The server must first know the client's IP and port number through the message sent by the client before it send the message to the client
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5)

while True:
    sock.sendto("Client send: hello UDP\n".encode(),addr)
    try:
        data, addr1 = sock.recvfrom(10)
        print("Recv from server: ", data)
    except Exception as e:
        pass
    time.sleep_ms(500)
sock.close()
########################### UDP Test end ############################