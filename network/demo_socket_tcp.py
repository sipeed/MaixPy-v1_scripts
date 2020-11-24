

SERVER_ADDR = "192.168.0.113"
SERVER_PORT = 60000

sock = socket.socket()
sock.connect((SERVER_ADDR, SERVER_PORT))

sock.settimeout(5)
while 1:
    try:
        sock.send("hello\n")
        data = sock.recv(10)
        if len(data) == 0:
            continue
        print("rcv:", len(data), data)
    except Exception as e:
        print("receive error:", e)
        continue
    time.sleep(2)

sock.close()


SERVER_ADDR = "192.168.0.113"
SERVER_PORT = 60000
sock = socket.socket()
sock.connect((SERVER_ADDR, SERVER_PORT))

sock.settimeout(3)
while 1:
    sock.send("hello\n")
    #data = sock.recv(10) # old maxipy have bug (recv timeout no return last data)
    #print(data) # fix
    try:
      data = b""
      while True:
        tmp = sock.recv(1)
        #print(tmp)
        if len(tmp) == 0:
            raise Exception('timeout or disconnected')
        data += tmp
    except Exception as e:
      print("rcv:", len(data), data)
    #time.sleep(2)

sock.close()
