# 同时开启两个 uartTrans 例程
from fpioa_manager import fm
import time
from machine import UART
import ustruct
from uart_protocol import UartTrans

def cus_cmd(uart, str):
    print("execute cus cmd {}".format(str))
    uart.write("execute cus cmd {}".format(str))

# read cmd from uart and execute cmd fun
if __name__ == "__main__":
    fm.register(22, fm.fpioa.UART1_TX, force=True)
    fm.register(21, fm.fpioa.UART1_RX, force=True)

    fm.register(24, fm.fpioa.UART2_TX, force=True)
    fm.register(23, fm.fpioa.UART2_RX, force=True)

    uart1 = UART(UART.UART1, 115200, 8, 1, 0, timeout=1000, read_buf_len=4096)
    uart2 = UART(UART.UART2, 115200, 8, 1, 0, timeout=1000, read_buf_len=4096)

    uart_TA = UartTrans(uart1)
    uart_TB = UartTrans(uart2)

    # pack cus cmd and send 
    print("send the packed 'cus' cmd to uart1")
    uart_TA.write('cus', 1)
    
    # register cus cmd
    uart_TA.reg_cmd("cus", cus_cmd, uart1, "cus1") 
    uart_TB.reg_cmd("cus", cus_cmd, uart2, "cus2") 

    # start to parse the receive cmd
    while True:
        uart_TA.parse(uart_TA.read())
        uart_TB.parse(uart_TB.read())
        time.sleep_ms(100)

'''output
pc send:
DD FF 01 00 03 63 75 73 E6 AB AA FF 

analysis:
DD FF: head
01: cmd type
00 03: cmd len
63 75 73: 'cus'
E6 AB: crc16
AA FF: end
output:
>>> send the packed 'cus' cmd to uart1
recv cmd: b'cus'
execute cus cmd 1
'''

'''packed data:  cmd: b'cus'

'''