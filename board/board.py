
class board_info:
  def set(key, value=None):
    return setattr(__class__, key, value)
  def all():
    return dir(__class__)
  def get():
    return getattr(__class__, key)
  def load(__map__={}):
    for k, v in __map__.items():
      __class__.set(k, v)

from Maix import config
tmp = config.get_value('board_info', None)
if tmp != None:
    board_info.load(tmp)
else:
    print('[Warning] Not loaded from /flash/config.json to board_info.')

if __name__ == "__main__":
  def check_config_json(data):
    try:
      with open('/flash/config.json', 'rb') as f:
        tmp = json.loads(f.read())
        if tmp["type"] != data["type"]:
          raise Exception('config.json no exist')
    except Exception as e:
      with open('/flash/config.json', "w") as f:
        f.write(cfg)
      import machine
      machine.reset()

  print(board_info.all())
  board_info.set('test', 123)
  print(board_info.test)
  print(board_info.all())

  import json
  test = {
      "type": "test",
      "board_info": {
          'PIN10': 10,
          'BOOT_KEY': 16,
          'WIFI_TX': 6,
          'WIFI_RX': 7,
          'WIFI_EN': 8,
      }
  }
  cfg = json.dumps(test)
  check_config_json(test)
  from Maix import config
  tmp = config.get_value('board_info', None)
  if tmp != None:
    board_info.load(tmp)
  print(board_info.all())
  print(board_info.PIN10)
  print(board_info.BOOT_KEY)
  print(board_info.WIFI_TX)
  print(board_info.WIFI_RX)
  print(board_info.WIFI_EN)
