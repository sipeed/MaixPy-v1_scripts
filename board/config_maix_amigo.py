import json

config = {
  "type": "amigo",
  "lcd": {
      "height": 320,
      "width": 480,
      "invert": 0,
      "dir": 40,
      "lcd_type": 1
  },
  "sdcard":{
      "sclk":11,
      "mosi":10,
      "miso":6,
      "cs":26
  },
  "board_info": {
      'BOOT_KEY': 16,
      'LED_R': 14,
      'LED_G': 15,
      'LED_B': 17,
      'LED_W': 32,
      'BACK': 31,
      'ENTER': 23,
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
