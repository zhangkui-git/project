
foo = [21, 38, 38, 56, 23, 19, 11, 15, 19, 13, 20, 6, 0, 8, 0, 10, 11, 0, 11, 8, 12, 5]

# 第一种
a = ','.join(map(str, foo))
print(111, a)


# 第二种
bar = ''.join(str(i) for i in foo)
print(222, bar)