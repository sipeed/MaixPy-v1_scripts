import nes, lcd

lcd.init(freq=15000000)

# B A SEL START UP DOWN LEFT RIGHT
# 1 2 4   8     16  32   64   128
# nes.input(8, 0, 0) # press START
# nes.input(1P, 2P, SYS)

try:
  nes.init(nes.INPUT)
  nes.load("mario.nes")
  # nes.run("/sd/mario.nes")
  for i in range(20000): # wait
    nes.loop()
  for i in range(500):
    nes.loop()
    nes.input(8, 0, 0) # input enter
    nes.loop()
    nes.input(0, 0, 0)
    nes.loop()
  while True:
    nes.loop() # run
finally:
  nes.free()

'''python
try:
  nes.init(nes.INPUT) # input
  nes.load("mario.nes") # load
  while True:
    nes.loop() # run
finally:
  nes.free() # exit
'''
  
