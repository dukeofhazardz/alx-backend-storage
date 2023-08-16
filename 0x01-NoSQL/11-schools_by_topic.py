#!/usr/bin/env python3
"""NoSQL with pymongo"""


def schools_by_topic(mongo_collection, topic):
    """ A Python function that returns the list of school
        having a specific topic """
    school_list = mongo_collection.find({"topics": {"$in": [topic]}})
    return school_list
