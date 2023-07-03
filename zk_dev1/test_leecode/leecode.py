
# -----------------------2022.7.4

# arr = [4, 2, 1, 3]
arr = [-85094,85888,11307,-46123,-11703,15548,15901,-79359,43432,-4189]
index_arr = []
data_arr = []

for i in range(len(arr) - 1):
    for j in range(i + 1, len(arr)):
        tmp_data = []
        index_arr.append(abs(arr[i] - arr[j]))
        if arr[i] - arr[j] >= 0:
            tmp_data.append(arr[j])
            tmp_data.append(arr[i])
        else:
            tmp_data.append(arr[i])
            tmp_data.append(arr[j])
        data_arr.append(tmp_data)

print("记录计算的数组----", data_arr)
print("记录计算的数组对应的结果----", index_arr)
index_arr_a = []
for h, f in enumerate(index_arr):
    tmp_a = [h, f]
    index_arr_a.append(tmp_a)
print("记录绝对值索引和结果为-----", index_arr_a)

index_arr.sort()
tmp_index_arr = index_arr[0]

data_arr_index = []
for z in index_arr_a:
    if z[1] == tmp_index_arr:
        data_arr_index.append(z[0])
print("记录计算结果为最小的数组索引----", data_arr_index)

new_data_arr = []
for k in data_arr_index:
    new_data_arr.append(data_arr[k])

print("得到计算结果为最小的数组----", new_data_arr)


new_data_arr_index = []
for x, y in enumerate(new_data_arr):
    tmp_new_data_arr = [x, y[0]]
    new_data_arr_index.append(tmp_new_data_arr)


def fun(new_data_arr_index):
    return new_data_arr_index[1]


new_data_arr_index.sort(key=fun)

print("得到结算结果为最小数组的索引和数组的第一个数----", new_data_arr_index)

sta_new_data_arr_index = []
for o, p in enumerate(new_data_arr_index):
    sta_new_data_arr_index.append(p[0])
print(sta_new_data_arr_index)

end_new_data_arr = []
for s in sta_new_data_arr_index:
    end_new_data_arr.append(new_data_arr[s])

print("最终结果为---", end_new_data_arr)

# 结果----------
class Solution:
    def minimumAbsDifference(self, arr: List[int]) -> List[List[int]]:
        arr = sorted(arr)
        res = []
        mindff = arr[-1] - arr[0]
        for i in range(len(arr)-1):
            if arr[i+1] - arr[i] < mindff:
                mindff = arr[i+1] - arr[i]
                res = []
                res.append([arr[i], arr[i+1]])
            elif arr[i+1] - arr[i] == mindff:
                res.append([arr[i], arr[i+1]])
        return res


# -----------------------2022-7-5

import bisect


class MyCalendar:
    def __init__(self):
        self.lst = []

    def book(self, start, end):
        if not self.lst:
            print("真还是假--------", not self.lst)
            bisect.insort(self.lst, start)
            bisect.insort(self.lst, end)
            print("1----", self.lst)
            return True
        idx = bisect.bisect_right(self.lst, start)
        if idx == len(self.lst) or idx % 2 == 0 and self.lst[idx] >= end:
            bisect.insort(self.lst, start)
            bisect.insort(self.lst, end)
            print("2----", self.lst)
            return True
        return False


res = MyCalendar()
res1 = res.book(1, 10)
res2 = res.book(7, 15)
res3 = res.book(10, 19)
res4 = res.book(19, 23)
print(res1, res2, res3, res4)

# ----------------20220708

class Solution:
    def replaceWords(self, dictionary: List[str], sentence: str) -> str:
        # # 按字节长度对字典排序
        # dictionary = sorted(dictionary, key=lambda x: len(x))
        # # 将sentence转为列表
        # sentence = sentence.split(' ')
        # # 双重for循环遍历
        # for i in range(len(sentence)):
        #     for j in dictionary:
        #         # 前缀相等的情况
        #         if j == sentence[i][:len(j)]:
        #             sentence[i] = j
        #             break
        # # 将列表转化为字符串返回
        # return ' '.join(sentence)

        # 第二种
        new_sentence = sentence.split(" ")

        # dictionary = sorted(dictionary, key=lambda x: len(x))
        # aaa-------------start
        new_dictionary_index = []
        for i, f in enumerate(dictionary):
            new_dictionary_index.append([i, len(f)])

        new_dictionary_index.sort(key=lambda x: x[1])
        new_dictionary = []
        for z in new_dictionary_index:
            new_dictionary.append(dictionary[z[0]])
        # aaa---------------end  两个for代替字典长度排序

        for m in range(len(new_sentence)):
            for n in new_dictionary:
                if n == new_sentence[m][:len(n)]:
                    new_sentence[m] = n
                    break
        return ' '.join(new_sentence)

# ----------------20220712

# 第一种：  奇数 + 偶数 = 奇数

row = [0 for i in range(m)]
col = [0 for i in range(n)]

print("1111", row)
print("2222", col)

for r, c in indices:
    row[r] += 1
    col[c] += 1
print("111133", row)
print("222244", col)
a = sum(r % 2 == 1 for r in row)
b = len(row) - a
c = sum(c % 2 == 1 for c in col)
d = len(col) - c
print(a * d + b * c)  # 奇数行数 * 偶数列数 + 偶数行数 * 奇数列数

# 第二种：  根据题意形成二维数组  计算奇数的个数
b = [[0 for _ in range(n)] for _ in range(m)]
for z, k in indices:
    for h in range(m):
        b[h][k] += 1
    for j in range(n):
        b[z][j] += 1
count = 0
for a in b:
    for c in a:
        if c % 2 != 0:
            count += 1
print(count)


# 计算4位数字 能够生成多少个不同的四位数字
a = [1, 2, 3, 4]
count = 0
for i in a:
    for f in a:
        for h in a:
            for l in a:
                if i != f and i != h and i != l and f != h and f != l and h != l:
                    count += 1
                    print(i * 1000 + f * 100 + h * 10 + l, end=',')

print('\n', count)


# 计算一个字符串中相同字符的个数

a = 'zhangkuiaaaaaaaaa'
b = set(list(a))
print(b)
count = 0
for i in b:
    for f in a:
        if i == f:
            count += 1
    print(i, count)
    count = 0

c = list(a)
d = {}
for o in c:
    d[o] = c.count(o)

print(d)



# 双指针计算列表里面两个数值差值是固定值的数据组
nums = [0, 1, 4, 6, 7, 10]
diff = 3


def findPairs(nums, k):
    if len(nums) < 2:
        return 0
    # nums.sort()
    idx1 = 0
    idx2 = 1
    # ans = set()
    ans = []
    while idx1 < len(nums) - 1 and idx2 <= len(nums) - 1:
        if idx1 == idx2:
            idx2 += 1
        s = nums[idx2] - nums[idx1]
        if s > k:
            idx1 += 1
        elif s < k:
            idx2 += 1
        else:
            ans.append((nums[idx1], nums[idx2]))
            idx1 += 1
    print(ans)
    return len(ans)


#  Counter 函数， 2023.6.13
# from collections import Counter
# nums = [4, 4, 2, 4, 3, 2, 5]
#
# class Solution:
#     def unequalTriplets(self, nums):
#         cnt = Counter(nums)
#         n = len(nums)
#         ans = a = 0
#         print(1111, cnt)
#         for b in cnt.values():
#             c = n - a - b
#             print(a, b, c)
#             ans += a * b * c
#             a += b
#         return ans
#
# print(Solution().unequalTriplets(nums))









