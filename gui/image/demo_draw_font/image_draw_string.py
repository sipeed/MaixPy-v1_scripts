import lcd, image

img = image.Image()

#image.font_load(image.UTF8, 16, 16, '/sd/0xA00000_font_uincode_16_16_tblr.Dzk')
image.font_load(image.UTF8, 16, 16, 0xA00000)

img.draw_string(20, 30, b'hello world!', scale=1, color=(255,255,255), x_spacing=2, mono_space=0)

img.draw_string(20, 60, b'你好，世界', scale=1, color=(0,0,255), x_spacing=2, mono_space=1)

img.draw_string(20, 160, b'簡繁轉換互換', scale=2, color=(0,255,255), x_spacing=2, mono_space=1)

img.draw_string(20, 90, b'こんにちは、世界', scale=1, color=(255,255,255), x_spacing=2, mono_space=1)

img.draw_string(20, 120, b'안녕,세상이야.', scale=1, color=(255,0,0), x_spacing=2, mono_space=1)

image.font_free()

lcd.display(img)
