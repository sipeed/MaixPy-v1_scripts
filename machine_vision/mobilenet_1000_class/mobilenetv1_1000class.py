# refer to http://blog.sipeed.com/p/680.html

import sensor, image, lcd, time
import KPU as kpu
import gc, sys


def main(labels = None, model_addr="/sd/m.kmodel", lcd_rotation=0, sensor_hmirror=False, sensor_vflip=False):
    gc.collect()

    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_windowing((224, 224))
    sensor.set_hmirror(sensor_hmirror)
    sensor.set_vflip(sensor_vflip)
    sensor.run(1)

    lcd.init(type=1)
    lcd.rotation(lcd_rotation)
    lcd.clear(lcd.WHITE)

    if not labels:
        raise Exception("no labels.txt")

    task = kpu.load(model_addr)

    try:
        while(True):
            img = sensor.snapshot()
            t = time.ticks_ms()
            fmap = kpu.forward(task, img)
            t = time.ticks_ms() - t
            plist=fmap[:]
            pmax=max(plist) 
            max_index=plist.index(pmax)
            img.draw_string(0,0, "%.2f\n%s" %(pmax, labels[max_index].strip()), scale=2, color=(255, 0, 0))
            img.draw_string(0, 200, "t:%dms" %(t), scale=2, color=(255, 0, 0))
            lcd.display(img)
    except Exception as e:
        sys.print_exception(e)
    finally:
        kpu.deinit(task)


if __name__ == "__main__":
    try:
        with open("labels.txt") as f:
            labels = f.readlines()
        main(labels=labels, model_addr=0x300000, lcd_rotation=0, sensor_hmirror=False, sensor_vflip=False)
        # main(labels=labels, model_addr="/sd/m.kmodel")
    except Exception as e:
        sys.print_exception(e)
    finally:
        gc.collect()
