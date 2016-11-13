from time import time
from functools import wraps


def processtime(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        resutl = func(*args, **kwargs)
        return result
    return wrapper
