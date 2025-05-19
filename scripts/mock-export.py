from pymongo import MongoClient
import json


def export_courses(client):
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
    with open('../data/courses.json', 'w') as f:
        json.dump(courses_list, f)

    return courses_list


def export_threads(client, courses_list):

    thread_list = {}

    for course in courses_list:
        course_id = course['course_id']
        results = client['mooc']['sample'].find(
            {"content.course_id": course_id}, {"content.title": 1, "content.id": 1})

        thread_list[course_id] = []
        for result in results:
            thread_list[course_id].append({
                'thread_title': result['content']['title'],
                'thread_id': result['content']['id']
            })
    with open('../data/threads.json', 'w') as f:
        json.dump(thread_list, f)


if __name__ == '__main__':
    client = MongoClient('mongodb://localhost:27017/')
    courses_list = export_courses(client)
    export_threads(client, courses_list)
