

import network, socket
from Maix import GPIO
from fpioa_manager import fm, board_info
import time

WIFI_SSID = "Sipeed_2.4G"
WIFI_PASSWD = "passwd"

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

err = 0
sock = socket.socket()
while 1:
    try:
        addr = socket.getaddrinfo("dl.sipeed.com", 80)[0][-1]
        # addr = socket.getaddrinfo("192.168.0.183", 8099)[0][-1]
        break
    except Exception:
        err += 1
    if err > 5:
        raise Exception("get ip failed!")
sock.connect(addr)
sock.send('''GET /MAIX/MaixPy/assets/Alice.jpg HTTP/1.1
Host: dl.sipeed.com
cache-control: no-cache
User-Agent: MaixPy
Connection: close

''')

img = b""
sock.settimeout(5)
while True:
    data = sock.recv(4096)
    if len(data) == 0: # connection closed
        break
    print("rcv:", len(data))
    img = img + data

sock.close()

print("rcv len:", len(img))
begin=img.find(b"\r\n\r\n")+4
print(begin)
img = img[begin:begin+43756]   ## jpg file size is 43756 byte
if len(img) != 43756:
    raise Exception("recv jpg not complete, try again")
print("image len:", len(img))

import image, lcd

img = image.Image(img, from_bytes=True)
lcd.init()
lcd.display(img)
del img


