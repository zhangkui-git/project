
import sys
import os
import time
import random

used_mem = {}

# input_file = sys.argv[1]
input_file = "test.txt"

with open(input_file) as f:
    file_data = f.read()


# for i in range(0, int(sys.argv[2])):
for i in range(0, 200):
    print(i)
    used_mem[i] = file_data + str(random.randint(0, 1000))

print(111111, used_mem)

time.sleep(50)






