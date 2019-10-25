import socket, network, time
import lcd, image
from Maix import GPIO
from machine import UART
from fpioa_manager import fm, board_info

WIFI_ESP32 = 1
WIFI_SSID = "Sipeed_2.4G"
WIFI_PASSWD = "Sipeed123."


if WIFI_ESP32 == 0:
    # for new MaixGO board, if not, remove it
    fm.register(0, fm.fpioa.GPIOHS1, force=True)
    wifi_io0_en=GPIO(GPIO.GPIOHS1, GPIO.OUT)
    wifi_io0_en.value(0)

    # En SEP8285
    fm.register(8, fm.fpioa.GPIOHS0, force=True)
    wifi_en=GPIO(GPIO.GPIOHS0,GPIO.OUT)
    fm.register(board_info.WIFI_RX,fm.fpioa.UART2_TX, force=True)
    fm.register(board_info.WIFI_TX,fm.fpioa.UART2_RX, force=True)

    def wifi_enable(en):
        global wifi_en
        wifi_en.value(en)

    def wifi_reset():
        global uart
        wifi_enable(0)
        time.sleep_ms(200)
        wifi_enable(1)
        time.sleep(2)
        uart = UART(UART.UART2,115200,timeout=1000, read_buf_len=4096)
        tmp = uart.read()
        uart.write("AT+UART_CUR=921600,8,1,0,0\r\n")
        print(uart.read())
        uart = UART(UART.UART2,921600,timeout=1000, read_buf_len=10240) # important! baudrate too low or read_buf_len too small will loose data
        uart.write("AT\r\n")
        tmp = uart.read()
        print(tmp)
        if not tmp.endswith("OK\r\n"):
            print("reset fail")
            return None
        try:
            nic = network.ESP8285(uart)
        except Exception:
            return None
        return nic

    nic = wifi_reset()
    if not nic:
        raise Exception("WiFi init fail")
else:
    fm.register(25,fm.fpioa.GPIOHS10)#cs
    fm.register(8,fm.fpioa.GPIOHS11)#rst
    fm.register(9,fm.fpioa.GPIOHS12)#rdy
    fm.register(28,fm.fpioa.GPIOHS13)#mosi
    fm.register(26,fm.fpioa.GPIOHS14)#miso
    fm.register(27,fm.fpioa.GPIOHS15)#sclk

    nic = network.ESP32_SPI(cs=fm.fpioa.GPIOHS10,rst=fm.fpioa.GPIOHS11,rdy=fm.fpioa.GPIOHS12, mosi=fm.fpioa.GPIOHS13,miso=fm.fpioa.GPIOHS14,sclk=fm.fpioa.GPIOHS15)

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

nic.ifconfig()

err = 0
sock = socket.socket()
while 1:
    try:
        addr = socket.getaddrinfo("dl.sipeed.com", 80)[0][-1]
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
    if len(data) == 0:
        break
    print("rcv:", len(data))
    img = img + data

sock.close()

print("rcv len:", len(img))
begin=img.find(b"\r\n\r\n")+4
img = img[begin:begin+43756]   ## jpg file size is 43756 byte
if len(img) != 43756:
    raise Exception("recv jpg not complete, try again")
print("image len:", len(img))

import image, lcd

img = image.Image(img, from_bytes=True)
lcd.init()
lcd.display(img)
del img


# print("save to /flash/Alice.jpg")
# f = open("/flash/Alice.jpg","wb")
# f.write(img)
# f.close()
# del img
# print("save ok")
# print("display")
# img = image.Image("/flash/Alice.jpg")
# lcd.init()
# lcd.display(img)
# del img

