

# Send image(jpeg) to server and display on server(PC), 
# server code refer to ../tools_on_PC/network/pic_server.py


import network, socket, time, sensor, image
from machine import UART
from Maix import GPIO
from fpioa_manager import fm, board_info

########## config ################
WIFI_SSID = "Sipeed_2.4G"
WIFI_PASSWD = "Sipeed123."
server_ip      = "192.168.0.183"
server_port    = 3456
##################################

# IO map for ESP32 on Maixduino
fm.register(25,fm.fpioa.GPIOHS10)#cs
fm.register(8,fm.fpioa.GPIOHS11)#rst
fm.register(9,fm.fpioa.GPIOHS12)#rdy
fm.register(28,fm.fpioa.GPIOHS13)#mosi
fm.register(26,fm.fpioa.GPIOHS14)#miso
fm.register(27,fm.fpioa.GPIOHS15)#sclk

nic = network.ESP32_SPI(cs=fm.fpioa.GPIOHS10,rst=fm.fpioa.GPIOHS11,rdy=fm.fpioa.GPIOHS12, mosi=fm.fpioa.GPIOHS13,miso=fm.fpioa.GPIOHS14,sclk=fm.fpioa.GPIOHS15)

addr = (server_ip, server_port)

clock = time.clock()

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
# sensor.skip_frames(time = 2000)

nic = None
while True:
    if not nic:
        nic = network.ESP32_SPI(cs=fm.fpioa.GPIOHS10,rst=fm.fpioa.GPIOHS11,rdy=fm.fpioa.GPIOHS12, mosi=fm.fpioa.GPIOHS13,miso=fm.fpioa.GPIOHS14,sclk=fm.fpioa.GPIOHS15)
        continue
    if not nic.isconnected():
        print("connect WiFi now")
        try:
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
        except Exception:
            continue
    if not nic.isconnected():
        print("WiFi connect fail")
        continue

# send pic
    sock = socket.socket()
    print(sock)
    try:
        sock.connect(addr)
    except Exception as e:
        print("connect error:", e)
        sock.close()
        continue
    sock.settimeout(5)

    count = 0
    err   = 0
    while True:
        clock.tick()
        if err >=10:
            print("socket broken")
            break
        img = sensor.snapshot()
        lcd.display(img)
        img = img.compress(quality=20)
        img_bytes = img.to_bytes()
        try:
            send_len = sock.send(img_bytes)
            if send_len == 0:
                raise Exception("send fail")
        except OSError as e:
            if e.args[0] == 128:
                print("connection closed")
                break
        except Exception as e:
            print("send fail:", e)
            time.sleep() 
            err += 1
            continue
        count += 1
        print("send:", count)
        print("fps:", clock.fps())
    print("close now")
    sock.close()

