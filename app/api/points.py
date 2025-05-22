import json
from pymongo import MongoClient
from config import MONGO_URL
from .utils import clean_mooc_thread


def list_courses():
    #with open('data/courses.json', 'r') as f:
    #    return json.load(f)
    client = MongoClient(MONGO_URL)
    results = client['mooc']['sample'].aggregate([
        {
            '$group': {
                '_id': '$content.course_id',
                'count': {
                    '$sum': 1
                }
            }
        }
    ])

    courses_list = []
    for result in results:
        courses_list.append({
            'course_id': result['_id'],
            'thread_count': result['count']
        })
    return courses_list


def list_threads(course_id):
    #with open('data/threads.json', 'r') as f:
    #    threads = json.load(f)
    #    return threads.get(course_id, [])
    client = MongoClient(MONGO_URL)
    results = client['mooc']['sample'].find(
            {"content.course_id": course_id}, {"content.title": 1, "content.id": 1})

    thread_list = []
    for result in results:
        thread_list.append({
            'thread_title': result['content']['title'],
            'thread_id': result['content']['id']
        })
    return thread_list

"""
def list_messages(thread_id):
    client = MongoClient('mongodb://localhost:27017/')
    filter = {
        '_id': thread_id
    }
    limit = 100

    result = client['G2']['extracted_documents'].find(
        filter=filter,
        limit=limit
    )
    return list(result)
"""

def dump_thread(thread_id):
    client = MongoClient(MONGO_URL)
    filter = {'_id' : thread_id}
    result = client['G2']['forum_original'].find_one(filter = filter)
    return clean_mooc_thread(result, analyse=False)

def analyze_thread(thread_id):
    client = MongoClient(MONGO_URL)
    filter = {'_id' : thread_id}
    result = client['G2']['forum_original'].find_one(filter = filter)
    return clean_mooc_thread(result, analyse=True)
