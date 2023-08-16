#!/usr/bin/env python3
"""
Cache class definition
"""
from redis import Redis
from uuid import uuid4
from functools import wraps
from typing import Callable, Union


def count_calls(method: Callable) -> Callable:
    """ A that takes a single method Callable argument
        and returns a Callable """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ The wrapper method """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """ Defines the Cache class """
    def __init__(self) -> None:
        """ Initializes and stores an instance of the Redis
            client as a private variable """
        self._redis = Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: any) -> str:
        """ A method that takes a data argument and returns a string. """
        key: str = str(uuid4())
        self._redis.set(f"{key}", data)
        return key
    
    def get(self, key: str, fn: Callable=None) -> Union[bytes, None]:
        """ A method that converts data back to the desired format. """
        if fn is None:
            return self._redis.get(key)
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data)

    def get_str(self, key: str) -> str:
        """ A method that parametrize Cache.get with the str
            conversion function """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """ A method that parametrize Cache.get with the int
            conversion function """
        return self.get(key, fn=int)
