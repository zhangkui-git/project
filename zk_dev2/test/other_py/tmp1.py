var1 = 10
var2 = var1
var1 = 20
print(var1, var2)


list1 = [1, 2, 3, 4, 8]
list2 = [2, 3, 4, 5, 6]
print(list(map(lambda x, y: x if x < y else 'NO', list1, list2)))


import time


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        exec_time = time.time() - start_time
        print(func.__name__, "函数，花费的时间是:", exec_time)
        return res
    return wrapper


@timer
def add(a, b):
    return a + b


@timer
def sub(a, b):
    return a - b


add(1, 2)
sub(1, 2)


















