#!/usr/bin/env python3
"""Module for Redis-based caching"""

import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps

UnionOfTypes = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts how many times methods of the Cache class are called.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Wrapper function for the count_calls method."""
        self._redis.incr(key)
        return method(self, *args, **kwds)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs
    and outputs for a particular function.
    """
    input_list = f"{method.__qualname__}:inputs"
    output_list = f"{method.__qualname__}:outputs"

    @wraps(method)
    def wrapper(self, *args) -> bytes:
        """Wrapper function for the call_history method."""
        self._redis.rpush(input_list, str(args))
        output = method(self, *args)
        self._redis.rpush(output_list, output)
        return output

    return wrapper


def replay(method: Callable) -> None:
    """
    Replay function that prints the call history of a decorated method.
    """
    name = method.__qualname__
    redis_connection = redis.Redis()

    calls = redis_connection.get(name).decode("utf-8")
    print(f"{name} was called {calls} times:")

    inputs = redis_connection.lrange(f"{name}:inputs", 0, -1)
    outputs = redis_connection.lrange(f"{name}:outputs", 0, -1)
    for input, output in zip(inputs, outputs):
        print(f"{name}(*{input.decode('utf-8')}) -> {output.decode('utf-8')}")


class Cache:
    """Class for methods that operate a caching system."""

    def __init__(self):
        """Initialize an instance of the Redis-based caching system."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: UnionOfTypes) -> str:
        """
        Store method takes a data argument and returns a string.
        Generate a random key (e.g., using uuid), store the input data in Redis
        using the random key, and return the key.
        """
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> UnionOfTypes:
        """
        Retrieve data stored at a key and convert
        the data back to the desired format.
        """
        data = self._redis.get(key)
        return fn(data) if fn else data

    def get_str(self, key: str) -> str:
        """Retrieve a string from the cache."""
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """Retrieve an integer from the cache."""
        return self.get(key, int)
