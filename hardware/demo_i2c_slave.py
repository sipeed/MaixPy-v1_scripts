from machine import I2C

count = 0

def on_receive(data):
    print("on_receive:",data)

def on_transmit():
    global count
    count = count+1
    print("on_transmit, send:",count)
    return count

def on_event(event):
    print("on_event:",event)

i2c = I2C(I2C.I2C0, mode=I2C.MODE_SLAVE, scl=28, sda=29, addr=0x24, addr_size=7, on_receive=on_receive, on_transmit=on_transmit, on_event=on_event)

