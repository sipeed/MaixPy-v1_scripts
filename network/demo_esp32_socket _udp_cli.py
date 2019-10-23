

import network, socket
from Maix import GPIO
from fpioa_manager import fm, board_info
import time

WIFI_SSID = "Sipeed_2.4G"
WIFI_PASSWD = "passwd"
SERVER_ADDR = "192.168.0.183"
SERVER_PORT = 8000


# IO map for ESP32 on Maixduino
fm.register(25,fm.fpioa.GPIOHS10)#cs
fm.register(8,fm.fpioa.GPIOHS11)#rst
fm.register(9,fm.fpioa.GPIOHS12)#rdy
fm.register(28,fm.fpioa.GPIOHS13)#mosi
fm.register(26,fm.fpioa.GPIOHS14)#miso
fm.register(27,fm.fpioa.GPIOHS15)#sclk

nic = network.ESP32_SPI(cs=fm.fpioa.GPIOHS10,rst=fm.fpioa.GPIOHS11,rdy=fm.fpioa.GPIOHS12, mosi=fm.fpioa.GPIOHS13,miso=fm.fpioa.GPIOHS14,sclk=fm.fpioa.GPIOHS15)

print("ESP32_SPI firmware version:", nic.version())

err = 0
while 1:
    try:
        nic.connect(WIFI_SSID, WIFI_PASSWD)
    except Exception:
        err += 1
        print("Connect AP failed, now try again")
        if err > 3:
            raise Exception("Conenct AP fail")
        continue
    break
print(nic.ifconfig())
print(nic.isconnected())


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1)
while 1:
    try:
        sock.sendto("hello\n".encode(),(SERVER_ADDR, SERVER_PORT))
        data, addr = sock.recvfrom(1024)
    except Exception as e:
        print("receive error:", e)
        continue
    print("addr:", addr, "data:", data)
    time.sleep(2)

sock.close()
