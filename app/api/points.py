import json


def list_courses():
    with open('data/courses.json', 'r') as f:
        return json.load(f)


def list_threads(course_id):
    with open('data/threads.json', 'r') as f:
        threads_list = json.load(f)
        return threads_list.get(course_id, [])


def dump_thread(thread_id):
    return []
