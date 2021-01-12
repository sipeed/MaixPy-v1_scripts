# 收发数据例程
from fpioa_manager import fm
import time
from machine import UART
import ustruct
from uart_protocol import UartTrans

# read cmd from uart and execute cmd fun
if __name__ == "__main__":
    fm.register(22, fm.fpioa.UART1_TX, force=True)
    fm.register(21, fm.fpioa.UART1_RX, force=True)
    uart1 = UART(UART.UART1, 115200, 8, 1, 0, timeout=1000, read_buf_len=4096)
    uart_t = UartTrans(uart1)

    # pack nums dat and send 
    print("send the packed nums data to uart1")
    nums = uart_t.pack_num(3.1415, 'f') + uart_t.pack_num(16, 'H') + uart_t.pack_num(-8, 'b')
    uart_t.write(nums)
    uart_t.write("aaaaaaaaaaaaaaaaaaa")

    # start to parse the receive cmd
    while True:
        udatas = uart_t.read()
        d = uart_t.parse(udatas)
        if d:
            print(d)

# send and reveive string
'''log
pc send:  DD FF 00 00 13 61 61 61 61 61 61 61 61 61 61 61 61 61 61 61 61 61 61 61 CE 3A AA FF

analysis:
DD FF: head
00: data type
00 13： data len
61 ... 61: data
CE 3A: crc16
AA FF: end

output:
['aaaaaaaaaaaaaaaaaaa']

pc send:
DD FF 00 00 0A 66 40 49 0E 56 48 00 10 62 F8 4C E0 AA FF 

analysis:
DD FF: head
00: data type
0A: data len
66: 'f' float
40 49 0e 56: 3.1415
48: 'H' uint16_t
00 10: 16
62: 'b' int8_t
f8: -8
4c e0: crc16
aa ff: end

output:
>>> send the packed nums data to uart1
[3.1415, 16, -8]
'''