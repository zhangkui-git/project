from collections import Counter

list_1 = ['hh', "hh", "k", "f"]
counter = Counter(list_1)
print(counter.values())
print(counter.get('hh'))
# for i in counter.values():
#     print(i)

