### Mongo_functions.py ###
"""
Module de gestion de l'accès à la base de données MongoDB.
Utilise pymongo.
"""

from config import MONGO_URL, MONGO_DB_NAME, MONGO_COLLECTION_CLEANED
from pymongo import MongoClient # pip install pymongo


print(MONGO_URL)
client = MongoClient(MONGO_URL)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_CLEANED]


def read_msg():
    # Lire les messages de la collection
    messages = collection.find({},{})
    return list(messages)
    
def read_msg_by_id(msg_id):
    # Lire un message spécifique par ID
    message = collection.find_one({"id": msg_id})
    if message:
        return message
    else:
        print(f"Message with ID {msg_id} not found.")
    # Fermer la connexion
    client.close()


def main():
    # Exemple d'utilisation
    all_msg = read_msg()
    print(all_msg[1:3])  
    #print("\nMessage with ID 1:")
    #msg = read_msg_by_id(1)
    #print(msg)

if __name__ == "__main__":
    main()

