# Download model from: https://www.maixhub.com/index.php/index/index/detail/id/235
import sensor,image,lcd
import KPU as kpu
import time
from Maix import FPIOA,GPIO
task_fd = kpu.load(0x200000)
task_ld = kpu.load(0x300000) 
task_fe = kpu.load(0x400000) 
clock = time.clock()
key_pin=16
fpioa = FPIOA()
fpioa.set_function(key_pin,FPIOA.GPIO7)
key_gpio=GPIO(GPIO.GPIO7,GPIO.IN)
last_key_state=1
key_pressed=0
def check_key():
    global last_key_state
    global key_pressed 
    val=key_gpio.value()
    if last_key_state == 1 and val == 0:
        key_pressed=1
    else:
        key_pressed=0
    last_key_state = val

lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(1)
sensor.set_vflip(1)
sensor.run(1)
anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025) #anchor for face detect
dst_point = [(44,59),(84,59),(64,82),(47,105),(81,105)] #standard face key point position
a = kpu.init_yolo2(task_fd, 0.5, 0.3, 5, anchor)
img_lcd=image.Image()
img_face=image.Image(size=(128,128))
a=img_face.pix_to_ai()
record_ftr=[]
record_ftrs=[]
names = ['Mr.1', 'Mr.2', 'Mr.3', 'Mr.4', 'Mr.5', 'Mr.6', 'Mr.7', 'Mr.8', 'Mr.9' , 'Mr.10'] 
while(1):
    check_key()
    img = sensor.snapshot()
    clock.tick()
    code = kpu.run_yolo2(task_fd, img)
    if code:
        for i in code:
            # Cut face and resize to 128x128
            a = img.draw_rectangle(i.rect())
            face_cut=img.cut(i.x(),i.y(),i.w(),i.h())
            face_cut_128=face_cut.resize(128,128)
            a=face_cut_128.pix_to_ai()
            #a = img.draw_image(face_cut_128, (0,0))
            # Landmark for face 5 points
            fmap = kpu.forward(task_ld, face_cut_128)
            plist=fmap[:]
            le=(i.x()+int(plist[0]*i.w() - 10), i.y()+int(plist[1]*i.h()))
            re=(i.x()+int(plist[2]*i.w()), i.y()+int(plist[3]*i.h()))
            nose=(i.x()+int(plist[4]*i.w()), i.y()+int(plist[5]*i.h()))
            lm=(i.x()+int(plist[6]*i.w()), i.y()+int(plist[7]*i.h()))
            rm=(i.x()+int(plist[8]*i.w()), i.y()+int(plist[9]*i.h()))
            a = img.draw_circle(le[0], le[1], 4)
            a = img.draw_circle(re[0], re[1], 4)
            a = img.draw_circle(nose[0], nose[1], 4)
            a = img.draw_circle(lm[0], lm[1], 4)
            a = img.draw_circle(rm[0], rm[1], 4)
            # align face to standard position
            src_point = [le, re, nose, lm, rm]
            T=image.get_affine_transform(src_point, dst_point)
            a=image.warp_affine_ai(img, img_face, T)
            a=img_face.ai_to_pix()
            #a = img.draw_image(img_face, (128,0))
            del(face_cut_128)
            # calculate face feature vector
            fmap = kpu.forward(task_fe, img_face)
            feature=kpu.face_encode(fmap[:])
            reg_flag = False
            scores = []
            for j in range(len(record_ftrs)):
                score = kpu.face_compare(record_ftrs[j], feature)
                scores.append(score)
            max_score = 0
            index = 0
            for k in range(len(scores)):
                if max_score < scores[k]:
                    max_score = scores[k]
                    index = k
            if max_score > 85:
                a = img.draw_string(i.x(),i.y(), ("%s :%2.1f" % (names[index], max_score)), color=(0,255,0),scale=2)
            else:
                a = img.draw_string(i.x(),i.y(), ("X :%2.1f" % (max_score)), color=(255,0,0),scale=2)
            if key_pressed == 1:
                key_pressed = 0
                record_ftr = feature
                record_ftrs.append(record_ftr)
            break
    fps =clock.fps()
    print("%2.1f fps"%fps)
    a = lcd.display(img)
    #kpu.memtest()

#a = kpu.deinit(task_fe)
#a = kpu.deinit(task_ld)
#a = kpu.deinit(task_fd)
