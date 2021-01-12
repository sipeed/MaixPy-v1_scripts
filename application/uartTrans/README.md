# UartTrans

自定义串口传输数据格式, 可用来传输指令（接收到指令执行用户注册的回调函数）或数据, 采用 crc16 校验

## 协议详情

| 2Byte | 1Byte        | 2Byte    | nByte | 2Byte   | 2Byte |
| :---- | :----------- | :------- | :---- | :------ | :---- |
| 起始  | 指令或者数据    | 数据数量  | 数据   | CRC校验  | 结束  |

* 起始: 0xaaff

* 数据类型: 1. 指令 0. 数据

* 数据数量: 16bit

* CRC16校验: (H)

* 结束: 0xddff(H)

## 快速开始

* 导入模块

```python
import UartTrans # import 
```

* 创建 UartTrans

```python
fm.register(22, fm.fpioa.UART1_TX, force=True)
fm.register(21, fm.fpioa.UART1_RX, force=True)
uart1 = UART(UART.UART1, 115200, 8, 1, 0, timeout=1000, read_buf_len=4096)
uart_t = UartTrans(uart1)
```

* 自定义函数并为其注册指令

```python
def cus_cmd(uart, s):
    print("execute cus cmd {}".format(s))
    uart.write("execute cus cmd {}".format(s))

uart_t.reg_cmd("cus", cus_cmd, uart1, 'hello') # 注册当接收到指令 'cus' 时执行 cus_cmd， 该函数参数为 uart1，'hello'
```

* 发送指令或字符串

```python
uart_t.write('cus', True) # send 'cus' cmd
uart_t.write('hello') # send 'hello'data
```

* 发送数字（`pack_num` 使用请查看[pack_num API](#pack_num)）

```python
nums = pack_num(3.1415, 'f') + pack_num(16, 'H') + pack_num(-8, 'b') # pack num data
uart_t.write(nums) # send num 3.1415(float) 16(uint16) -8(int8)
```

* 接收指令或数据

```python
udatas = uart_t.read()
```

* 执行接收的指令, 返回接收到的数据

```python
d = uart_t.parse(udatas)
```

## API: UartTrans

### 注册指令

注册新指令并设置回调, 若指令已存在, 则会覆盖.

```python
reg_cmd(cmd, fun, *args):
```

#### 参数

* `cmd` 指令名, 字符串类型 
* `fun` 指令回调函数
* `*args` 回调函数参数

#### 返回值

无


### 注销指令

```python
unreg_cmd(cmd):
```

#### 参数

`cmd` 指令名, 字符串类型.

#### 返回值

无

### 发送指令或数据

```python
write(s, is_cmd)
```

#### 参数

`s` 要发送的字符串, 打包好的数字, 指令(也是字符串), `is_cmd` 是否以指令的形式发送

#### 返回值

无

### 打包数字<div id="pack_num"></div>

将数字打包成传输格式

```python
pack_num(n, fl)
```

#### 参数
 
 * `n` 数字
 * `fl` 数字类型, uint8_t(B), int8_t(b), uint16_t(H), int16_t(h), uint32_t(I), int32_t(i), uint64_t(Q), int64_t(q), float(f), double(d), str(s)

#### 返回值

打包后的数字

#### 示例

将3.1415打包成float类型后发送

```python
pi = uart_t.pack_num(3.1415, 'f')
uart_t.write(pi)
```

### 接收指令或数据

读取数据、指令并解析后返回

```python
read()
```

#### 返回值

接收到的数据或指令列表, 格式为二维列表: `[[is_cmd, data]]` is_cmd: data 是否为指令(1), 数据(0), data: 数据或指令本身.
未接收到数据则为空列表

### 解析数据

将 read 得到的数据进行解析, 若为指令, 指令已注册则立即执行指令对应回调函数, 不存在将打印提醒信息, 若为数据, 将数据存储在列表中返回

```python
parse(udatas)
```

#### 参数
`udatas` read 得到的数据

#### 返回值

列表, 解析后的数据列表

#### 示例

读取数据、指令并解析

```python
udatas = uart_t.read()
uart_t.parse(udatas)
```
## 格式示例

1. 字符串 `aaaaaaaaaaaaaaaaaaa`

> 串口接收:  DD FF 00 00 13 61 61 61 61 61 61 61 61 61 61 61 61 61 61 61 61 61 61 61 CE 3A AA FF
> 
> 分析:
> 
> DD FF: head
> 
> 00: data type
> 
> 00 13： data len
> 
> 61 ... 61: data
> 
> CE 3A: crc16
> 
> AA FF: end
> 
> read 后数据:
> 
> ```python
> [(0, b'aaaaaaaaaaaaaaaaaaa')] # type: data
> ```
> 
> parse 后数据:
> 
> ```python
> ['aaaaaaaaaaaaaaaaaaa']
> ```

2. 数字 `3.1415, 16, -8` 

> 串口接收到:  DD FF 00 00 0A 66 40 49 0E 56 48 00 10 62 F8 4C E0 AA FF 
> 
> 分析:
> 
> DD FF: head
> 
> 00: data type
> 
> 0A: data len
> 
> 66: 'f' float
> 
> 40 49 0e 56: 3.1415
> 
> 48: 'H' uint16_t
> 
> 00 10: 16
> 
> 62: 'b' int8_t
> 
> F8: -8
> 
> 4C E0: crc16
> 
> AA FF: end
> 
> read 后数据:
> 
> ```python
> [(0, b'f@I\x0eVH\x00\x10b\xf8')] # type: data
> ```
> 
> parse 后数据:
> 
> ```python
> [[3.1415, 16, -8]]
> ```

3. 指令 `cus`

> 串口接收到: DD FF 01 00 03 63 75 73 E6 AB AA FF
> 
> 分析:
> 
> DD FF: head
> 
> 00: data type
> 
> 0A: data len
> 
> 66: 'f' float
> 
> 40 49 0e 56: 3.1415
> 
> 48: 'H' uint16_t
> 
> 00 10: 16
> 
> 62: 'b' int8_t
> 
> F8: -8
> 
> 4C E0: crc16
> 
> AA DD: end
> 
> read 后数据:
> 
> ```python
> [(1, b'cus')] # type: cmd
> ```
> 
> parse 后数据:
> 
> 该条数据为指令类型, parse直接执行该指令回调函数
