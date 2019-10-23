


## Use ESP32 as WiFi module

* Download latest firmware of esp32 [here](https://github.com/sipeed/Maixduino_esp32_fimware/releases)
* Upload firmware to ESP32 by [esptool](https://github.com/espressif/esptool) or other burn tools, e.g.
```
pip install esptool
esptool.py --chip esp32 --port /dev/ttyUSB1 erase_flash
esptool.py --chip esp32 --port /dev/ttyUSB1 --baud 1500000 write_flash -z 0x0000 maixduino_esp32_firmware_v1.4.0.bin
```

* Then try demo

