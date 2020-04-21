import utime
from machine import I2C

i2c = I2C(I2C.I2C0,freq=100000, scl=28, sda=29)
#scl和sda看自己具体插哪里而更改的

def pca_setfreq(freqs):
    freqs *= 0.92
    prescaleval = 25000000
    prescaleval /= 4096
    prescaleval /= freqs
    prescaleval -= 1
    prescale =int(prescaleval + 0.5)

    oldmode = i2c.readfrom_mem(0x40,0x00,8)

    newmode = (oldmode[0]&0x7F) | 0x10  #sleep

    i2c.writeto_mem(0x40,0x00,newmode) #go to sleep

    i2c.writeto_mem(0x40,0xFE, prescale)  #set the prescaler

    i2c.writeto_mem(0x40,0x00, oldmode)
    utime.sleep_ms(2)

    i2c.writeto_mem(0x40,0x00, oldmode[0]|0xa1)

def pca_setpwm(num,on,off):
    i2c.writeto_mem(0x40,0x06+4*num,on)
    i2c.writeto_mem(0x40,0x07+4*num,on>>8)
    i2c.writeto_mem(0x40,0x08+4*num,off)
    i2c.writeto_mem(0x40,0x09+4*num,off>>8)

def pca_init(hz,angle): #初始化函数
    off = 0
    i2c.writeto_mem(0x40,0x00,0x0)
    pca_setfreq(hz)
    off = int(145+angle*2.4)
    pca_setpwm(0,0,off)
    #pca_setpwm(1,0,off)
    #pca_setpwm(2,0,off)
    #pca_setpwm(3,0,off)
    #pca_setpwm(4,0,off)
    #pca_setpwm(5,0,off)
    #pca_setpwm(6,0,off)
    #pca_setpwm(7,0,off)
    #pca_setpwm(8,0,off)
    #pca_setpwm(9,0,off)
    #pca_setpwm(10,0,off)
    #pca_setpwm(11,0,off)
    #pca_setpwm(12,0,off)
    #pca_setpwm(13,0,off)
    #pca_setpwm(14,0,off)
    #pca_setpwm(15,0,off)
    utime.sleep_ms(500)

def pca_mg90(num,start_angle,end_angle,mode,speed):
    off = 0
    if mode==0:
        off=int(158+end_angle*2.2)
        pca_setpwm(num,0,off)
    elif mode==1:
        off=int(158+end_angle*2.2)
        pca_setpwm(num,0,off)
    #未完待续

pca_init(50,60)
