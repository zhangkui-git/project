a = []

for i in range(1, 10001):
    include = str(i).find("7")
    print(include)
    if include == -1 and int(i) % 7 != 0:
        a.append(i)

print(a)
file = open("data.txt", "w")
file.write(str(a))
file.close()




















