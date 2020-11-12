import json

config = {
  "type": "dock",
  "board_info": {
      'BOOT_KEY': 16,
      'LED_R': 14,
      'LED_G': 13,
      'LED_B': 12,
      'WIFI_TX': 6,
      'WIFI_RX': 7,
      'WIFI_EN': 8,
      'MIC0_WS': 30,
      'MIC0_DATA': 20,
      'MIC0_BCK': 32,
      'I2S_WS': 33,
      'I2S_DA': 34,
      'I2S_BCK': 35,
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
