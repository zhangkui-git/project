# class istest2(object):
#     def isValue(self, n):
#         if n == 2:
#             return True
#         else:
#             return False
# t = istest2()
# print(t.isValue(2))

# 20210923-数字3幂的返回True 或 False
# class Solution(object):
#     def isPowerOfThree(self, n):
#         if n == 0:
#             return False
#         if n == 1:
#             return True
#          if n == 2:
#              return False
#         while n != 1:
#             if n % 3 == 0:
#                 n = n // 3
#             else:
#                 return False
#         return True
# d = Solution()
# print(d.isPowerOfThree(3))


#  1+2+....+10 = ？
# a = 0
# for i in range(11):
#     a+=i
# #    print(i)
# print(a)

# 冒泡
# a = [12, 30, 2, 8, 19, 22, 80, 1, 99]
# for i in range(len(a)):
#     for j in range(len(a)-i-1):
#       if a[j] > a[j+1]:
#         a[j], a[j+1] = a[j+1], a[j]
# print(a)

# 山脉数组
# class isTset1014(object):
#     def peakIndex(self, a):
#         for i in range(len(a) - 1):
#             if a.__getitem__(i) > a.__getitem__(i-1) and a.__getitem__(i) > a.__getitem__(i+1):
#                 return i
#         return 99

# a = [1, 2, 4, 5, 6, 4, 3]
# b = isTset1014()
# print(b.peakIndex(a))


# a = 5
# b = bin(a)
# c = len(bin(a))
# d = int('1'*(len(bin(a))-2), 2)
# e = a ^ d
# print('1'*(len(bin(a))-2))
# print(b)
# print(c)
# print((len(bin(a))-2))
# print('1'*(len(bin(a))-2))
# print('1'*(len(bin(a))-2), 2)
# print(d)


# print(d)
# print(e)

# 数字的补数
# class is2to10(object):
#     def test2to10(self, a, d):
#         return a ^ int('1'*(len(bin(d))-2), 2)
#
# a = 5
# d = 9
# b = is2to10()
# c = int('1' * (len(bin(d)) - 2), 2)
# print(c)
# print(b.test2to10(a, d))

#

# count = 1
# data1 = '{}{}'.format('2021-', count)
# print(data1)

# 数组去重并排序输出， 1. set数据类型自动去重排序输出  2. 利用剔除法解决
# a = [1, 3, 0, 2, 6, 0, 5]
# id = set(a)
# list1 = list(set(a))
# print(list1)
# print(id)

# new_a = []
# for i in a:
#     if i not in new_a:
#         new_a.append(i)
#         for b in range(len(new_a)):
#             for c in range(len(new_a)-b-1):
#                 if new_a[c] < new_a[c+1]:
#                     new_a[c], new_a[c+1] = new_a[c+1], new_a[c]
# print(new_a)

# 输出字符串每个元素个数
# a = 'zhangkui,zzzzzzzzzzzzzzzzzz'
# new_a = {}
# for i in a:
#     new_a[i] = a.count(i)
# print(new_a)

# a = input("请输入：")
# dict1 = {}
# for i in a:
#     if i not in dict1:
#         dict1[i] = 1
#     else:
#         dict1[i] += 1
# for k in dict1:
#     print(k, "总共出现次数：", dict1[k])



# a = [1, 2, 9, 21, 3, 5, 1, 0, 3]
# b = [2, 3, 5, 30, 20, 19]
# a.extend(b)
# c = list(set(a))
# print(a)
# for i in range(len(b)):
#     a.append(b[i])
# print(a)


# 取出数组乘积最大的俩数之乘积 ： 目前未判断正数 负数情况
# a = [1, -2, -399999999999, 69999999, 0, 2]
# new_a = []
# for i in range(len(a)):
#     c = int(a[i])
#     c = abs(c)
#     new_a.append(c)
# print(new_a)
# for e in range(len(new_a)):
#     for f in range(len(new_a)-e-1):
#         if new_a[f] < new_a[f+1]:
#             new_a[f], new_a[f+1] = new_a[f+1], new_a[f]
# print(new_a)
# print(new_a[0]*new_a[1])

