s1 = 'abc'
s2 = 'bad'

b1 = {}
b2 = {}
if len(s1) == len(s2):
    if set(s1) == set(s2):
        a1 = list(set(s1))
        a2 = list(set(s2))
        for i in range(len(a1)):
            b1[a1[i]] = s1.count(a1[i])
            b2[a2[i]] = s2.count(a2[i])
        print(b1 == b2)
    else:
        print(22)
else:
    print(23)




