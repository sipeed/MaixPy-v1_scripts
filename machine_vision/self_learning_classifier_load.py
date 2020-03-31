import KPU as kpu
import sensor
import lcd
import gc

############### config #################
saved_path = "3_classes.classifier"
THRESHOLD = 11
class_names = ['class1', 'class2', 'class3']
########################################

def draw_string(img, x, y, text, color, scale, bg=None ):
    if bg:
        img.draw_rectangle(x-2,y-2, len(text)*8*scale+4 , 16*scale, fill=True, color=bg)
    img = img.draw_string(x, y, text, color=color,scale=scale)
    return img


lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))

try:
    del model
except Exception:
    pass
try:
    del classifier
except Exception:
    pass
gc.collect()
model = kpu.load(0x300000)
classifier, class_num, sample_num = kpu.classifier.load(model, saved_path)

while 1:
    img = sensor.snapshot()
    res_index = -1
    try:
        res_index, min_dist = classifier.predict(img)
        print("{:.2f}".format(min_dist))
    except Exception as e:
        print("predict err:", e)
    if res_index >= 0 and min_dist < THRESHOLD :
        print("predict result:", class_names[res_index])
        img = draw_string(img, 2, 2, class_names[res_index], color=lcd.WHITE,scale=2, bg=lcd.RED)
    else:
        print("unknown, maybe:", class_names[res_index])
        img = draw_string(img, 2, 2, 'maybe {}'.format(class_names[res_index]), color=lcd.WHITE,scale=2, bg=lcd.RED)
    lcd.display(img)
