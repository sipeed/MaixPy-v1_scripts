import time
from machine import WDT

# '''
# test default wdt
wdt0 = WDT(id=0, timeout=3000)
print('into', wdt0)
time.sleep(2)
print(time.ticks_ms())
# 1.test wdt feed
wdt0.feed()
time.sleep(2)
print(time.ticks_ms())
# 2.test wdt stop
wdt0.stop()
print('stop', wdt0)
# 3.wait wdt work
#while True:
    #print('idle', time.ticks_ms())
    #time.sleep(1)
# '''

# '''
def on_wdt(self):
    print(self.context(), self)
    #self.feed()
    ## release WDT
    #self.stop()

# test callback wdt
wdt1 = WDT(id=1, timeout=4000, callback=on_wdt, context={})
print('into', wdt1)
time.sleep(2)
print(time.ticks_ms())
# 1.test wdt feed
wdt1.feed()
time.sleep(2)
print(time.ticks_ms())
# 2.test wdt stop
wdt1.stop()
print('stop', wdt1)
# 3.wait wdt work
#while True:
    #print('idle', time.ticks_ms())
    #time.sleep(1)
# '''

#'''
## test default and callback wdt
def on_wdt(self):
    print(self.context(), self)
    #self.feed()
    ## release WDT
    #self.stop()

wdt0 = WDT(id=0, timeout=3000, callback=on_wdt, context=[])
wdt1 = WDT(id=1, timeout=4000, callback=on_wdt, context={})
## 3.wait wdt work
while True:
    #wdt0.feed()
    print('idle', time.ticks_ms())
    time.sleep(1)
#'''