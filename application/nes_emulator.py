import nes, lcd

lcd.init(freq=15000000)
nes.init(nes.KEYBOARD)
nes.run("/sd/mario.nes")

