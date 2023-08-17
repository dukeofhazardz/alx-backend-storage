#!/usr/bin/env python3
"""NoSQL with pymongo"""
import pymongo


def top_students(mongo_collection):
    """ A Python function that returns all students sorted by average score """
    all_students = [student for student in mongo_collection.find({})]
    for student in all_students:
        topics = student.get('topics')

        count = 0
        total_score = 0
        for topic in topics:
            total_score += topic.get('score')
            count += 1
        avg_score = total_score / count
        mongo_collection.update_one({"name": f"{student.get('name')}"},
                                    {"$set": {"averageScore": avg_score}})
    return [student for student in mongo_collection.
            find({}, sort=[('averageScore', pymongo.DESCENDING)])]