# 监测大写字母
# class Solution:
#     def detectCapitalUse(self, word):
#         is_upper = [c.isupper() for c in word]  # 大写字符判别列表
#         print(is_upper)
#         is_lower = [c.islower() for c in word]  # 小写字符判别列表
#         if all(is_upper) or all(is_lower):  # 如果所有字符都是大写或小写
#             return True
#         if any(is_upper) and is_upper[0] and all(is_lower[1:]):  # 如果既有大写又有小写 , 要求第一个大写其他都小写
#             return True
#         else:
#             return False
#
# word = input("请输入：")
# p = Solution()
# print(p.detectCapitalUse(word))

# 亲密字母
# class Solution:
#     def buddyStrings(self, A, B):
#         if len(A) != len(B):
#             return False
#         if A == B:
#             if len(set(A)) < len(A):
#                 return True
#             return False
#         a = []
#         for i in range(len(A)):
#             if A[i] != B[i]:
#                 a.append(i)
#         if len(a) > 2 or len(a) == 1:
#             return False
#         if A[a[0]] == B[a[1]] and A[a[1]] == B[a[0]]:
#             return True
#         return False
#
# A = 'abcd'
# B = 'abcd'
# p = Solution()
# print(p.buddyStrings(A, B))


# 数字计算最小次数为1
# class intTh(object):
#     def dintTh(self, n):
#         cnt = 0
#         while n != 1:
#             if n == 3:
#                 return cnt + 2
#             elif n % 2 == 0:
#                 n //= 2
#             elif (n + 1) % 4:
#                 n -= 1
#             # print(n)
#             else:
#                 n += 1
#             cnt += 1
#         return cnt
# n = 4
# p = intTh()
# print(p.dintTh(n))

# 20211201 - 连续字符:  enumerate - 函数用法
# class Solution:
#     def maxPower(self, s):
#         a = 1
#         b = s[0]
#         tmp = 1
#         for i, f in enumerate(s):
#             if i:
#                 if f == b:
#                     tmp += 1
#                 else:
#                     tmp = 1
#                     b = f
#                 a = max(a, tmp)
#         return a
# s = 'qaweeeesddeedt'
# p = Solution()
# print(p.maxPower(s))

# 20211202 -- 506. 相对名次: sort / sorted / 及索引列表排序（ sort(key=lambda a:a[0], reverse = True) ）函数用法
# class Solution:
#     def findRelativeRanks(self, score: List[int]) -> List[str]:  # 如果直接排序是不行的，因为会丢失老的索引。 因此我用了一个 pairs 数组，来维护一个 score-> 索引的映射。之后对 paris 进行降序排列即可。由于我事先保存了老的索引信息，因此是没有问题的。
# # ---------------- 第一种：使用sorted 倒叙排序 或 使用冒泡
#         nums = []
#         nums = sorted(score, reverse=True)
#         res = []
#         for i in range(len(score)):
#             if nums.index(i) == 0:
#                 res.append('Gold Medal')
#             elif nums.index(i) == 1:
#                 res.append('Silver Medal')
#             elif nums.index(i) == 2:
#                 res.append('Bronze Medal')
#             else:
#                 res.append(str(nums.index(i) + 1))
#         return res
# -------- 采用第二种方法计算（由于题型方法限制，只能保留索引方式）
#         c = []
#         for i in range(len(score)):
#             c.append([score[i], i])
#         # print(c)
#         c.sort(key=lambda a: a[0], reverse=True)
        # print(c)
        # print(c[0][1])
#         for i in range(len(score)):
#             if i == 0:
#                 score[c[i][1]] = 'Gold Medal'
#             if i == 1:
#                 score[c[i][1]] = 'Silver Medal'
#             if i == 2:
#                 score[c[i][1]] = 'Bronze Medal'
#             if i > 2:
#                 score[c[i][1]] = str(i + 1)
#         return score
# score = [3, 4, 6, 2, 9, 0]
# p = Solution()
# print(p.findRelativeRanks(score))


# 2021.12.12 -  转换成小写字母
# str = "www.runoob.com"
# print(str.upper())  # 把所有小写转成大写
# print(str.lower())  #把所有大写转成小写
# print(str.capitalize())  # 把第一个字母转成大写，其余小写
# print(str.title())  #把每个单词的第一个字母转成大写，其余小写
# ----------- s 代表字符串
# s.isalnum() # 所有字符都是数字或者字母
# s.isalpha() # 所有字符都是字母
# s.isdigit() # 所有字符都是数字
# s.islower() # 所有字符都是小写
# s.isupper() # 所有字符都是大写
# s.istitle() # 所有单词都是首字母大写，像标题
# s.isspace() # 所有字符都是空白字符、\t、\n


