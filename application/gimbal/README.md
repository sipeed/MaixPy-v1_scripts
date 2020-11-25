A gimbal demo (Servo)
======

Two(/Tree) axies servo gimbal

Servo parameters:

* freq: 50 (Hz)
* T:    1/50 = 0.02s = 20ms
* duty: [0.5ms, 2.5ms] -> [0.025, 0.125] -> [2.5%, 12.5%]
* pins:
  * IO24 <--> pitch
  * IO25 <--> roll

Usage:

* Use `face_model`([face_model_at_0x300000.kfpkg](https://dl.sipeed.com/MAIX/MaixPy/model)) to detect face
* Change parameters according to your gimbal hardware( code at the start of the `main`), like direction of `camera` and `lcd`, and `PID` parameters
* Run script

demo video:

[![](maixpy_gimbal.png)](https://wiki.sipeed.com/maixpy_gimbal.mp4)

<video src="gimbal.mp4" controls="controls" preload="auto">not support play video</video>


