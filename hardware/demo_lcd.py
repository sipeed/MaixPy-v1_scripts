
import lcd, time

lcd.init()
#lcd.direction(lcd.XY_RLDU)

#lcd.init(type=2, invert=True) # cube ips
#lcd.init(width=320, height=240, invert=True, freq=20000000)

# see lcd datasheet (such as amigo ips)
#lcd.register(0x36, 0b01101000) # BGR2RGB Mode
#lcd.register(0x21, None) # invert=True
#lcd.register(0x20, None) # invert=False
#lcd.register(0x36, [0b01101000, ]) # invert=True

lcd.clear(lcd.RED)

lcd.rotation(0)
lcd.draw_string(30, 30, "hello maixpy", lcd.WHITE, lcd.RED)
time.sleep(1)
lcd.rotation(1)
lcd.draw_string(60, 60, "hello maixpy", lcd.WHITE, lcd.RED)
time.sleep(1)
lcd.rotation(2)
lcd.draw_string(120, 60, "hello maixpy", lcd.WHITE, lcd.RED)
time.sleep(1)
lcd.rotation(3)
lcd.draw_string(120, 120, "hello maixpy", lcd.WHITE, lcd.RED)
time.sleep(1)
