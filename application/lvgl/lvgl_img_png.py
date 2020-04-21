
# init


import lvgl as lv
import lvgl_helper as lv_h
import lodepng as png
import lcd
import time
import ustruct as struct
from machine import Timer
from machine import I2C

config_touchscreen_support = True
board_m1n = False
   
i2c = I2C(I2C.I2C0, freq=400000, scl=30, sda=31)
if not board_m1n:
	lcd.init()
else:
	lcd.init(type=2, freq=20000000)
if config_touchscreen_support:
	import touchscreen as ts
	ts.init(i2c)
lv.init()

disp_buf1 = lv.disp_buf_t()
buf1_1 = bytearray(320*10)
lv.disp_buf_init(disp_buf1,buf1_1, None, len(buf1_1)//4)
disp_drv = lv.disp_drv_t()
lv.disp_drv_init(disp_drv)
disp_drv.buffer = disp_buf1
disp_drv.flush_cb = lv_h.flush
if board_m1n:
    disp_drv.hor_res = 240
    disp_drv.ver_res = 240
else:
    disp_drv.hor_res = 320
    disp_drv.ver_res = 240
lv.disp_drv_register(disp_drv)

if config_touchscreen_support:
	indev_drv = lv.indev_drv_t()
	lv.indev_drv_init(indev_drv) 
	indev_drv.type = lv.INDEV_TYPE.POINTER
	indev_drv.read_cb = lv_h.read
	lv.indev_drv_register(indev_drv)

# lv.log_register_print_cb(lv_h.log)
lv.log_register_print_cb(lambda level,path,line,msg: print('%s(%d): %s' % (path, line, msg)))


COLOR_SIZE = lv.color_t.SIZE
COLOR_IS_SWAPPED = hasattr(lv.color_t().ch,'green_h')
class lodepng_error(RuntimeError):
    def __init__(self, err):
        if type(err) is int:
            super().__init__(png.error_text(err))
        else:
            super().__init__(err)

# Parse PNG file header
# Taken from https://github.com/shibukawa/imagesize_py/blob/ffef30c1a4715c5acf90e8945ceb77f4a2ed2d45/imagesize.py#L63-L85

def get_png_info(decoder, src, header):
    # Only handle variable image types

    if lv.img.src_get_type(src) != lv.img.SRC.VARIABLE:
        return lv.RES.INV

    png_header = bytes(lv.img_dsc_t.cast(src).data.__dereference__(24))

    if png_header.startswith(b'\211PNG\r\n\032\n'):
        if png_header[12:16] == b'IHDR':
            start = 16
        # Maybe this is for an older PNG version.
        else:
            start = 8
        try:
            width, height = struct.unpack(">LL", png_header[start:start+8])
        except struct.error:
            return lv.RES.INV
    else:
        return lv.RES.INV

    header.always_zero = 0
    header.w = width
    header.h = height
    header.cf = lv.img.CF.TRUE_COLOR_ALPHA

    return lv.RES.OK

# Convert color formats

def convert_rgba8888_to_bgra5658(img_view):
    img_size = int(len(img_view)) // 4
    p = img_view
    j = 0
    for i in range(img_size):
        r = p[i*4]
        g = p[i*4 + 1]
        b = p[i*4 + 2]
        a = p[i*4 + 3]
        j = i*3
        p[j] = \
            ((b & 0b11111000) >> 3) |\
            ((g & 0b00011100) << 3)
        p[j + 1] = \
            ((g & 0b11100000) >> 5) |\
            ((r & 0b11111000) )
        p[j + 2] = a

# Read and parse PNG file
def open_png(decoder, dsc):
    img_dsc = lv.img_dsc_t.cast(dsc.src)
    png_data = img_dsc.data
    png_size = img_dsc.data_size
    png_decoded = png.C_Pointer()
    png_width = png.C_Pointer()
    png_height = png.C_Pointer()
    error = png.decode32(png_decoded, png_width, png_height, png_data, png_size)
    if error:
        raise lodepng_error(error)
    img_size = png_width.int_val * png_height.int_val * 4
    img_data = png_decoded.ptr_val
    img_view = img_data.__dereference__(img_size)
    # convert_rgba8888_to_bgra5658(img_view)
    lv_h.rgba8888_to_5658(img_view)

    dsc.img_data = img_data
    return lv.RES.OK

# Register new image decoder

decoder = lv.img.decoder_create()
decoder.info_cb = get_png_info
decoder.open_cb = open_png

# Create a screen with a draggable image

with open('png_decoder_test.png','rb') as f:
  png_data = f.read()

png_img_dsc = lv.img_dsc_t({
    'data_size': len(png_data),
    'data': png_data 
})

scr = lv.obj()

# Create an image on the left using the decoder

lv.img.cache_set_size(2)
img1 = lv.img(scr)
img1.align(scr, lv.ALIGN.IN_LEFT_MID, -50, 0)
img1.set_src(png_img_dsc)
img1.set_drag(True)

# Create an image on the right directly without the decoder

img2 = lv.img(scr)
img2.align(scr, lv.ALIGN.CENTER, 0, 0)
raw_dsc = lv.img_dsc_t()
get_png_info(None, png_img_dsc, raw_dsc.header)
dsc = lv.img_decoder_dsc_t({'src': png_img_dsc})
if open_png(None, dsc) == lv.RES.OK:
    raw_dsc.data = dsc.img_data
    raw_dsc.data_size = raw_dsc.header.w * raw_dsc.header.h * lv.color_t.SIZE
    img2.set_src(raw_dsc)
    img2.set_drag(True)

# Load the screen and display image

lv.scr_load(scr)

def on_timer(timer):
	lv.tick_inc(5)
	
timer = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PERIODIC, period=5, unit=Timer.UNIT_MS, callback=on_timer, arg=None)

while True:
	tim = time.ticks_ms()
	lv.task_handler()
	while time.ticks_ms()-tim < 5:
		pass


