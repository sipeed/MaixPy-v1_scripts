

# Send image(jpeg) to server and display on server(PC), 
# server code refer to ../tools_on_PC/network/pic_server.py


import network, socket, time, sensor, image
from machine import UART
from Maix import GPIO
from fpioa_manager import fm, board_info

########## config ################
wifi_ap_ssid   = "Sipeed_2.4G"
wifi_ap_passwd = "Sipeed123."
server_ip      = "192.168.0.183"
server_port    = 3456
##################################

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
    uart = UART(UART.UART2,921600,timeout=1000, read_buf_len=4096)
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

addr = (server_ip, server_port)

clock = time.clock()

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

nic = None
while True:
    if not nic or not nic.isconnected():
        nic = wifi_reset()
    if not nic:
        print("wifi reset fail")
        continue
    try:
        nic.connect(wifi_ap_ssid, wifi_ap_passwd)
        nic.ifconfig()
    except Exception:
        continue
    if not nic.isconnected():
        print("WiFi connect fail")
        continue

# send pic
    sock = socket.socket()
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
        img = img.compress(quality=20)
        img_bytes = img.to_bytes()
        try:
            send_len = sock.send(img_bytes)
        except Exception:
            print("send fail")
            time.sleep(2)
            err += 1
            continue
        count += 1
        print("send:", count)
        print("fps:", clock.fps())
    sock.close()

