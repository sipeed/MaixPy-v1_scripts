import uos

mount_points = uos.listdir("/")
for fs in mount_points:
    print("------------")
    print(" dir:", fs)
    uos.listdir("/"+fs)


