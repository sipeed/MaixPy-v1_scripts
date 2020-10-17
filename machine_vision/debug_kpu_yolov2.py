
import sys, time, sensor, lcd

class camera:

    is_init = False
    is_dual_buff = False

    def init():
        sensor.reset(dual_buff=__class__.is_dual_buff)
        sensor.set_pixformat(sensor.RGB565)
        sensor.set_framesize(sensor.QVGA)
        sensor.set_windowing((320, 224))
        sensor.set_hmirror(1)
        sensor.set_vflip(1)
        sensor.run(1)
        sensor.skip_frames()

    def get_image():
        if __class__.is_init == False:
            __class__.init()
            __class__.is_init = True
        return sensor.snapshot()


import KPU as kpu

import lcd
lcd.init()

if __name__ == "__main__":

    with open("anchors.txt","r") as f:
        anchor_txt=f.read()
    #print(anchor_txt)
    anchor=tuple([float(i) for i in anchor_txt.split(",")])
    #print(anchor)

    with open("classes.txt","r") as f:
        labels_txt=f.read()
    #print(labels_txt)
    labels=tuple([str(i) for i in labels_txt.split(",")])
    #print(labels)

    import time
    last = time.ticks_ms()
    while True:
        try:
            #KpuTask = kpu.load(0x5C0000)
            KpuTask = kpu.load("/sd/yolov2.kmodel")
            kpu.init_yolo2(KpuTask, 0.6, 0.3, 5, anchor)
            while True:
                #print(time.ticks_ms() - last)
                last = time.ticks_ms()
                img = camera.get_image()
                things = kpu.run_yolo2(KpuTask, img)
                if things:

                    for pos in range(len(things)):
                        i = things[pos]
                        img.draw_rectangle(320 - (i.x() + i.w()), i.y(), i.w(), i.h())
                        img.draw_string(320 - (i.x() + i.w()), i.y(), '%.2f:%s' % (i.value(), labels[i.classid()]), color=(0, 255, 0))

                ## gc.collect() # have bug when reply 3
                lcd.display(img)
        except KeyboardInterrupt as e:
            pass
        finally:
            kpu.deinit(KpuTask)
            #break
