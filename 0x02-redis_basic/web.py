#!/usr/bin/env python3
"""Expiring web cache and tracker module"""

import redis
import requests
from typing import Callable
from functools import wraps

redis_connection = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """
    Decorator that wraps around HTTP request functions to provide caching.
    """

    @wraps(method)
    def wrapper(url):
        """Wrapper function for the count_requests decorator."""
        redis_connection.incr(f"count:{url}")
        cached_response = redis_connection.get(f"cached:{url}")
        if cached_response:
            return cached_response.decode("utf-8")
        result = method(url)
        redis_connection.setex(f"cached:{url}", 10, result)
        return result

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """
    Retrieves a web page, and caches the response for 10 seconds.
    """
    res = requests.get(url)
    return res.text
