
SERVER_ADDR = "192.168.0.183"
SERVER_PORT = 8000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1)
while 1:
    try:
        sock.sendto("hello\n".encode(),(SERVER_ADDR, SERVER_PORT))
        data, addr = sock.recvfrom(1024)
    except Exception as e:
        print("receive error:", e)
        continue
    print("addr:", addr, "data:", data)
    time.sleep(2)

sock.close()
