import socket
import network
import gc
import os
import lcd, image
import machine
from Maix import GPIO
from board import board_info
from fpioa_manager import fm

#reset ESP8285 begin
fm.register(8, fm.fpioa.GPIOHS0, force=True)
wifi_en=GPIO(GPIO.GPIOHS0, GPIO.OUT)

fm.register(0, fm.fpioa.GPIOHS1, force=True)
wifi_io0_en=GPIO(GPIO.GPIOHS1, GPIO.OUT)
wifi_io0_en.value(0)

wifi_en.value(0)  ##if ESP8285 init error ,try add ## or remove ##  this line.
time.sleep(2)
wifi_en.value(1)
time.sleep(5)
#reset ESP8285 end

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
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1

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
begin=img.find(b"\r\n\r\n")+4
img = img[begin:begin+43756]   ## jpg file size is 43756 byte
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

