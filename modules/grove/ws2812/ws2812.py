##############demo1
from modules import ws2812
class_ws2812 = ws2812(board_info.D[4],30)
for i in range(30):
    class_ws2812.set_led(i,(0xff,0,0))
class_ws2812.display()

#############demo2
from modules import ws2812
class_ws2812 = ws2812(board_info.D[4],30)
r=0
dir = True
while True:
    if dir:
        r += 1
    else:
        r -= 1
    if r>=255:
        r = 255
        dir = False
    elif r<0:
        r = 0
        dir = True
    for i in range(30):
        a = class_ws2812.set_led(i,(r,0,0))
    a=class_ws2812.display()
