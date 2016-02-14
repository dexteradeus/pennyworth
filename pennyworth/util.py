
from __future__ import absolute_import, unicode_literals
from builtins import *
from functools import wraps
from random import randint

def get_random_id():
    return randint(1, 2**16)

def validate_int(val):
    try:
        val = int(val)
    except (ValueError, TypeError):
        raise ValueError('Invalid value "{}". Must be integer.'.format(val))
    return val

def validate_bytes(val):
    try:
        val = bytes(val)
    except (ValueError, TypeError):
        raise ValueError('Invalid value "{}". Must be of type bytes or '
            'equivalent'.format(val))
    return val

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
