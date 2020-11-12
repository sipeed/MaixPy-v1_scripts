import json

config = {
  "type": "bit",
  "board_info": {
      'BOOT_KEY': 16,
      'LED_R': 13,
      'LED_G': 12,
      'LED_B': 14,
      'MIC0_WS': 19,
      'MIC0_DATA': 20,
      'MIC0_BCK': 18,
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
