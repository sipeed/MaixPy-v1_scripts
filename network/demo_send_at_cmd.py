import time
from Maix import GPIO
from machine import UART
from fpioa_manager import fm, board_info

fm.register(0, fm.fpioa.GPIOHS1, force=True)
wifi_io0_en=GPIO(GPIO.GPIOHS1, GPIO.OUT)
wifi_io0_en.value(0)

fm.register(8, fm.fpioa.GPIOHS0)
wifi_en=GPIO(GPIO.GPIOHS0,GPIO.OUT)
fm.register(board_info.WIFI_RX,fm.fpioa.UART2_TX)
fm.register(board_info.WIFI_TX,fm.fpioa.UART2_RX)

def wifi_enable(en):
    global wifi_en
    wifi_en.value(en)


uart = UART(UART.UART2,115200,timeout=1000, read_buf_len=4096)


wifi_enable(0)
time.sleep_ms(200)
wifi_enable(1)

time.sleep_ms(2000)

while 1:
	read = uart.read()
	if read:
		print(read)
	uart.write("AT+GMR\r\n")
	time.sleep_ms(500)

