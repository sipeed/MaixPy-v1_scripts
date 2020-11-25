import time
import machine

print(time.time())
t1 = time.localtime(546450051)
print('t1', t1)
t2 = time.mktime(t1)
print('t2', t2)
print(time.time())
time.set_time(t1)
print(time.time())
time.sleep(1)
print(time.localtime(time.time()))

'''
raw REPL; CTRL-B to exit
>OK
74
t1 (2017, 4, 25, 15, 40, 51, 1, 115)
t2 546450051
546450065
546450051
(2017, 4, 25, 15, 40, 52, 1, 115)
>
MicroPython v0.5.1-136-g039f72b6c-dirty on 2020-11-18; Sipeed_M1 with kendryte-k210
Type "help()" for more information.
>>>
>>>
'''
