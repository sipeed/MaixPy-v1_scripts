

import network, socket
from Maix import GPIO
from fpioa_manager import fm
from board import board_info
import time

WIFI_SSID = "webduino.io"
WIFI_PASSWD = "webduino"

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

try:
    import usocket as _socket
except:
    import _socket
try:
    import ussl as ssl
except:
    import ssl

def main(use_stream=True):
    s = _socket.socket()
    s.settimeout(1)
    host = "www.baidu.com"
    ai = _socket.getaddrinfo(host, 443)
    print("Address infos:", ai)
    addr = ai[0][-1]
    for i in range(5):
        try:
            print("Connect address:", addr)
            s.connect(addr)

            tmp = ssl.wrap_socket(s, server_hostname=host)

            tmp.write(b"GET / HTTP/1.1\r\n\r\n")
            print(tmp.readline('\r\n'))
        except Exception as e:
          print(e)

    s.close()

main()


