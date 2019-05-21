import network, time
from machine import UART
from Maix import GPIO
from fpioa_manager import fm, board_info


fm.register(8, fm.fpioa.GPIOHS0)
wifi_en=GPIO(GPIO.GPIOHS0, GPIO.OUT)
fm.register(board_info.WIFI_RX, fm.fpioa.UART2_TX)
fm.register(board_info.WIFI_TX, fm.fpioa.UART2_RX)

uart = UART(UART.UART2,115200,timeout=1000, read_buf_len=4096)

def wifi_enable(en):
    global wifi_en
    wifi_en.value(en)

def wifi_deal_ap_info(info):
    res = []
    for ap_str in info:
        ap_str = ap_str.split(",")
        info_one = []
        for node in ap_str:
            if node.startswith('"'):
                info_one.append(node[1:-1])
            else:
                info_one.append(int(node))
        res.append(info_one)
    return res
    

wifi_enable(1)
time.sleep(2)
nic = network.ESP8285(uart)

ap_info = nic.scan()
ap_info = wifi_deal_ap_info(ap_info)

ap_info.sort(key=lambda x:x[2], reverse=True) # sort by rssi
for ap in ap_info:
    print("SSID:{:^20}, RSSI:{:>5} , MAC:{:^20}".format(ap[1], ap[2], ap[3]) )
    
