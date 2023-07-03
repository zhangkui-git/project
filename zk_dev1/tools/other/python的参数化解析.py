import argparse
import sys

parse = argparse.ArgumentParser(prog='tmp1.py')     # 创建一个解析器对象
parse.add_argument('-w', '--w', dest='w1', default=123, type=int, help='年龄（此参数help为参数描述）')    # 可选参数
# parse.add_argument('w', type=int, help='年龄（此参数help为参数描述）')     # 必选参数
args = parse.parse_args()
print(args.w1)


