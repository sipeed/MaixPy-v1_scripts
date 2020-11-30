'''
This is a testing program
the program is used to start server
'''
import socket
import sys
import time

def start_tcp_server(ip, port):
    #create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, port)
    #bind port
    print('starting listen on ip %s, port %s' % server_address)
    sock.bind(server_address)
    #starting listening, allow only one connection
    try:
        sock.listen(1)
    except socket.error as e:
        print("fail to listen on port %s" % e)
        sys.exit(1)
    while True:
        print("waiting for connection")
        client, addr = sock.accept()
        print('having a connection')
        for i in range(5):
          print('send message')
          client.send(b'I am server')
          print(client.recv(6))
        print('send OSError: [Errno 128(32)] ENOTCONN')
        client.close()

if __name__ == '__main__':
    start_tcp_server('0.0.0.0', 60000)
