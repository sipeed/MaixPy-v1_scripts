import uos

mount_points = uos.listdir("/")
for fs in mount_points:
    print("------------")
    print(" dir:", fs)
    uos.listdir("/"+fs)

with open('main.py', 'rb') as f:
# 	f.write('print(Hello, world!)\r\n')
    print(f.read())
