#!/usr/bin/env python3
"""NoSQL with pymongo"""


def update_topics(mongo_collection, name, topics):
    """ A Python function that changes all topics of a school
        document based on the name """
    collection = mongo_collection.update_many({"name": name},
                                              {'$set': {"topics": topics}})
    return collection
