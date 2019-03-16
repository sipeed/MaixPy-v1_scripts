import uos

class RAMFlashDev:
    def __init__(self):
            self.fs_size = 256*1024
            self.fs_data = bytearray(256*1024)
            self.erase_block = 32*1024
            self.log_block_size = 64*1024
            self.log_page_size = 4*1024

    def read(self,buf,size,addr):
            for i in range(len(buf)):
                buf[i] = self.fs_data[addr+i]

    def write(self,buf,size,addr):
            for i in range(len(buf)):
                self.fs_data[addr+i] = buf[i]

    def erase(self,size,addr):
            for i in range(size):
                self.fs_data[addr+i] = 0xff


blkdev = RAMFlashDev()
vfs = uos.VfsSpiffs(blkdev)
vfs.mkfs(vfs)
uos.mount(vfs,'/ramdisk')

text_str = "hello maixpy"
f = open("/ramdisk/test.txt", "w")
print("write:", text_str)
f.write(text_str)
f.close()

f = open("/ramdisk/test.txt", "r")
text = f.read()
print("read:",text)
f.close()


