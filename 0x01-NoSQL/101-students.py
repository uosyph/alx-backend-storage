#!/usr/bin/env python3
"""Lists all students sorted by average score"""


def top_students(mongo_collection):
    """Returns all students sorted by average score"""
    return list(mongo_collection.find())
