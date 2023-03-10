
def num(n):
	e = list(str(n))
	b = []
	for i in e:
		b.append(int(i))
	return b


def str2(str1):
	d = []
	for z in range(len(str1)):
		tmp = []
		for j in str1[z]:
			tmp.append(str(j))
		c = ''.join(tmp)
		d.append(int(c))
	return d

def permutation(b1):
	s = []
	if len(b1) == 1:
		return [b1]
	else:
		for i in range(len(b1)):
			b1[i], b1[0] = b1[0], b1[i]  # 每次交换一个元素
			temp = permutation(b1[1:])  # 递归
			for l in temp:  # 如果只是打印不用保存，那么for循环可以去掉
				s.append([b1[0]] + l)
			b1[i], b1[0] = b1[0], b1[i]  # 恢复原始序列
	return s


if __name__ == '__main__':
	n = 2140
	b = num(n)
	print(b)
	print(permutation(b))
	str1 = permutation(b)
	print(str2(str1))
