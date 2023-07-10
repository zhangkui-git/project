import re
import string
import random


def gen_rdm(randomlength=5, con_digits=True):
    """
  生成一个指定长度的随机字符串，其中
  string.digits=0123456789
  string.ascii_letters=abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ

  :param randomlength: 生成随机数据的长度，默认是5
  :param con_digits: 是否允许数字
  :return:
  """
    if con_digits:
        str_list = [random.choice(string.digits + string.ascii_letters) for i in range(randomlength)]
    else:
        str_list = [random.choice(string.ascii_letters) for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str


def gen_str_zh(randomlength=5):
    s = '我的祖国是花园花园的花朵真鲜艳和暖的阳光照耀着我们每个人脸上都肖开颜'
    str_list = [random.choice(s) for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str


def gen_digit(start=0, end=10):
    return random.randint(start, end)


if __name__ == '__main__':
    print(gen_rdm())
    print(gen_str_zh())
    print(gen_digit(start=2000, end=3000))
    a = 'hello'
    print(a * 2)
    # print(a.index('s', 2, 3))
    print(a.upper())
    print(a.lower())
    print(a.split('l', 1))
    print(a.strip('h'))
    print(a.count('l'))
    print(a.replace('l', 'h', 1))
    b = [1, 2, 3, 'st', True, 3.6]
    print(b.count(1))
    print(b.index(2, 1, 3))
    print(b.count('st'))
    print(b.pop(0))
    print(b)
    print(b.remove(2))
    print(b)
    # print(b.clear())
    # print(b)
    print(b.insert(0, 1))
    print(b)
    c = (1, 2, 3, 'w', False, 3.5)
    print(c.index('w'))
    c.count(2)
    print(c.__str__())
    d = {'type': 'int', 'name': 'lm', 'age': 15}
    d['type'] = 'class'
    print(d)
    d['sex'] = 'girl'
    print(d)
    print(d.pop('sex'))
    print(d)
    print(d.get('name'))
    print(d.values())
    print(d.keys())
    print(d.items())
    for k, v in d.items():
        print(k, ':', v)
