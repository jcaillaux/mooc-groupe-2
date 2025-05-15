### extract_content.py ###
"""
Module d'extraction des messages pour ne garder que les champs qui nous intéressent.
"""

from pymongo import MongoClient
from config import MONGO_URL, MONGO_DB_NAME, MONGO_COLLECTION_ORIGINAL, MONGO_COLLECTION_CLEANED

client = MongoClient(MONGO_URL)
db = client[MONGO_DB_NAME]
collection_original = db[MONGO_COLLECTION_ORIGINAL]
collection_cleaned = db[MONGO_COLLECTION_CLEANED]



def extract_content(content):      
    """
    Fonction d'extraction du contenu des messages.
    """
    """id = content.get('id', "")
    created_at = content.get('created_at', "")
    parent_id = content.get('parent_id', "")
    thread_id = content.get('thread_id', "")
    course_id = content.get('course_id', "")
    type = content.get('type', "")
    username = content.get('username', "")
    user_id = content.get('user_id', "")
    courseware_title = content.get('courseware_title', "")
    body = content.get('body', "")
    
    depth = content.get('depth', "")
    """
    children = content.get('children', [])


    # Vérifier si le document existe déjà dans la collection cleaned
    if not collection_cleaned.find_one({'id': id}):
        # Insérer le document dans la collection cleaned
        collection_cleaned.insert_one(content)
        #print(f"ID: {id:30} Course ID: {course_id:45} Username: {username}, {len(children)} ")
        

    # Appel récursif pour traiter les enfants
    for doc in children:
        extract_content(doc)
        input("Press Enter to continue...")

def main():
    """
    Fonction principale pour extraire le contenu des messages de la collection originale.
    """

    filter={}
   
    project={
        'content.id': 1,
        'content.created_at': 1,
        'content.parent_id': 1,
        'content.thread_id': 1,
        'content.course_id': 1,
        'content.type': 1,
        'content.username': 1,
        'content.user_id': 1,
        'content.courseware_title': 1,
        'content.body': 1,
        'content.children': 1,
        'content.depth': 1,
        'content.endorsed': 1
    }

    sort=list({}.items())
    
    result = collection_original.find(
    filter=filter,
    projection=project,
    sort=sort
    )

    for doc in result:
        content = doc['content']
        print(content)
        print("-" * 100)
        extract_content(content)

if __name__ == "__main__":
    main()

