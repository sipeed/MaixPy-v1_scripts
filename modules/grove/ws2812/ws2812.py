from modules import ws2812

# test maix cube grove ws2813 24
led_io, led_num = 24, 24

ws = ws2812(led_io, led_num)

for i in range(led_num):
    ws.set_led(i, (0, 0, 0))
ws.display()

import time, math
value = 0
while True:
  value += 1
  for i in range(value, value + led_num):
    ws.set_led(i % led_num, (value + i, value + i, value + i))
  ws.display()
  time.sleep_ms(10)
