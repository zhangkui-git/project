def get(**kwargs):
    kwargs = kwargs.get('key2')
    print(kwargs)


get(key=1, key2=2)


def test(one, *args):
    print(f"first element is {one}")
    # print("in args:", type(args))
    print("in args:", len(args))
    # for i in args:
    #     print("%s" % i)


test(3, 4, 5, 4)