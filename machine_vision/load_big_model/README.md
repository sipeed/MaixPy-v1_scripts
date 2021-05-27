load big kmodel
========

If your model is too big(size), you can use this way to load it dynamically from flash

Limitations:
* Slower than normal run
* Only support load from flash, from file system is not supported

## Example usage

* Burn [preprocessed kmodel](../models/face_model_be_at_0x600000.kfpkg) (or download [here](https://dl.sipeed.com/MAIX/MaixPy/model)) to flash by kflash_gui
* Run [demo_load_big_model.py](./demo_load_big_model.py) on MaixPy
* The difference from [demo_find_face.py](../demo_find_face.py) is `kpu.load()` changed to `kpu.load_flash`, the parameters: 
  * `model_addr`: flash addr store your model, note, you need flip the model endian(step 1).
  * `is_dual_buf`: `0`, single buf, use less ram and slower speed; `1`, dual buf, more ram and faster speed.
  * `batch_size`: when set `is_dual_buf` to 1, you need set load batch_size, suggestion value is `0x4000`~`0x10000`, you can test out best value for your model. set to 0 if `is_dual_buf` is 0
  * `spi_speed`: when use flash runner, we will temporary set flash to high speed mode, set the spi speed you want. the value should <= 80000000 (actual frequency, value set may not equal to actual freq.)


## Run your model

* Preprocess kmodel on PC
```
  cd MaixPy_scripts/machine_vision
  python3 model_le2be.py your_kmodel_path.kmodel
```
this command will generate a kmodel ends with `_be.kmodel`(`be` means `big edian`),
you **MUST** use this model if you use `kpu.load_flash()` API

* Burn this kmodel to flash, and run your script







