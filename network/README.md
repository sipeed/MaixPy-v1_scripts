# Usage

## network

- [network_esp32.py](./network_esp32.py)
- [network_espat.py](./network_espat.py)
- [network_wiznet5k.py](./network_wiznet5k.py)

> 使用 MaixPy IDE 的菜单功能【发送文件到板子】即可作为一个类库使用。

Use the MaixPy IDE's menu functionality [send files to the board] as a class library.

```python
from network_esp32 import wifi

from network_espat import wifi

from network_wiznet5k import lan
```

## example

> 使用网卡连接到网络后才能进行以下操作。

Using the network card to connect to the network to make the following operation.

- [demo_esp32_ap_scan.py](./demo_esp32_ap_scan.py)
- [demo_esp32_ping.py](./demo_esp32_ping.py)

- [demo_espat_ap_scan.py](./demo_espat_ap_scan.py)

- [demo_socket_tcp_client.py](./demo_socket_tcp_client.py)
- (run your pc python3 not maixpy)[demo_socket_tcp_server.py](./demo_socket_tcp_server.py)

- [demo_socket_udp_client.py](./demo_socket_udp_client.py)
- (run your pc python3 not maixpy)[demo_socket_udp_server.py](./demo_socket_udp_server.py)

- [demo_socket_mqtt.py](./demo_socket_mqtt.py)

- [demo_http_get_jpg.py](./demo_http_get_jpg.py)
- [demo_socket_https.py](./demo_socket_https.py)

- [demo_socket_send_pic.py](./demo_socket_send_pic.py)
- (run your pc python3 not maixpy)[demo_socket_pic_server.py](./demo_socket_pic_server.py)

## other

- [demo_espat_ap_test.py](./demo_espat_ap_test.py)
- [espat_upgrade.py](./espat_upgrade.py)

- [demo_esp32_read_adc.py](./demo_esp32_read_adc.py)
