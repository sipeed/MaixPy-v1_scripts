import lcd
import image

bg = (236, 36, 36)
lcd.init(freq=15000000)


img = image.Image()
img.draw_circle((150, 140, 80))
img.draw_rectangle(100,100,60,60)
img.draw_cross((250, 40))
img.draw_arrow((250, 200, 20, 200), color=(236, 36, 36))

#img.rotation_corr(x_rotation=180)
img.rotation_corr(x_rotation=180, fov=2) # The FOV parameter is required otherwise strange errors will occur

lcd.display(img)
