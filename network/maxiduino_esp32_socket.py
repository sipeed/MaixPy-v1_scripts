

import network, socket
from Maix import GPIO
from fpioa_manager import fm
from board import board_info
import time

WIFI_SSID = "Sipeed_2.4G"
WIFI_PASSWD = "xxxxxxxxx"
SERVER_ADDR = "192.168.0.113"
SERVER_PORT = 60000


# IO map for ESP32 on Maixduino
fm.register(25,fm.fpioa.GPIOHS10, force=True)#cs
fm.register(8,fm.fpioa.GPIOHS11, force=True)#rst
fm.register(9,fm.fpioa.GPIOHS12, force=True)#rdy
fm.register(28,fm.fpioa.GPIOHS13, force=True)#mosi
fm.register(26,fm.fpioa.GPIOHS14, force=True)#miso
fm.register(27,fm.fpioa.GPIOHS15, force=True)#sclk

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


sock = socket.socket()
sock.connect((SERVER_ADDR, SERVER_PORT))

sock.settimeout(5)
while 1:
    try:
        sock.send("hello\n")
        #data = sock.recv(10) # old maxipy have bug (recv timeout no return last data)
        try:
          data = b""
          while True:
            tmp = sock.recv(1)
            #print(tmp)
            if len(tmp) == 0:
                break
            data += tmp
        except Exception as e:
          print("rcv:", len(data), data)
    except Exception as e:
        print("receive error:", e)
        continue
    time.sleep(2)

sock.close()
