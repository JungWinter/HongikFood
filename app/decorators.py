from time import time
from functools import wraps


def processtime(func):
    '''
    콘솔에서 함수의 실행시간을 디버깅하는 용도입니다.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        during = time() - start
        print(">>", func.__name__, ">> %.5fs" % during)
        return result
    return wrapper
