self learning classifier
=====


* Download firnware >= v0.5.0-33 [here](https://dl.sipeed.com/MAIX/MaixPy/release/master/maixpy_v0.5.0_33_gfcd6d8a)
* Download kmodel [here](https://www.maixhub.com/index.php/index/index/detail/id/225.html)
* Flash kmodel and firmware by [kflash_gui](https://github.com/sipeed/kflash_gui)
* Connect board to PC, open terminal tool like minicom, or use MaixPyIDE
* Run [demo script](self_learning_classifier.py)

Then you capture train image

* Push `boot button` to capture 3 classes like `phone`, `car`, `keyboard`, every one class only capture once
* Then capture 15 sample images, no cap order needed, you can capture 5 `phone`, 5 `car` and 5 `keyboard`
* Then it will automatically train the 15 sample images
* The image type will be displayed on the left top of screen

video on [youtube](https://www.youtube.com/watch?v=aLW1YQrT-2A) or [bilibili](https://www.bilibili.com/video/BV1Ck4y1d7tx)

## save/load

* Use `classifier.save(path)` to save trained data
* load by `KPU.classifier.load()`, refer to [self_learning_classifier_load.py](self_learning_classifier_load.py)

