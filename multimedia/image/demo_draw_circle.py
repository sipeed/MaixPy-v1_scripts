import lcd, time
import image

bg = (236,36,36)
lcd.init(freq=15000000)
lcd.direction(lcd.YX_RLDU)

img = image.Image()
img.draw_string(60, 100, "hello maixpy", scale=2) 
img.draw_rectangle((120,120,30,30)) 
img.draw_circle((150,140, 80))
img.draw_cross((250,40))
img.draw_arrow((250,200,20,200), color=(236,36,36))
lcd.display(img)