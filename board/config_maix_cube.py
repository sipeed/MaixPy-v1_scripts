import json

config = {
    "type": "cube",
    "lcd": {
        "height": 240,
        "width": 240,
        "invert": 1,
        "dir": 96
    },
    "board_info": {
        'BOOT_KEY': 16,
        'LED_R': 13,
        'LED_G': 12,
        'LED_B': 14,
        'LED_W': 32,
        'BACK': 11,
        'ENTER': 10,
        'NEXT': 16,
        'WIFI_TX': 6,
        'WIFI_RX': 7,
        'WIFI_EN': 8,
        'I2S0_MCLK': 19,
        'I2S0_SCLK': 35,
        'I2S0_WS': 33,
        'I2S0_IN_D0': 34,
        'I2S0_OUT_D2': 18,
        'I2C_SDA': 31,
        'I2C_SCL': 30,
        'SPI_SCLK': 21,
        'SPI_MOSI': 8,
        'SPI_MISO': 15,
        'SPI_CS': 20,
    }
}

cfg = json.dumps(config)
print(cfg)

# config lcd back_light
try:
    os.remove('/flash/boot.py')
except:
    pass
with open('/flash/boot.py', 'wb') as f:
    cfg_sensor = b'from fpioa_manager import fm\nfrom Maix import GPIO\nfm.register(17, fm.fpioa.GPIOHS28)\nlcd_en = GPIO(GPIO.GPIOHS28, GPIO.OUT)\nlcd_en.value(0)\n'
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
