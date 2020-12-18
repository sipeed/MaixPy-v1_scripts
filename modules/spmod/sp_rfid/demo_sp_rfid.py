# DATE: 2020-12-18.1
from Maix import GPIO
from fpioa_manager import fm
from machine import SPI
import time


class MFRC522:
    NRSTPD = 22

    MAX_LEN = 16

    PCD_IDLE = 0x00
    PCD_AUTHENT = 0x0E
    PCD_RECEIVE = 0x08
    PCD_TRANSMIT = 0x04
    PCD_TRANSCEIVE = 0x0C
    PCD_RESETPHASE = 0x0F
    PCD_CALCCRC = 0x03

    PICC_REQIDL = 0x26
    PICC_REQALL = 0x52
    PICC_ANTICOLL = 0x93
    PICC_SElECTTAG = 0x93
    PICC_AUTHENT1A = 0x60
    PICC_AUTHENT1B = 0x61
    PICC_READ = 0x30
    PICC_WRITE = 0xA0
    PICC_DECREMENT = 0xC0
    PICC_INCREMENT = 0xC1
    PICC_RESTORE = 0xC2
    PICC_TRANSFER = 0xB0
    PICC_HALT = 0x50

    MI_OK = 0
    MI_NOTAGERR = 1
    MI_ERR = 2

    Reserved00 = 0x00
    CommandReg = 0x01
    CommIEnReg = 0x02
    DivlEnReg = 0x03
    CommIrqReg = 0x04
    DivIrqReg = 0x05
    ErrorReg = 0x06
    Status1Reg = 0x07
    Status2Reg = 0x08
    FIFODataReg = 0x09
    FIFOLevelReg = 0x0A
    WaterLevelReg = 0x0B
    ControlReg = 0x0C
    BitFramingReg = 0x0D
    CollReg = 0x0E
    Reserved01 = 0x0F

    Reserved10 = 0x10
    ModeReg = 0x11
    TxModeReg = 0x12
    RxModeReg = 0x13
    TxControlReg = 0x14
    TxAutoReg = 0x15
    TxSelReg = 0x16
    RxSelReg = 0x17
    RxThresholdReg = 0x18
    DemodReg = 0x19
    Reserved11 = 0x1A
    Reserved12 = 0x1B
    MifareReg = 0x1C
    Reserved13 = 0x1D
    Reserved14 = 0x1E
    SerialSpeedReg = 0x1F

    Reserved20 = 0x20
    CRCResultRegM = 0x21
    CRCResultRegL = 0x22
    Reserved21 = 0x23
    ModWidthReg = 0x24
    Reserved22 = 0x25
    RFCfgReg = 0x26
    GsNReg = 0x27
    CWGsPReg = 0x28
    ModGsPReg = 0x29
    TModeReg = 0x2A
    TPrescalerReg = 0x2B
    TReloadRegH = 0x2C
    TReloadRegL = 0x2D
    TCounterValueRegH = 0x2E
    TCounterValueRegL = 0x2F

    Reserved30 = 0x30
    TestSel1Reg = 0x31
    TestSel2Reg = 0x32
    TestPinEnReg = 0x33
    TestPinValueReg = 0x34
    TestBusReg = 0x35
    AutoTestReg = 0x36
    VersionReg = 0x37
    AnalogTestReg = 0x38
    TestDAC1Reg = 0x39
    TestDAC2Reg = 0x3A
    TestADCReg = 0x3B
    Reserved31 = 0x3C
    Reserved32 = 0x3D
    Reserved33 = 0x3E
    Reserved34 = 0x3F

    serNum = []

    def __init__(self, spi, cs):
        self.spi = spi
        self.cs = cs
        self.MFRC522_Init()

    def MFRC522_Reset(self):
        # 打印所有寄存器的值
        # for i in range(0x30):
        #     val = self.Read_MFRC522(i)
        #     print("val: [{} -> {}]\r\n".format(hex(i), hex(val)))
        val = self.Read_MFRC522(self.VersionReg)
        print("version: [{}]".format(hex(val)))

        self.Write_MFRC522(self.CommandReg, self.PCD_RESETPHASE)

        val = 0xFF
        t = 0xff
        while (val) and (t & 0x10):
            val = val - 1
            t = self.Read_MFRC522(self.CommandReg)
            time.sleep_ms(1)

        time.sleep_ms(1)

        # 定义发送和接收常用模式 和Mifare卡通讯，CRC初始值0x6363
        self.Write_MFRC522(self.ModeReg, 0x3D)

        self.Write_MFRC522(self.TReloadRegL, 30)  # 16位定时器低位
        self.Write_MFRC522(self.TReloadRegH, 0)  # 16位定时器高位

        self.Write_MFRC522(self.TModeReg, 0x8D)  # 定义内部定时器的设置

        self.Write_MFRC522(self.TPrescalerReg, 0x3E)  # 设置定时器分频系数

        self.Write_MFRC522(self.TxAutoReg, 0x40)  # 调制发送信号为100%ASK

    def Write_MFRC522(self, addr, val):
        self.cs.value(0)
        self.spi.write(((addr << 1) & 0x7E))
        self.spi.write(val)
        self.cs.value(1)

    def Read_MFRC522(self, addr):
        self.cs.value(0)
        self.spi.write((((addr << 1) & 0x7E) | 0x80))
        val = self.spi.read(1)
        self.cs.value(1)
        return val[0]

    def SetBitMask(self, reg, mask):
        tmp = self.Read_MFRC522(reg)
        self.Write_MFRC522(reg, tmp | mask)

    def ClearBitMask(self, reg, mask):
        tmp = self.Read_MFRC522(reg)
        self.Write_MFRC522(reg, tmp & (~mask))

    def AntennaOn(self):
        temp = self.Read_MFRC522(self.TxControlReg)
        if not (temp & 0x03):
            self.SetBitMask(self.TxControlReg, 0x03)

    def AntennaOff(self):
        self.ClearBitMask(self.TxControlReg, 0x03)

    # 通过RC522与卡片通信
    def MFRC522_ToCard(self, command, sendData):
        backData = []
        backLen = 0
        status = self.MI_ERR
        irqEn = 0x00
        waitIRq = 0x00
        lastBits = None
        n = 0
        i = 0

        if command == self.PCD_AUTHENT:     # Mifare认证
            irqEn = 0x12                    # 允许错误中断请求ErrIEn  允许空闲中断IdleIEn
            waitIRq = 0x10                  # 认证寻卡等待时候 查询空闲中断标志位
        if command == self.PCD_TRANSCEIVE:  # 接收发送 发送接收
            irqEn = 0x77                    # 允许TxIEn RxIEn IdleIEn LoAlertIEn ErrIEn TimerIEn
            waitIRq = 0x30                  # 寻卡等待时候 查询接收中断标志位与 空闲中断标志位

        # IRqInv置位管脚IRQ与Status1Reg的IRq位的值相反
        self.Write_MFRC522(self.CommIEnReg, irqEn | 0x80)
        # Set1该位清零时，CommIRqReg的屏蔽位清零
        self.ClearBitMask(self.CommIrqReg, 0x80)
        # 写空闲命令
        self.Write_MFRC522(self.CommandReg, self.PCD_IDLE)

        # 置位FlushBuffer清除内部FIFO的读和写指针以及ErrReg的BufferOvfl标志位被清除
        self.SetBitMask(self.FIFOLevelReg, 0x80)

        while(i < len(sendData)):
            self.Write_MFRC522(self.FIFODataReg, sendData[i])  # 写数据进FIFOdata
            i = i+1

        self.Write_MFRC522(self.CommandReg, command)  # 写命令

        if command == self.PCD_TRANSCEIVE:
            # StartSend置位启动数据发送 该位与收发命令使用时才有效
            self.SetBitMask(self.BitFramingReg, 0x80)

        i = 1000 * 3

        # 认证 与寻卡等待时间
        while True:
            n = self.Read_MFRC522(self.CommIrqReg)  # 查询事件中断
            i = i - 1
            if not ((i != 0) and (not (n & 0x01)) and (not (n & waitIRq))):
                break

        self.ClearBitMask(self.BitFramingReg, 0x80)  # 清理允许StartSend位

        if i != 0:
            # 读错误标志寄存器BufferOfI CollErr ParityErr ProtocolErr
            if not (self.Read_MFRC522(self.ErrorReg) & 0x1B):
                status = self.MI_OK

                if n & irqEn & 0x01:
                    status = self.MI_NOTAGERR

                if command == self.PCD_TRANSCEIVE:
                    n = self.Read_MFRC522(self.FIFOLevelReg)
                    lastBits = self.Read_MFRC522(self.ControlReg) & 0x07
                    # print("n: {}, {}".format(n, lastBits))
                    if lastBits != 0:
                        backLen = (n-1)*8 + lastBits
                    else:
                        backLen = n*8

                    if n == 0:
                        n = 1
                    if n > self.MAX_LEN:
                        n = self.MAX_LEN

                    i = 0
                    while i < n:
                        backData.append(self.Read_MFRC522(self.FIFODataReg))
                        i = i + 1
            else:
                # print("erro: {}".format(hex(self.Read_MFRC522(self.ErrorReg))))
                status = self.MI_ERR
        # print("backlen: {}".format(backLen))
        self.SetBitMask(self.ControlReg, 0x80)
        # stop timer now
        self.Write_MFRC522(self.CommandReg, self.PCD_IDLE)
        return (status, backData, backLen)

    def MFRC522_Request(self, reqMode):
        status = None
        backBits = None
        TagType = []

        # 清理指示MIFARECyptol单元接通以及所有卡的数据通信被加密的情况
        self.ClearBitMask(self.Status2Reg, 0x08)
        # 发送的最后一个字节的 七位
        self.Write_MFRC522(self.BitFramingReg, 0x07)
        # TX1,TX2管脚的输出信号传递经发送调制的13.56的能量载波信号
        self.SetBitMask(self.TxControlReg, 0x03)

        TagType.append(reqMode)
        (status, backData, backBits) = self.MFRC522_ToCard(
            self.PCD_TRANSCEIVE, TagType)
        # print("backBits: {}".format(backBits))
        if ((status != self.MI_OK) | (backBits != 0x10)):
            status = self.MI_ERR

        return (status, backData)

    def MFRC522_Anticoll(self):
        backData = []
        serNumCheck = 0

        serNum = []

        self.Write_MFRC522(self.BitFramingReg, 0x00)

        serNum.append(self.PICC_ANTICOLL)
        serNum.append(0x20)

        (status, backData, backBits) = self.MFRC522_ToCard(
            self.PCD_TRANSCEIVE, serNum)

        if(status == self.MI_OK):
            i = 0
            if len(backData) == 5:
                while i < 4:
                    serNumCheck = serNumCheck ^ backData[i]
                    i = i + 1
                if serNumCheck != backData[i]:
                    status = self.MI_ERR
            else:
                status = self.MI_ERR

        return (status, backData)

    def CalulateCRC(self, pIndata):
        self.ClearBitMask(self.DivIrqReg, 0x04)
        self.SetBitMask(self.FIFOLevelReg, 0x80)
        i = 0
        while i < len(pIndata):
            self.Write_MFRC522(self.FIFODataReg, pIndata[i])
            i = i + 1
        self.Write_MFRC522(self.CommandReg, self.PCD_CALCCRC)
        i = 0xFF
        while True:
            n = self.Read_MFRC522(self.DivIrqReg)
            i = i - 1
            if not ((i != 0) and not (n & 0x04)):
                break
        pOutData = []
        pOutData.append(self.Read_MFRC522(self.CRCResultRegL))
        pOutData.append(self.Read_MFRC522(self.CRCResultRegM))
        return pOutData

    def MFRC522_SelectTag(self, serNum):
        backData = []
        buf = []
        buf.append(self.PICC_SElECTTAG)
        buf.append(0x70)
        i = 0
        while i < 5:
            buf.append(serNum[i])
            i = i + 1
        pOut = self.CalulateCRC(buf)
        buf.append(pOut[0])
        buf.append(pOut[1])
        (status, backData, backLen) = self.MFRC522_ToCard(self.PCD_TRANSCEIVE, buf)

        if (status == self.MI_OK) and (backLen == 0x18):
            print("Size: ", str(backData[0]))
            return backData[0]
        else:
            return 0

    def MFRC522_Auth(self, authMode, BlockAddr, Sectorkey, serNum):
        buff = []

        # First byte should be the authMode (A or B)
        buff.append(authMode)

        # Second byte is the trailerBlock (usually 7)
        buff.append(BlockAddr)

        # Now we need to append the authKey which usually is 6 bytes of 0xFF
        i = 0
        while(i < len(Sectorkey)):
            buff.append(Sectorkey[i])
            i = i + 1
        i = 0

        # Next we append the first 4 bytes of the UID
        while(i < 4):
            buff.append(serNum[i])
            i = i + 1

        # Now we start the authentication itself
        (status, backData, backLen) = self.MFRC522_ToCard(self.PCD_AUTHENT, buff)

        # Check if an error occurred
        if not(status == self.MI_OK):
            print("AUTH ERROR!!")
        if not (self.Read_MFRC522(self.Status2Reg) & 0x08) != 0:
            print("AUTH ERROR(status2reg & 0x08) != 0")

        # Return the status
        return status

    def MFRC522_StopCrypto1(self):
        self.ClearBitMask(self.Status2Reg, 0x08)

    def MFRC522_Read(self, blockAddr):
        recvData = []
        recvData.append(self.PICC_READ)
        recvData.append(blockAddr)
        pOut = self.CalulateCRC(recvData)
        recvData.append(pOut[0])
        recvData.append(pOut[1])
        (status, backData, backLen) = self.MFRC522_ToCard(
            self.PCD_TRANSCEIVE, recvData)
        if not (status == self.MI_OK):
            print("Error while reading!")
        i = 0
        if len(backData) == 16:
            print("Sector "+str(blockAddr)+" "+str(backData))
            return backData

    def MFRC522_Write(self, blockAddr, writeData):
        buff = []
        buff.append(self.PICC_WRITE)
        buff.append(blockAddr)
        crc = self.CalulateCRC(buff)
        buff.append(crc[0])
        buff.append(crc[1])
        (status, backData, backLen) = self.MFRC522_ToCard(
            self.PCD_TRANSCEIVE, buff)
        if not(status == self.MI_OK) or not(backLen == 4) or not((backData[0] & 0x0F) == 0x0A):
            status = self.MI_ERR

        print(str(backLen)+" backdata &0x0F == 0x0A "+str(backData[0] & 0x0F))
        if status == self.MI_OK:
            i = 0
            buf = []
            while i < 16:
                buf.append(writeData[i])
                i = i + 1
            crc = self.CalulateCRC(buf)
            buf.append(crc[0])
            buf.append(crc[1])
            (status, backData, backLen) = self.MFRC522_ToCard(
                self.PCD_TRANSCEIVE, buf)
            if not(status == self.MI_OK) or not(backLen == 4) or not((backData[0] & 0x0F) == 0x0A):
                print("Error while writing")
            if status == self.MI_OK:
                print("Data written")
            return status

    def MFRC522_DumpClassic1K(self, key, uid):
        i = 0
        while i < 64:
            status = self.MFRC522_Auth(self.PICC_AUTHENT1A, i, key, uid)
            # Check if authenticated
            if status == self.MI_OK:
                self.MFRC522_Read(i)
            else:
                print("Authentication error")
            i = i+1

    def MFRC522_Init(self):
        self.MFRC522_Reset()
        self.M500PcdConfigISOType('A')
        time.sleep_ms(2)
        self.AntennaOn()  # 开天线

    def M500PcdConfigISOType(self, ucType):
        if ucType == 'A':  # ISO14443_A
            self.ClearBitMask(self.Status2Reg, 0x08)
            self.Write_MFRC522(self.ModeReg, 0x3D)  # 3F
            self.Write_MFRC522(self.RxSelReg, 0x86)  # 84
            self.Write_MFRC522(self.RFCfgReg, 0x7F)  # 4F
            self.Write_MFRC522(self.TReloadRegL, 30)
            self.Write_MFRC522(self.TReloadRegH, 0)
            self.Write_MFRC522(self.TModeReg, 0x8D)
            self.Write_MFRC522(self.TPrescalerReg, 0x3E)
        else:
            print("unk ISO type\r\n")

