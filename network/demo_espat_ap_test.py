# This file is part of MaixPY
# Copyright (c) sipeed.com
#
# Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#

from network_espat import wifi
wifi.reset()

print(wifi.at_cmd("AT\r\n"))
print(wifi.at_cmd("AT+GMR\r\n"))

'''
>>> reset...
b'\r\n\r\nOK\r\n'
b'AT version:1.1.0.0(May 11 2016 18:09:56)\r\nSDK version:1.5.4(baaeaebb)\r\ncompile time:May 20 2016 15:06:44\r\nOK\r\n'
MicroPython v0.5.1-136-g039f72b6c-dirty on 2020-11-18; Sipeed_M1 with kendryte-k210
Type "help()" for more information.
>>>
'''
