Mobilenet V1 1000 classes classifier
==========


* Download model from https://dl.sipeed.com/MAIX/MaixPy/model , download `mobilenet_0x300000.kfpkg`
* And [labels.txt](./labels.txt)
* To make sure have enough memory for this `4.2MiB` model, so use `minimum` version firmware
* Reduce GC heap size by 
```python
from Maix import utils
import machine

utils.gc_heap_size(256*1024)
machine.reset()
```
* Run [script](.mobilenetv1_1000class.py)

More doc see[doc](maixpy.sipeed.com)

