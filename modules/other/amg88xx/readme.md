## amg88xx

see this https://github.com/sipeed/MaixPy/pull/329


- driver for amg88xx
- module for amg88xx
- enable/disable from menuconfig the driver and module

## EXAMPLE

on maix-cube.

```python

import lcd

from board import board_info
from fpioa_manager import fm
from modules import amg88xx

fm.fpioa.set_function(board_info.GROVE1, fm.fpioa.I2C0_SCLK)
fm.fpioa.set_function(board_info.GROVE2, fm.fpioa.I2C0_SDA)

lcd.init()

dev = amg88xx(0)

while 1:
    time.sleep(1/10)

    # GET DATA
    temperature = dev.temperature()
    mn, mx, _, _ = dev.min_max()

    #                    min,   max,   scale,  method
    img   = dev.to_image(mn,    mx,    30,     dev.METHOD_NEAREST)
    # img = dev.to_image(mn,    mx,    30,     dev.METHOD_BILINEAR)

    lcd.display(img.to_rainbow(1))
```
