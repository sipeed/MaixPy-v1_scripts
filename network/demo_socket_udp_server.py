import socket
BUFSIZE = 1024
ip_port = ('0.0.0.0', 60000)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # udp 
server.bind(ip_port)
while True:
    data,client_addr = server.recvfrom(BUFSIZE)
    print('server recv', data)
    server.sendto(data.upper(),client_addr)
server.close()

'''
('server recv', 'hello\n')
('server recv', 'hello\n')
('server recv', 'hello\n')
('server recv', 'hello\n')
('server recv', 'hello\n')
('server recv', 'hello\n')
'''
