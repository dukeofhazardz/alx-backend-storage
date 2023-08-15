#!/usr/bin/env python3
"""NoSQL with pymongo"""


def list_all(mongo_collection):
    """Python function that lists all documents in a collection"""
    collections = [doc for doc in mongo_collection.find()]
    return collections
