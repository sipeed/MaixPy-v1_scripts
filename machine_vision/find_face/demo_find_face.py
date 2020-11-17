
import sensor, image, lcd, time
import KPU as kpu
import gc, sys


def main(model_addr=0x300000, lcd_rotation=0, sensor_hmirror=False, sensor_vflip=False):
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_hmirror(sensor_hmirror)
    sensor.set_vflip(sensor_vflip)
    sensor.run(1)

    lcd.init(type=1)
    lcd.rotation(lcd_rotation)
    lcd.clear(lcd.WHITE)

    task = kpu.load(model_addr)
    anchors = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
    kpu.init_yolo2(task, 0.5, 0.3, 5, anchors) # threshold:[0,1], nms_value: [0, 1]
    try:
        while(True):
            img = sensor.snapshot()
            t = time.ticks_ms()
            objects = kpu.run_yolo2(task, img)
            t = time.ticks_ms() - t
            if objects:
                for obj in objects:
                    img.draw_rectangle(obj.rect())
            img.draw_string(0, 200, "t:%dms" %(t), scale=2)
            lcd.display(img)
    except Exception as e:
        sys.print_exception(e)
    finally:
        kpu.deinit(task)


if __name__ == "__main__":
    try:
        main( model_addr=0x300000, lcd_rotation=0, sensor_hmirror=False, sensor_vflip=False)
        # main(model_addr="/sd/m.kmodel")
    except Exception as e:
        sys.print_exception(e)
    finally:
        gc.collect()
