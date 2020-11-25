import lvgl as lv

# lvgl must be initialized before any lvgl function is called or object/struct is constructed!

lv.init()

# Create a style based on style_plain but with a symbol font

symbolstyle = lv.style_t(lv.style_plain)
symbolstyle.text.font = lv.font_roboto_28

# The following two lines do the same thing.
# They show how to initialize struct either directly or through a dict

symbolstyle.text.color = lv.color_hex(0xffffff)
symbolstyle.text.color = lv.color_make(0xff, 0xff, 0xff)
if hasattr(symbolstyle.text.color.ch, 'alpha'):
    symbolstyle.text.color.ch.alpha = 0xff # Only has alpha when color is 32 bit

def get_member_name(obj, value):
    for member in dir(obj):
        if getattr(obj, member) == value:
            return member

class SymbolButton(lv.btn):
    def __init__(self, parent, symbol, text):
        super().__init__(parent)
        self.symbol = lv.label(self)
        self.symbol.set_text(symbol)
        self.symbol.set_style(lv.label.STYLE.MAIN, symbolstyle)
        
        self.label = lv.label(self)
        self.label.set_text(text)
        
class Page_Buttons:
    def __init__(self, app, page):
        self.app = app
        self.page = page

        self.btn1 = SymbolButton(page, lv.SYMBOL.PLAY, "Play")
        self.btn1.set_size(80,80)
        self.btn1.align(page, lv.ALIGN.IN_TOP_LEFT, 30, 30)
        
        self.btn2 = SymbolButton(page, lv.SYMBOL.PAUSE, "Pause")
        self.btn2.set_size(80,80)
        self.btn2.align(page, lv.ALIGN.IN_TOP_RIGHT, -30, 30)
    
        self.label = lv.label(page)
        self.label.align(page, lv.ALIGN.IN_BOTTOM_LEFT, 30, -30)

        # Currently only single callback per object is supported

        for btn, name in [(self.btn1, 'Play'), (self.btn2, 'Pause')]:
            btn.set_event_cb(lambda obj=None, event=-1, name=name: self.label.set_text('%s %s' % (name, get_member_name(lv.EVENT, event))))


class Page_Simple:
    def __init__(self, app, page):
        self.app = app
        self.page = page
        
        # slider 
        self.slider = lv.slider(page)
        self.slider.align(page, lv.ALIGN.IN_TOP_LEFT, 20, 20)
        self.slider_label = lv.label(page)
        self.slider_label.align(self.slider, lv.ALIGN.OUT_RIGHT_MID, 15, 0)
        self.slider.set_event_cb(self.on_slider_changed)
        self.on_slider_changed(None)
        
        # style selector
        self.styles = [('Plain', lv.style_plain), ('Plain color', lv.style_plain_color), ('Pretty', lv.style_pretty), ('Pretty color', lv.style_pretty_color)]
    
        self.style_selector = lv.ddlist(page)
        self.style_selector.align(self.slider, lv.ALIGN.IN_BOTTOM_LEFT, 0, 40)
        self.style_selector.set_options('\n'.join(x[0] for x in self.styles))
        self.style_selector.set_event_cb(self.on_style_selector_changed)

        # counter button
        self.counter_btn = lv.btn(page)
        self.counter_btn.set_size(80,80)
        self.counter_btn.align(self.style_selector, lv.ALIGN.OUT_RIGHT_TOP, 40, 0)
        self.counter_label = lv.label(self.counter_btn)
        self.counter_label.set_text('Count')
        self.counter_btn.set_event_cb(self.on_counter_btn)
        self.counter = 0

    
    def on_slider_changed(self, obj=None, event=-1):
        self.slider_label.set_text(str(self.slider.get_value()))

    def on_style_selector_changed(self, obj=None, event=-1):
        selected = self.style_selector.get_selected()
        self.app.screen_main.tabview.set_style(lv.tabview.STYLE.BG, self.styles[selected][1])   

    def on_counter_btn(self, obj, event):
        if event == lv.EVENT.CLICKED:
            self.counter += 1
            self.counter_label.set_text(str(self.counter))

