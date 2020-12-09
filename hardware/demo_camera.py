import sensor, lcd

try:
    sensor.reset()
except Exception as e:
    raise Exception("sensor reset fail, please check hardware connection, or hardware damaged! err: {}".format(e))
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
# sensor.set_hmirror(1) # cube & amigo
# sensor.set_vflip(1) # cube & amigo
sensor.run(1)
sensor.skip_frames()
lcd.init(freq=15000000)

while(True):
    lcd.display(sensor.snapshot())

