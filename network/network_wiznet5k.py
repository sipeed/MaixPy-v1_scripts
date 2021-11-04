import network

class lan:

  nic = None

  def reset(spi1, cs, force=False, reply=5):
    if force == False and __class__.isconnected():
        return True
    try:
      #  create wiznet5k nic
      __class__.nic = network.WIZNET5K(spi=spi1, cs=cs)
      # time.sleep_ms(500) # wait at ready to connect
    except Exception as e:
        print(e)
        return False
    return True

  def ifconfig():  # should check ip != 0.0.0.0
    if __class__.nic != None:
        return __class__.nic.ifconfig()

  def isconnected():
    if __class__.nic != None:
        return __class__.nic.isconnected()
    return False

if __name__ == '__main__':

  from machine import SPI
  from Maix import GPIO
  import socket, time
  from fpioa_manager import fm

  ################ config ################
  local_ip = "192.168.0.117"
  local_netmask = "255.255.255.0"
  local_gateway = "255.255.255.0"
  local_dns_server = "8.8.8.8"

  server_ip = "192.168.0.141"
  server_port = 8000
  addr = (server_ip, server_port)
  #######################################

  def network_wiznet5k():
    if lan.isconnected() == False:
      WIZNET5K_SPI_SCK = 21
      WIZNET5K_SPI_MOSI = 8
      WIZNET5K_SPI_MISO = 15
      WIZNET5K_SPI_CS = 20
      spi1 = SPI(4, mode=SPI.MODE_MASTER, baudrate=600 * 1000,
                 polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=WIZNET5K_SPI_SCK, mosi=WIZNET5K_SPI_MOSI, miso=WIZNET5K_SPI_MISO)

      for i in range(5):
        try:
          lan.reset(spi1, WIZNET5K_SPI_CS)
          print('try connect lan...')
          if lan.isconnected():
            break
        except Exception as e:
          print(e)
    print('network state:', lan.isconnected(), lan.ifconfig())

  network_wiznet5k()

  if lan.isconnected():
    is_dhcp = False
    if is_dhcp:
      # #dhcp: Dynamic IP acquisition, It's not necessary
      while True:
        if(lan.nic.dhclient()):
          print("DHCP IP:", lan.ifconfig())
          break
    else:
      lan.ifconfig()

    ############################## UDP Test ##############################
    # # The server must first know the client's IP and port number through the message sent by the client before it send the message to the client
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)

    while True:
      sock.sendto("Client send: hello UDP\n".encode(), addr)
      try:
        data, addr1 = sock.recvfrom(10)
        print("Recv from server: ", data)
      except Exception as e:
        pass
      time.sleep_ms(500)
    sock.close()
    ############################ UDP Test end ############################

    ############################## TCP Test ##############################
    # The TCP server needs to be pre-started
    # sock = socket.socket()
    # sock.connect(addr)
    # while 1:
    #   sock.send("Client send: Hello TCP\n")
    #   try:
    #       data = sock.recv(10)
    #       print("Recv from Server: ", data)
    #   except Exception as e:
    #       print(e)
    #   time.sleep(500)
    #   sock.close()
    ############################ TCP Test end ############################
