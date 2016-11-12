from random import randint
from time import time
from copy import deepcopy

# dict 생성
dict1 = {}
dict2 = {}
dict3 = {}

print("dict 생성 시작")
for i in range(1000000):
    dict1[i] = {"test": i}
dict2 = deepcopy(dict1)
dict3 = deepcopy(dict1)
dict4 = deepcopy(dict1)
print("dict 생성 끝")


def log(dic):
    def _log(func):
        def wrapper(*args, **kwargs):
            print(func.__name__, "테스트 시작. 길이 :", len(dic))
            start = time()
            try:
                result = func(*args, **kwargs)
            except MemoryError:
                print("Out of MemoryError")
            end = time() - start
            print(func.__name__, "테스트 끝. 길이 :", len(dic))
            print("실행 시간 : %.5fs" % end)
            return result
        return wrapper
    return _log


@log(dict1)
def type1():
    expireList = []
    for key in dict1:
        if dict1[key]["test"] > 50000:
            expireList.append(key)
    for key in expireList:
        dict1.pop(key)


@log(dict2)
def type2():
    it = (key for key in deepcopy(dict2))
    for _ in range(len(dict2)):
        key = next(it)
        if dict2[key]["test"] > 50000:
            del dict2[key]


@log(dict3)
def type3():
    for key in deepcopy(dict3):
        if dict3[key]["test"] > 50000:
            del dict3[key]


@log(dict4)
def type4():
    for key in list(dict4):
        if dict4[key]["test"] > 50000:
            del dict4[key]

type1()
type2()
type3()
type4()
