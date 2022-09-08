import time
import lcd

lcd.init(type=5, lcd_type=3)
while True:
    lcd.clear(0xff00)
    lcd.rotation(0)
    lcd.draw_string(30, 30, "hello maixpy", lcd.WHITE, 0xff00)
    time.sleep(1)

    lcd.clear(0x00ff)
    lcd.rotation(1)
    lcd.draw_string(60, 60, "hello maixpy", lcd.WHITE, 0X00FF)
    time.sleep(1)

    lcd.clear(0x0ff0)
    lcd.rotation(2)
    lcd.draw_string(120, 60, "hello maixpy", lcd.WHITE, 0x0ff0)
    time.sleep(1)

    lcd.clear(0x0f0f)
    lcd.rotation(3)
    lcd.draw_string(120, 120, "hello maixpy", lcd.WHITE, 0x0f0f)
    time.sleep(1)
