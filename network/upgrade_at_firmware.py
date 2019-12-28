

######## AP config #########
WIFI_SSID = "Sipeed_2.4G"
WIFI_PASSWD = "Sipeed123."
############################


import time
from Maix import GPIO
from machine import UART
from fpioa_manager import fm, board_info

class Upgrade():
    def __init__(self, ssid=None, passwd=None):
        if not ssid:
            raise Exception("no SSID")
        self.ssid = ssid
        self.passwd = passwd
        print("[init SSID:", ssid, ", PASSWD:", passwd)
        fm.register(0, fm.fpioa.GPIOHS1, force=True)
        wifi_io0_en=GPIO(GPIO.GPIOHS1, GPIO.OUT)
        wifi_io0_en.value(0)

        fm.register(8, fm.fpioa.GPIOHS0)
        self.wifi_en = GPIO(GPIO.GPIOHS0,GPIO.OUT)

        fm.register(board_info.WIFI_RX,fm.fpioa.UART2_TX)
        fm.register(board_info.WIFI_TX,fm.fpioa.UART2_RX)
        self.uart = UART(UART.UART2,115200,timeout=1000, read_buf_len=4096)
        self.update_step = 0

    def wifi_enable(self, en):
        self.wifi_en.value(en)
    
    def reboot(self):
        print("reoobt")
        self.wifi_enable(0)
        time.sleep_ms(200)
        self.wifi_enable(1)
        time.sleep_ms(2000)
        print("reoobt end")

    def cmd_set_station_mode(self):
        print("[cmd station mode]")
        recv = self.uart.read()
        print(recv)
        self.uart.write(b'AT+CWMODE_DEF=1\r\n')
        time.sleep_ms(200)
        recv = self.uart.read()
        print(recv)
        if b"OK" in recv:
            return True
        return False

    def cmd_join_ap_and_wait(self):
        print("[cmd join ap]")
        recv = self.uart.read()
        print(recv)
        if self.passwd:
            self.uart.write(b'AT+CWJAP_DEF="{}","{}"\r\n'.format(self.ssid, self.passwd))
        else:
            self.uart.write(b'AT+CWJAP_DEF="{}"\r\n'.format(self.ssid))
        time.sleep_ms(200)
        print("[wait join ap -- 0]")
        read = b""
        tim = time.ticks_ms()
        while 1:
            if time.ticks_ms() - tim > 10000:
                return False
            recv = self.uart.read()
            if recv:
                print(recv)
            else:
                print(".", end='')
            if recv:
                read += recv
            if b"GOT IP" in read:
                return True
    
    def wait_join_ap(self):
        print("[wait join ap]")
        read = b""
        tim = time.ticks_ms()
        while 1:
            if time.ticks_ms() - tim > 10000:
                raise Exception("wait for join AP timeout")
            recv = self.uart.read()
            if recv:
                print(recv)
            else:
                print(".", end='')
            if recv:
                read += recv
            if b"GOT IP" in read:
                break
        time.sleep_ms(1000)
        read = self.uart.read()
        print(read)
        
    def cmd_upgrade(self):
        print("[cmd upgrade]")
        self.update_step = 0
        recv = self.uart.read()
        print(recv)
        self.uart.write(b'AT+CIUPDATE\r\n')
        time.sleep_ms(200)
        print("[wait upgrade process -- 0]")
        read = b""
        tim = time.ticks_ms()
        while 1:
            if time.ticks_ms() - tim > 3000:
                return False
            recv = self.uart.read()
            if recv:
                print(recv)
            else:
                print(".", end='')
            if recv:
                read += recv
            if b"+CIPUPDATE:" in read:
                if b":4" in read:
                    self.update_step = 4
                return True
            time.sleep_ms(200)
    
    def cmd_restore(self):
        print("[cmd restore]")
        recv = self.uart.read()
        print(recv)
        self.uart.write(b'AT+RESTORE\r\n')
        self.wait_boot_up()

    def wait_upgrade(self):
        print("[wait upgrade process]")
        read = b""
        tim = time.ticks_ms()
        while 1:
            if time.ticks_ms() - tim > 80000:
                raise Exception("wait for update timeout")
            recv = self.uart.read()
            if recv:
                print(recv)
            else:
                print(".", end='')
            if recv:
                read += recv
            if self.update_step != 4 and b"+CIPUPDATE:4" in read:
                self.update_step = 4
            if self.update_step == 4 and b"OK" in read:
                break
            time.sleep_ms(200)

    def check_version(self):
        read = self.uart.read()
        print(read)
        self.uart.write("AT+GMR\r\n")
        time.sleep_ms(200)
        read = self.uart.read()
        print(read)
        if b"version" in read:
            return read.split(b"\r\n")[1:-2]
        else:
            return None

    def wait_boot_up(self):
        print("[wait boot up]")
        read = b""
        tim = time.ticks_ms()
        while 1:
            if time.ticks_ms() - tim > 5000:
                raise Exception("wait boot up timeout")
            recv = self.uart.read()
            if recv:
                print(recv)
            else:
                print(".", end='')
            if recv:
                read += recv
            if b"ready\r\n" in read:
                break

    def upgrade(self):
        # reboot
        self.reboot()

        # wait boot up
        self.wait_boot_up()

        # set mode
        while not self.cmd_set_station_mode():
            time.sleep_ms(1)

        # config AP # wait for join ok
        while not self.cmd_join_ap_and_wait():
            time.sleep_ms(1)
        
        # reboot # maybe firmware v1.5 reboot by itself (bug)
        self.reboot()

        # wait for connect to AP
        self.wait_join_ap()

        # upgrade
        while not self.cmd_upgrade():
            time.sleep_ms(1)
        
        self.wait_upgrade()
        time.sleep_ms(2000)
        self.wait_boot_up()
        self.cmd_restore()
        version = self.check_version()
        print("===============")
        for v in version:
            print(v.decode())
        print("===============")
        
        

obj = Upgrade(WIFI_SSID, WIFI_PASSWD)
obj.upgrade()

