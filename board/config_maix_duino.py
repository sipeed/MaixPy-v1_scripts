import json

config = {
  "type": "duino",
  "board_info": {
      'BOOT_KEY': 16,
      'LED_R': 13,
      'LED_G': 12,
      'LED_B': 14,
      'WIFI_TX': 6,
      'WIFI_RX': 7,
      'WIFI_EN': 8,
      'MIC0_WS': 19,
      'MIC0_DATA': 20,
      'MIC0_BCK': 18,
      'I2S_WS': 33,
      'I2S_DA': 34,
      'I2S_BCK': 35,
      'ESP32_CS': 25,
      'ESP32_RST': 8,
      'ESP32_RDY': 9,
      'ESP32_MOSI': 28,
      'ESP32_MISO': 26,
      'ESP32_SCLK': 27,
      'PIN0':4,
      'PIN1':5,
      'PIN2':21,
      'PIN3':22,
      'PIN4':23,
      'PIN5':24,
      'PIN6':32,
      'PIN7':15,
      'PIN8':14,
      'PIN9':13,
      'PIN10':12,
      'PIN11':11,
      'PIN12':10,
      'PIN13':3,
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
