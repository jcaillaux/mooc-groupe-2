from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
# Autorision explicite des requêtes CORS pour toutes les routes et tous les domaines mais pour test
CORS(app, resources={r"/*": {"origins": "*"}})


def list_courses():
    with open(r'C:/Users/p2972/Projets/Mooc/mooc/mooc-groupe-2/data/courses.json', 'r') as f:
        return json.load(f)


def list_threads(course_id):
    with open(r'C:/Users/p2972/Projets/Mooc/mooc/mooc-groupe-2/data/threads.json', 'r') as f:
        threads = json.load(f)
        return threads.get(course_id, [])
    

from pymongo import MongoClient




def list_messages(thread_id):
    client = MongoClient('mongodb://localhost:27017/')
    filter={
        '_id': thread_id
    }
    limit=100

    result = client['mooc']['sample'].find(
    filter=filter,
    limit=limit
    )
    return list(result)
    

def dump_thread(thread_id):
    # À implémenter plus tard si tu veux exposer un thread par son ID
    return []


@app.route('/api/courses', methods=['GET'])
def api_list_courses():
    return jsonify(list_courses())


@app.route('/api/threads/<course_id>', methods=['GET'])
def api_list_threads(course_id):
    return jsonify(list_threads(course_id))


@app.route('/api/thread/<thread_id>', methods=['GET'])
def api_get_thread(thread_id):
    return jsonify(list_messages(thread_id))


if __name__ == '__main__':
    app.run(debug=True)


