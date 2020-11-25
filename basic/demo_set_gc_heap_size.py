import machine
import Maix

gc_mem_size = 1024*1024

print('config micropython gc stack 1M (1024KB) if not')
if Maix.utils.gc_heap_size() != gc_mem_size:
    Maix.utils.gc_heap_size(gc_mem_size)
    print('updates take effect when you reboot the system. ')
    machine.reset()

print('Current: ', Maix.utils.gc_heap_size())

'''

[MAIXPY] Pll0:freq:806000000
[MAIXPY] Pll1:freq:398666666
[MAIXPY] Pll2:freq:45066666
[MAIXPY] cpu:freq:403000000
[MAIXPY] kpu:freq:398666666
[MAIXPY] Flash:0xef:0x17
[MaixPy] gc heap=0x800cbc50-0x8014bc50(524288)
[MaixPy] init end

 __  __              _____  __   __  _____   __     __
|  \/  |     /\     |_   _| \ \ / / |  __ \  \ \   / /
| \  / |    /  \      | |    \ V /  | |__) |  \ \_/ /
| |\/| |   / /\ \     | |     > <   |  ___/    \   /
| |  | |  / ____ \   _| |_   / . \  | |         | |
|_|  |_| /_/    \_\ |_____| /_/ \_\ |_|         |_|

Official Site : https://www.sipeed.com
Wiki          : https://maixpy.sipeed.com

MicroPython v0.5.1-136-g039f72b6c-dirty on 2020-11-18; Sipeed_M1 with kendryte-k210
Type "help()" for more information.
>>>
>>>
>>>
raw REPL; CTRL-B to exit
>OK
config micropython gc stack 1M (1024KB) if not
updates take effect when you reboot the s
[MAIXPY] Pll0:freq:806000000
[MAIXPY] Pll1:freq:398666666
[MAIXPY] Pll2:freq:45066666
[MAIXPY] cpu:freq:403000000
[MAIXPY] kpu:freq:398666666
[MAIXPY] Flash:0xef:0x17
[MaixPy] gc heap=0x800cbc50-0x801cbc50(1048576)
[MaixPy] init end

 __  __              _____  __   __  _____   __     __
|  \/  |     /\     |_   _| \ \ / / |  __ \  \ \   / /
| \  / |    /  \      | |    \ V /  | |__) |  \ \_/ /
| |\/| |   / /\ \     | |     > <   |  ___/    \   /
| |  | |  / ____ \   _| |_   / . \  | |         | |
|_|  |_| /_/    \_\ |_____| /_/ \_\ |_|         |_|

Official Site : https://www.sipeed.com
Wiki          : https://maixpy.sipeed.com

MicroPython v0.5.1-136-g039f72b6c-dirty on 2020-11-18; Sipeed_M1 with kendryte-k210
Type "help()" for more information.
>>>
'''
