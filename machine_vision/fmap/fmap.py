import sensor,lcd,image
import KPU as kpu
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))	#set to 224x224 input
sensor.set_hmirror(0)				#flip camera
task = kpu.load(0x300000)			#load model from flash address 0x200000

img_lcd=image.Image()
img_lcd = img_lcd.to_grayscale()
while True:
    img2 = sensor.snapshot()
    #lcd.display(img,oft=(0,0))		#display large picture
    img2=img2.to_grayscale()		#convert to gray
    img2=img2.resize(28,28)			#resize to mnist input 28x28
    a=img2.invert()					#invert picture as mnist need
    # a=img2.strech_char(1)			#preprocessing pictures, eliminate dark corner
    img2x2=img2.resize(28*2,28*2)	#scale to display
    a = img_lcd.draw_image(img2x2,0,0)#display small 28x28 picture
    a=img2.pix_to_ai();				#generate data for ai
    #watch conv0
    a=kpu.set_layers(task, 1)			
    fmap=kpu.forward(task,img2)		#run neural network model
    for i in range(0,16):
        tmp=kpu.fmap(fmap,i)
        tmpx2=tmp.resize(14*2,14*2) #scale to display
        a=img_lcd.draw_image(tmpx2,(i%8)*14*2,28*2+14*2*int(i/8))
    #watch conv1
    a=kpu.set_layers(task, 2)			
    fmap=kpu.forward(task,img2)		#run neural network model
    for i in range(0,32):
        tmp=kpu.fmap(fmap,i)
        tmpx2=tmp.resize(7*2,7*2)   #scale to display
        a=img_lcd.draw_image(tmpx2,(i%16)*7*2,28*2+14*2*2+7*2*int(i/16))
    #watch conv2
    a=kpu.set_layers(task, 8)			
    fmap=kpu.forward(task,img2)		#run neural network model
    for i in range(0,10):
        tmp=kpu.fmap(fmap,i)
        tmpx2=tmp.resize(4*2,4*2)   #scale to display
        a=img_lcd.draw_image(tmpx2,i*4*2,28*2+14*2*2+7*2*2)
    #watch softmax
    a=kpu.set_layers(task, 11)
    fmap=kpu.forward(task,img2)	
    plist=fmap[:]
    for i in range(0,10):
        cc = int(plist[i]*256)
    lcd.display(img_lcd)