class Anim(lv.anim_t):
    def __init__(self, obj, val, size, exec_cb, path_cb, time=500, playback = False, ready_cb=None):
        super().__init__()
        lv.anim_init(self)
        lv.anim_set_time(self, time, 0)
        lv.anim_set_values(self, val, val+size)
        if callable(exec_cb):
            lv.anim_set_custom_exec_cb(self, exec_cb)
        else:
            lv.anim_set_exec_cb(self, obj, exec_cb)
        lv.anim_set_path_cb(self, path_cb )
        if playback: lv.anim_set_playback(self, 0)
        if ready_cb: lv.anim_set_ready_cb(self, ready_cb)
        lv.anim_create(self)
        
class AnimatedChart(lv.chart):
    def __init__(self, parent, val, size):
        super().__init__(parent)
        self.val = val
        self.size = size
        self.max = 2000
        self.min = 500
        self.factor = 100
        self.anim_phase1()

    def anim_phase1(self):
        Anim(
            self,
            self.val,
            self.size,
            lambda a, val: self.set_range(0, val),
            lv.anim_path_ease_in,
            ready_cb=lambda a:self.anim_phase2(),
            time=(self.max * self.factor) // 100)

    def anim_phase2(self):
        Anim(
            self,
            self.val+self.size,
            -self.size,
            lambda a, val: self.set_range(0, val),
            lv.anim_path_ease_out,
            ready_cb=lambda a:self.anim_phase1(),
            time=(self.min * self.factor) // 100)


class Page_Chart():
    def __init__(self, app, page):
        self.app = app
        self.page = page
        self.chart = AnimatedChart(page, 100, 1000)
        self.chart.set_width(page.get_width() - 100)
        self.chart.align(page, lv.ALIGN.CENTER, 0, 0)
        self.series1 = self.chart.add_series(lv.color_hex(0xFF0000))
        self.chart.set_type(self.chart.TYPE.POINT | self.chart.TYPE.LINE)
        self.chart.set_series_width(3)
        self.chart.set_range(0,100)
        self.chart.init_points(self.series1, 10)
        self.chart.set_points(self.series1, [10,20,30,20,10,40,50,90,95,90])
        self.chart.set_x_tick_texts('a\nb\nc\nd\ne', 2, lv.chart.AXIS.DRAW_LAST_TICK)
        self.chart.set_x_tick_length(10, 5)
        self.chart.set_y_tick_texts('1\n2\n3\n4\n5', 2, lv.chart.AXIS.DRAW_LAST_TICK)
        self.chart.set_y_tick_length(10, 5)
        self.chart.set_div_line_count(3, 3)
        self.chart.set_margin(30)

        # Create a slider that controls the chart animation speed

        def on_slider_changed(obj=None, event=-1):
            self.chart.factor = self.slider.get_value()

        self.slider = lv.slider(page)
        self.slider.align(self.chart, lv.ALIGN.OUT_RIGHT_TOP, 10, 0)
        self.slider.set_width(30)
        self.slider.set_height(self.chart.get_height())
        self.slider.set_range(10, 200)
        self.slider.set_value(self.chart.factor, 0)
        self.slider.set_event_cb(on_slider_changed)

        
class Screen_Main(lv.obj):
    def __init__(self, app, *args, **kwds):
        self.app = app
        super().__init__(*args, **kwds)
        
        self.tabview = lv.tabview(self)
        self.page_simple = Page_Simple(self.app, self.tabview.add_tab('Simple'))
        self.page_buttons = Page_Buttons(self.app, self.tabview.add_tab('Buttons'))
        self.page_chart = Page_Chart(self.app, self.tabview.add_tab('Chart'))


class AdvancedDemoApplication():
    
    def init_gui(self):
        import lvgl as lv
        import lvgl_helper as lv_h
        import lcd
        import time
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

        # Create the main screen and load it.

        self.screen_main = Screen_Main(self)
        lv.scr_load(self.screen_main)

app = AdvancedDemoApplication()
app.init_gui()


from machine import Timer

def on_timer(timer):
	lv.tick_inc(5)

timer = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PERIODIC, period=5, unit=Timer.UNIT_MS, callback=on_timer, arg=None)

while True:
	tim = time.ticks_ms()
	lv.task_handler()
	while time.ticks_ms()-tim < 5:
		pass

