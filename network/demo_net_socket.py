import socket
import network
import gc
import os
import lcd, image
import machine
from board import board_info
from fpioa_manager import fm

fm.register(board_info.WIFI_RX, fm.fpioa.UART2_TX, force=True)
fm.register(board_info.WIFI_TX, fm.fpioa.UART2_RX, force=True)
uart = machine.UART(machine.UART.UART2, 115200,timeout=1000, read_buf_len=4096)
nic=network.ESP8285(uart)
nic.connect("Sipeed_2.4G","passwd")

sock = socket.socket()
addr = socket.getaddrinfo("dl.sipeed.com", 80)[0][-1]
sock.connect(addr)
sock.send('''GET /MAIX/MaixPy/assets/Alice.jpg HTTP/1.1
Host: dl.sipeed.com
cache-control: no-cache

''')

img = b""
sock.settimeout(5)
while True:
    data = sock.recv(4096)
    if len(data) == 0:
        break
    print("rcv:", len(data))
    img = img + data

print(len(img))
img = img[img.find(b"\r\n\r\n")+4:]
print(len(img))
print("save to /sd/Alice.jpg")
f = open("/sd/Alice.jpg","wb")
f.write(img)
f.close()
print("save ok")
print("display")
img = image.Image("/sd/Alice.jpg")
lcd.init()
lcd.display(img)

