
import json

config = {
  "type": "amigo",
  "lcd": {
      "height": 320,
      "width": 480,
      "invert": 1,
      "dir": 40,
      "lcd_type": 2
  },
  "sdcard":{
      "sclk":11,
      "mosi":10,
      "miso":6,
      "cs":26
  },
  "board_info": {
      'BOOT_KEY': 23,
      'LED_R': 14,
      'LED_G': 15,
      'LED_B': 17,
      'LED_W': 32,
      'BACK': 23,
      'ENTER': 16,
      'NEXT': 20,
      'WIFI_TX': 6,
      'WIFI_RX': 7,
      'WIFI_EN': 8,
      'I2S0_MCLK': 13,
      'I2S0_SCLK': 21,
      'I2S0_WS': 18,
      'I2S0_IN_D0': 35,
      'I2S0_OUT_D2': 34,
      'I2C_SDA': 27,
      'I2C_SCL': 24,
      'SPI_SCLK': 11,
      'SPI_MOSI': 10,
      'SPI_MISO': 6,
      'SPI_CS': 12,
  }
}

cfg = json.dumps(config)
print(cfg)

# config sensor
try:
  os.remove('/flash/boot.py')
except:
  pass
with open('/flash/boot.py', 'wb') as f:
  cfg_sensor = b'import lcd\nlcd.clear((99, 99, 99))\nlcd.register(0xD1, 0x00)\nlcd.init()\nfrom machine import I2C\naxp173 = I2C(I2C.I2C0, freq=100000, scl=24, sda=27)\naxp173.writeto_mem(0x34, 0x27, 0x20)\naxp173.writeto_mem(0x34, 0x28, 0x0C)\naxp173.writeto_mem(0x34, 0x36, 0xCC, mem_size=8)'
  f.write(cfg_sensor)
  del cfg_sensor

try:
  with open('/flash/config.json', 'rb') as f:
    tmp = json.loads(f.read())
    print(tmp)
    if tmp["type"] != config["type"]:
      raise Exception('config.json no exist')
except Exception as e:
  with open('/flash/config.json', "w") as f:
    f.write(cfg)
  import machine
  machine.reset()
