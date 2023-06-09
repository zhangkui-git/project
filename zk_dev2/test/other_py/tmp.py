
list1 = [1, 2, 3, 4, 8]
list2 = [2, 3, 4, 5, 6]
list3 = [4, 5, 6, 7, 8]

print(list(map(lambda x, y, z: z if x < y < z else 'NO', list1, list2, list3)))


def add(num, b=1):
    return num + b


def get_num(func, arr):
    b = 0
    for i in arr:
        if func(i):
            b += i
    print(b)


a = lambda x: x % 8 == 0
arr = [2, 4, 16, 8]
get_num(a, arr)




































