#!/usr/bin/env python3
"""Module for Redis-based caching"""

import redis
from uuid import uuid4
from typing import Union

UnionOfTypes = Union[str, bytes, int, float]


class Cache:
    """Class for methods that operate a caching system."""

    def __init__(self):
        """Initialize an instance of the Redis-based caching system."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: UnionOfTypes) -> str:
        """
        Store method takes a data argument and returns a string.
        Generate a random key (e.g., using uuid), store the input data in Redis
        using the random key, and return the key.
        """
        key = str(uuid4())
        self._redis.mset({key: data})
        return key
