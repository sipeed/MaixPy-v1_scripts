
import image, lcd

lcd.init(freq=20000000)

i = 0
dir = 1

while(True):
    img = image.Image(copy_to_fb=1)
    img.clear()
    img.draw_rectangle(i,50,50,50)
    lcd.display(img)
    
    if dir:
        i += 5
        if i==270:
           dir = 0
    else:
        i -= 5
        if i==0:
            dir = 1

