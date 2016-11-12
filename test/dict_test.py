from random import randint
from time import time
# dict 생성
dict1 = {}
dict2 = {}

print("dict 생성 시작")
for i in range(3000000):
    dict1[i] = {"test": i}
    dict2[i] = {"test": i}
print("dict 생성 끝")

# type 1
expireList = []
print("type 1 테스트 시작", len(dict1))
start = time()
for key in dict1:
    if dict1[key]["test"] > 50000:
        expireList.append(key)
for key in expireList:
    dict1.pop(key)
end = time() - start
print("type 1 테스트 끝", len(dict1))
print("process : %.5fs" % end)

# type 2
print("type 2 테스트 시작", len(dict2))
start = time()
for key in list(dict2):
    if dict2[key]["test"] > 50000:
        del dict2[key]
end = time() - start
print("type 2 테스트 끝", len(dict2))
print("process : %.5fs" % end)
