import ustruct

class UartTrans:
    def __init__(self, uart):
        self.uart = uart
        self.orders = {}
        self.args = {}

    CRC16_TABLE = (
    0x0000, 0xC0C1, 0xC181, 0x0140, 0xC301, 0x03C0, 0x0280, 0xC241, 0xC601,
    0x06C0, 0x0780, 0xC741, 0x0500, 0xC5C1, 0xC481, 0x0440, 0xCC01, 0x0CC0,
    0x0D80, 0xCD41, 0x0F00, 0xCFC1, 0xCE81, 0x0E40, 0x0A00, 0xCAC1, 0xCB81,
    0x0B40, 0xC901, 0x09C0, 0x0880, 0xC841, 0xD801, 0x18C0, 0x1980, 0xD941,
    0x1B00, 0xDBC1, 0xDA81, 0x1A40, 0x1E00, 0xDEC1, 0xDF81, 0x1F40, 0xDD01,
    0x1DC0, 0x1C80, 0xDC41, 0x1400, 0xD4C1, 0xD581, 0x1540, 0xD701, 0x17C0,
    0x1680, 0xD641, 0xD201, 0x12C0, 0x1380, 0xD341, 0x1100, 0xD1C1, 0xD081,
    0x1040, 0xF001, 0x30C0, 0x3180, 0xF141, 0x3300, 0xF3C1, 0xF281, 0x3240,
    0x3600, 0xF6C1, 0xF781, 0x3740, 0xF501, 0x35C0, 0x3480, 0xF441, 0x3C00,
    0xFCC1, 0xFD81, 0x3D40, 0xFF01, 0x3FC0, 0x3E80, 0xFE41, 0xFA01, 0x3AC0,
    0x3B80, 0xFB41, 0x3900, 0xF9C1, 0xF881, 0x3840, 0x2800, 0xE8C1, 0xE981,
    0x2940, 0xEB01, 0x2BC0, 0x2A80, 0xEA41, 0xEE01, 0x2EC0, 0x2F80, 0xEF41,
    0x2D00, 0xEDC1, 0xEC81, 0x2C40, 0xE401, 0x24C0, 0x2580, 0xE541, 0x2700,
    0xE7C1, 0xE681, 0x2640, 0x2200, 0xE2C1, 0xE381, 0x2340, 0xE101, 0x21C0,
    0x2080, 0xE041, 0xA001, 0x60C0, 0x6180, 0xA141, 0x6300, 0xA3C1, 0xA281,
    0x6240, 0x6600, 0xA6C1, 0xA781, 0x6740, 0xA501, 0x65C0, 0x6480, 0xA441,
    0x6C00, 0xACC1, 0xAD81, 0x6D40, 0xAF01, 0x6FC0, 0x6E80, 0xAE41, 0xAA01,
    0x6AC0, 0x6B80, 0xAB41, 0x6900, 0xA9C1, 0xA881, 0x6840, 0x7800, 0xB8C1,
    0xB981, 0x7940, 0xBB01, 0x7BC0, 0x7A80, 0xBA41, 0xBE01, 0x7EC0, 0x7F80,
    0xBF41, 0x7D00, 0xBDC1, 0xBC81, 0x7C40, 0xB401, 0x74C0, 0x7580, 0xB541,
    0x7700, 0xB7C1, 0xB681, 0x7640, 0x7200, 0xB2C1, 0xB381, 0x7340, 0xB101,
    0x71C0, 0x7080, 0xB041, 0x5000, 0x90C1, 0x9181, 0x5140, 0x9301, 0x53C0,
    0x5280, 0x9241, 0x9601, 0x56C0, 0x5780, 0x9741, 0x5500, 0x95C1, 0x9481,
    0x5440, 0x9C01, 0x5CC0, 0x5D80, 0x9D41, 0x5F00, 0x9FC1, 0x9E81, 0x5E40,
    0x5A00, 0x9AC1, 0x9B81, 0x5B40, 0x9901, 0x59C0, 0x5880, 0x9841, 0x8801,
    0x48C0, 0x4980, 0x8941, 0x4B00, 0x8BC1, 0x8A81, 0x4A40, 0x4E00, 0x8EC1,
    0x8F81, 0x4F40, 0x8D01, 0x4DC0, 0x4C80, 0x8C41, 0x4400, 0x84C1, 0x8581,
    0x4540, 0x8701, 0x47C0, 0x4680, 0x8641, 0x8201, 0x42C0, 0x4380, 0x8341,
    0x4100, 0x81C1, 0x8081, 0x4040)

    def crc16(self, data):
        crc = 0xFFFF
        for char in data:
            crc = (crc >> 8) ^ self.CRC16_TABLE[((crc) ^ char) & 0xFF]
        crc = ustruct.pack('<H', crc)
        crc = crc[0] << 8 | crc[1]
        return crc
    
    # brief: register cmd
    # cmd: strng, cmd name
    # fun: the function will be execute
    # args: parameter of the fun 
    def reg_cmd(self, cmd, fun, *args):
        hcmd = hash(cmd)
        self.orders[hcmd] = fun
        self.args[hcmd] = args

    # brief: unregister cmd
    # cmd: string
    def unreg_cmd(self, cmd):
        hcmd = hash(cmd)
        try:
            del self.orders[hcmd]
        except:
            print("unreg order {} failed".format(cmd))
        try:
            del self.args[hcmd]
        except:
            pass

    # brief: pack data, 
    # data: data will be packed
    # return: packed data(packed data format: 0xddff(head) len data crc16 0xaaff(end))
    def pack_data(self, data, cmd = 0):
        head = 0xddff
        end = 0xaaff
        data = bytearray(data)
        crc = self.crc16(data)
        fmt = '>HBH'+str(len(data))+'sHH'
        is_cmd = 1 if cmd else 0
        data = ustruct.pack(fmt, head, is_cmd, len(data), data, crc, end)
        return data

    # brief: unpack data
    # data: the rawdata will be unpacked(rawdata format: 0xddff len data crc16 0xaaff)
    # return: unpacked data
    def unpack_data(self, data, size):
        data = bytearray(data)
        ra = size - 4
        ret = []
        for i in range(ra):
            try:
                (head, is_cmd, len) = ustruct.unpack('>HBH', data[i:i+5])
                if(head == 0xddff):  # check head
                    try:
                        fmt = '>'+str(len)+'sHH'
                        (s, crc, end) = ustruct.unpack(
                            fmt, data[i+5:])
                        if s != None:
                            crc_check = self.crc16(s)
                            if crc == crc_check:
                                ret.append((is_cmd, s))
                            else:
                                print("receive crc check failed: ", data)
                        continue
                    except:
                        continue
            except:
                continue
        return ret

    def read(self):
        read_data = self.uart.read()
        if read_data:
            udatas = self.unpack_data(read_data, len(read_data))
            return udatas
    
    def write(self, s, is_cmd = 0):
        s = self.pack_data(s, is_cmd)
        return self.uart.write(s)

    # execute cmd
    # cmd: string
    def exec_cmd(self, cmd):
        hcmd = hash(cmd)
        try:
            args = self.args[hcmd]
            try:
                self.orders[hcmd](*args) # execute cmd fun
            except:
                print("can't find cmd: ", cmd)
        except:
            try:
                self.orders[hcmd]() # execute cmd fun
            except:
                print("can't find cmd: ", cmd)

    def bytes_to_nums(self, b):
        ret = []
        i = 0
        while i < len(b):
            try:
                t = ustruct.unpack('>s', b[i:i+1]) # type
                t = t[0].decode('utf-8')
                fmt = '>' + t
                try:
                    num = ustruct.unpack(fmt, b[i+1:])
                    ret.append(num[0])
                    i = i + 1 + ustruct.calcsize(str(t))
                except: 
                    i = i + 1
            except:
                i = i + 1
        return ret

    # fl: uint8_t(B)，int8_t(b), uint16_t(H), int16_t(h), uint32_t(I), int32_t(i), double(d), str(s)
    def pack_num(self, n, fl):
        return  ustruct.pack(">s"+fl,fl,n)

    # read data, parse to cmd and execute
    def parse(self, udatas):
        ret = []
        if udatas:
            for udata in udatas:
                is_cmd  = udata[0]
                if udata[0]: # cmd
                    self.exec_cmd(udata[1])
                else: # data
                    nums = self.bytes_to_nums(udata[1])
                    if len(nums) > 0:
                        ret.append(nums) # is nums
                    try:
                        s = udata[1].decode('utf-8') # is string
                        ret.append(s)
                    except:
                        pass
        return ret