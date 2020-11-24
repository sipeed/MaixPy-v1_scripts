# This file is part of MaixPY
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

# Uasge see readme.md
# from network_esp32 import wifi
# from network_esp8285 import wifi
# from network_w5k import wlan

SSID = "Sipeed_2.4G"
PASW = "Sipeed123."

def enable_esp32():
    if wifi.isconnected() == False:
        for i in range(5):
            try:
                # Running within 3 seconds of power-up can cause an SD load error
                # wifi.reset(is_hard=False) 
                wifi.reset(is_hard=True)
                print('try AT connect wifi...')
                wifi.connect(SSID, PASW)
                if wifi.isconnected():
                    break
            except Exception as e:
                print(e)
    print('network state:', wifi.isconnected(), wifi.ifconfig())

enable_esp32()

########## server config ################
# Send image(jpeg) to server and display on server(PC),
# server code refer to ../demo_recv_pic_server.py
WIFI_SSID   = "Sipeed_2.4G"
WIFI_PASSWD = "Sipeed123."
addr        = ("192.168.0.107", 3456)
##################################

import socket, time, sensor, image
import lcd

clock = time.clock()
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

while True:
    # send pic
    while True:
        try:
            sock = socket.socket()
            print(sock)
            sock.connect(addr)
            break
        except Exception as e:
            print("connect error:", e)
            sock.close()
            continue
    sock.settimeout(5)

    send_len, count, err = 0, 0, 0
    while True:
        clock.tick()
        if err >=10:
            print("socket broken")
            break
        img = sensor.snapshot()
        lcd.display(img)
        img = img.compress(quality=60)
        img_bytes = img.to_bytes()
        print("send len: ", len(img_bytes))
        try:
            block = int(len(img_bytes)/2048)
            for i in range(block):
                send_len = sock.send(img_bytes[i*2048:(i+1)*2048])
                #time.sleep_ms(500)
            send_len2 = sock.send(img_bytes[block*2048:])
            #send_len = sock.send(img_bytes[0:2048])
            #send_len = sock.send(img_bytes[2048:])
            #time.sleep_ms(500)
            if send_len == 0:
                raise Exception("send fail")
        except OSError as e:
            if e.args[0] == 128:
                print("connection closed")
                break
        except Exception as e:
            print("send fail:", e)
            time.sleep(1)
            err += 1
            continue
        count += 1
        print("send:", count)
        print("fps:", clock.fps())
        #time.sleep_ms(500)
    print("close now")
    sock.close()

'''
    ESP32_SPI firmware version: 1.4.0
    try AT connect wifi...
    network state: True ('192.168.0.180', '255.255.255.0', '192.168.0.1')
    ping baidu.com: 40 ms
    >
    MicroPython v0.5.1-136-g039f72b6c-dirty on 2020-11-18; Sipeed_M1 with kendryte-k210
    Type "help()" for more information.
    >>>
'''
