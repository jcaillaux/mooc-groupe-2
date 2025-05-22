<<<<<<< Updated upstream
=======
from pymongo import MongoClient
from flask import Flask, jsonify
from flask_cors import CORS
>>>>>>> Stashed changes
import json
from pymongo import MongoClient


def list_courses():
    with open('data/courses.json', 'r') as f:
        return json.load(f)


def list_threads(course_id):
    with open('data/threads.json', 'r') as f:
        threads = json.load(f)
        return threads.get(course_id, [])


def list_messages(thread_id):
    client = MongoClient('mongodb://localhost:27017/')
    filter = {
        '_id': thread_id
    }
    limit = 100

<<<<<<< Updated upstream
    result = client['G2']['extracted_documents'].find(
=======
    result = client['mooc']['sample'].find(
>>>>>>> Stashed changes
        filter=filter,
        limit=limit
    )
    return list(result)


def dump_thread(thread_id):
    # À implémenter plus tard si tu veux exposer un thread par son ID
    return []


"""
@app.route('/api/thread/<thread_id>', methods=['GET'])
def api_get_thread(thread_id):
    return jsonify(list_messages(thread_id))


@app.route('/api/login', methods=['POST'])
def api_login():
    json_data = request.get_json()
    username = json_data.get('username')
    password = json_data.get('password')

    if username == 'admin' and password == 'admin':
        return jsonify({'status': 'success', 'message': 'Login successful'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
<<<<<<< Updated upstream
"""
=======

>>>>>>> Stashed changes

if __name__ == '__main__':
    app.run(debug=True)
