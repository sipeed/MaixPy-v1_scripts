
import sys

while True:
    tmp = sys.stdin.read(1)
    if tmp == 'e':
        break
    sys.stdout.write(tmp)
