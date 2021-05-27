# 从 SPI FLASH 中加载并运行大模型
========

由于 K210 的 RAM 的运行机制，当需要加载大模型文件时，可以通过直接 Flash 中动态加载并运行

局限性：
* 从 flash 加载运行的速度，比正常运行慢
* 仅支持从内部 flash 加载，不支持从文件系统加载

## 用法示例

* 烧录[预处理的 kmodel 示例文件](../models/face_model_be_at_0x600000.kfpkg)(或者从[这里下载](https://dl.sipeed.com/MAIX/MaixPy/model))，然后使用 kflash_gui 烧录到 flash 中

* 在 MaixPy 上运行示例程序[demo_load_big_model.py](./demo_load_big_model.py)

* 与 [demo_find_face.py](../demo_find_face.py) 的区别是将 `kpu.load()` 更改为 `kpu.load_flash`, 相关参数如下：
  * `model_addr`: Flash addr 经过预处理的模型烧录到 flash 中的偏移地址。注意，这里需要预处理模型文件(第1步)。
  * `is_dual_buf`：`0`，单一缓冲区加载，使用较少的 RAM 和较慢的速度动态加载该模型文件；`1`，开启双缓冲加载，需要更大的 RAM， 运行速度相对较快。
  * `batch_size`：将`is_dual_buf`设置为 1 时，需要设置 load batch_size，建议值为`0x4000`~`0x10000`，可以测试出模型的最佳值。如果 is_dual_buf 为 0 则设置为 0
  * `spi_speed`：使用 SPI flash 加载模型文件时，我们会暂时将 flash 设置为高速模式，并设置所需的 spi 时钟频率。该值应 <= 80000000(实际频率，设置的值可能不等于实际频率。)


## 预处理模型文件

* 在 PC 上对 kmodel 模型文件进行预处理（对模型字节序进行翻转）

  ```shell
  cd MaixPy_scripts/machine_vision
  python3 model_le2be.py your_kmodel_path.kmodel #进行预处理
  ```

  如果需要从 flash 中动态加载模型文件时必须，使用预处理之后的`_be.kmodel` 模型文件，该命令将生成以`_be.kmodel`(`be`表示`big edian`) 结尾的 kmodel
* 烧录该预处理的模型文件，然后运行示例脚本