# 20211217 - 换酒问题
# class nullto9(object):
#     def to9(self, sum, ch):
#         res = []
#         sum2 = sum
#         if sum < ch or sum / ch < 1:
#             return sum
#         if sum == ch:
#             return sum + 1
#         while sum2/ch >= 1:
#             res.append(sum2//ch)
#             sum2 = sum2 // ch + sum2 % ch
#         sum1 = 0
#         for i in range(len(res)):
#             sum1 += res[i]
#         return sum1 + sum
# p = nullto9()
# print(p.to9(11, 3))


# 20211221 - 今年的第几天
# class Solution:
#     def dayOfYear(self, date: str) -> int:
#         dicmon = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
#         dicp = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
#         dicr = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
#         dicday = ["01", "02", "03", "04", "05", "06", "07", "08", "09"]
#         year = int(date[:4])
#         if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
#             now_mon = date[-5:7]
#             now_day = date[-2:]
#             res = 0
#             for i in range(dicmon.index(now_mon)):
#                 res += dicr[i]
#             if now_day in dicday:
#                 return res + int(dicday[dicday.index(now_day)][1])
#             else:
#                 return res + int(now_day)
#         else:
#             now_mon = date[-5:7]
#             now_day = date[-2:]
#             res = 0
#             for i in range(dicmon.index(now_mon)):
#                 res += dicp[i]
#             if now_day in dicday:
#                 return res + int(dicday[dicday.index(now_day)][1])
#             else:
#                 return res + int(now_day)

#
# date = input("请输入日期yyyy-mm-dd:")
# p = Solution()
# print(p.dayOfYear(date))


# 两数之和 -- 使用 enumerate - 函数用法

# 自己利用while循环写的
# class Solution:
#     def twoSum(self, nums, target):
#         f = 0
#         i = 1
#         while f < len(nums):
#             while i < len(nums):
#                 if nums[f] + nums[i] == target:
#                     return [f, i]
#                 else:
#                     i += 1
#             f += 1
#             i = f + 1
#         return -1

# class Solution:
#     def twoSum(self, nums, target):
#         dic1 = {}
#         for i, f in enumerate(nums):
#             if target - f in dic1:
#                 return [dic1[target - f], i]
#             dic1[nums[i]] = i
#         return -1
#
# nums = [2, 11, 4, 15]
# nums = [3, 3]
# nums = [3, 2, 4]
# nums = [3, 2, 3]
# target = 6
# p = Solution()
# print(p.twoSum(nums, target))

# 针对于format函数 及 time函数的了解

# s = 'zhangkui'
# s1 = 'abcdefghigklmnopqrstuvwxyz'
# t = s[1:-1]
# print(t)
# count = random.randint(1, 31)
# res = '0 {s} 0'.format(s=s)
# count = 1
# while count <= 100:
#     start_time = datetime(2022, 1, 13, 9, 18, 23)
#     start_time1 = start_time + timedelta(minutes=15 * count)
#     print(start_time1)
#     count += 1
# # res1 = '{}{}'.format('2022-01-', count)
# print(res, '\n', res1)


# 20220115  -- 1716. 计算力扣银行的钱
# class Solution:
#     def totalMoney(self, n: int) -> int:
#         if n <= 7:
#             return int((1 + n) * n / 2)
#         if n > 7:
#             a1 = 28
#             num = n // 7
#             num1 = n % 7
#             sum3 = a1
#             print(f"num取整是{num}")
#             print(f"num1余数是{num1}")
#             if num == 1:
#                 sum3 = a1
#             if num > 1:
#                 cnt = 1
#                 while cnt < num:
#                     a1 = 28 + 7 * cnt
#                     sum3 = sum3 + a1
#                     cnt += 1
#             cnt1 = 1
#             sum2 = 0
#             while cnt1 <= num1:
#                 sum1 = num + cnt1
#                 sum2 = sum2 + sum1
#                 cnt1 += 1
#             print(f"sum2数值{sum2}")
#             print(f"sum3数值{sum3}")
#             return sum3 + sum2
#
# p = Solution()
# print(p.totalMoney(26))