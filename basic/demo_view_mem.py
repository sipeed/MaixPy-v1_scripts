import gc

print(gc.mem_free() / 1024) # stack mem

import Maix

print(Maix.utils.heap_free() / 1024) # heap mem

'''
>>> 
raw REPL; CTRL-B to exit
>OK
352.0937
4640.0
>
MicroPython v0.5.1-136-g039f72b6c-dirty on 2020-11-18; Sipeed_M1 with kendryte-k210
Type "help()" for more information.
>>> 
'''