if __name__ == "__main__":
    time.sleep(2)
    from micropython import const
    ################### config ###################
    CS_NUM = const(20)
    SPI_FREQ_KHZ = const(600)
    SPI_SCK = const(21)
    SPI_MOSI = const(8)
    SPI_MISO = const(15)
    #############################################

    continue_reading = True

    # 20: CS_NUM;
    fm.register(CS_NUM, fm.fpioa.GPIOHS20, force=True)

    # set gpiohs work mode to output mode
    cs = GPIO(GPIO.GPIOHS20, GPIO.OUT)

    spi1 = SPI(SPI.SPI_SOFT, mode=SPI.MODE_MASTER, baudrate=SPI_FREQ_KHZ * 1000,
            polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=SPI_SCK, mosi=SPI_MOSI, miso=SPI_MISO)

    # Create an object of the class MFRC522
    MIFAREReader = MFRC522(spi1, cs)

    # Welcome message
    print("Welcome to the MFRC522 data read/write example")

    # This loop keeps checking for chips. If one is near it will get the UID and authenticate
    while continue_reading:
        time.sleep_ms(300)
        # Scan for cards
        (status, ataq) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQALL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            print("Card detected type: ",hex(ataq[0]<<8|ataq[1]))
            # Get the UID of the card
            (status, uid) = MIFAREReader.MFRC522_Anticoll()

            # If we have the UID, continue
            if status == MIFAREReader.MI_OK:

                # Print UID
                print("Card read UID: " +
                    str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

                # This is the default key of M1(S50) for authentication
                key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                # Select the scanned tag
                MIFAREReader.MFRC522_SelectTag(uid)

                # Authenticate
                status = MIFAREReader.MFRC522_Auth(
                    MIFAREReader.PICC_AUTHENT1A, 0x12, key, uid)

                # Check if authenticated
                if status == MIFAREReader.MI_OK:
                    data = []
                    # Fill the data with 0~16
                    for x in range(0, 16):
                        data.append(x)

                    # Write the data
                    print("Sector 11 will now be filled with 1~16:")
                    status = MIFAREReader.MFRC522_Write(0x12, data)

                    if status == MIFAREReader.MI_OK:
                        print("start to read")
                        # read the data
                        MIFAREReader.MFRC522_Read(0x12)

                    # Stop
                    MIFAREReader.MFRC522_StopCrypto1()
                else:
                    print("Authentication error")
