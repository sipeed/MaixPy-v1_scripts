#################################
# model_le2be.py
# 
# run python3 on pc not maixpy
#
# not maixpy !!!!!!!!
#################################

import struct
import sys
import os

# main body
if sys.argv.__len__() > 1:
    # 参数获取
    src_file = sys.argv[1]
else:
    # 文本输入
    src_file = input("Source Bin Path: ")

if not os.path.exists(src_file):
    print('File Path Invalid! Exiting...')
    exit(1)

dst_file = src_file.split(".")
ext = dst_file.pop()
dst_file = ".".join(dst_file)
dst_file = "{}_be.{}".format(dst_file, ext)
print("Source file: {0}\nTarget File: {1}".format(
    src_file, dst_file))

try:
    sf = open(src_file, "rb")
    df = open(dst_file, "wb")

    buf_tmp = [b'0' for x in range(0, 4)]
    contents = sf.read()
    buf_size = contents.__len__()
    # 不足4个字节,自动补0
    extra_size = (buf_size % 4)
    if extra_size > 0:
        buf_size += (4 - extra_size)
        contents = contents + b'0000'

    for i in range(0, buf_size, 4):
        buf_tmp[3] = contents[i]
        buf_tmp[2] = contents[i+1]
        buf_tmp[1] = contents[i+2]
        buf_tmp[0] = contents[i+3]

        # pack into bytes flow
        tmp_bytes = struct.pack("4B", buf_tmp[0], buf_tmp[1], buf_tmp[2], buf_tmp[3])
        df.write(tmp_bytes)
finally:
    if sf:
        sf.close()
    if df:
        df.close()

print("Convert Completed!")

