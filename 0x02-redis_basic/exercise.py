#!/usr/bin/env python3
"""
Cache class definition
"""
from redis import Redis
from uuid import uuid4
from functools import wraps
from typing import Callable, Union


def count_calls(method: Callable) -> Callable:
    """ A function that takes a single method Callable argument
        and returns a Callable """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ The wrapper method """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ A function that stores the history of inputs and outputs
        for a particular function. """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ The wrapper method """
        key_inputs = "{}:inputs".format(method.__qualname__)
        key_outputs = "{}:outputs".format(method.__qualname__)
        input_str = str(args)
        redis_instance = self._redis
        redis_instance.rpush(key_inputs, input_str)

        result = method(self, *args, **kwargs)
        redis_instance.rpush(key_outputs, result)

        return result
    return wrapper


class Cache:
    """ Defines the Cache class """
    def __init__(self) -> None:
        """ Initializes and stores an instance of the Redis
            client as a private variable """
        self._redis = Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: any) -> str:
        """ A method that takes a data argument and returns a string. """
        key: str = str(uuid4())
        self._redis.set(f"{key}", data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[bytes, None]:
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


def replay(method: Callable) -> None:
    """ A function to display the history of calls of a particular function """
    key_inputs = "{}:inputs".format(method.__qualname__)
    key_outputs = "{}:outputs".format(method.__qualname__)

    redis_instance = method.__self__._redis
    inputs = redis_instance.lrange(key_inputs, 0, -1)
    outputs = redis_instance.lrange(key_outputs, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for input_str, output_str in zip(inputs, outputs):
        input_str = input_str.decode('utf-8')
        output_str = output_str.decode('utf-8')
        print(f"{method.__qualname__}(*{input_str}) -> {output_str}")
