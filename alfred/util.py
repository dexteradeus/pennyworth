
from functools import wraps
from random import randint

def get_random_id():
    return randint(0, 2**16)

def disconnect(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        try:
            return fn(self, *args, **kwargs)
        except:
            raise
        finally:
            if self._connected:
                self._disconnect()
    return wrapper
