from config import MONGO_URL
from pymongo import MongoClient # pip install pymongo


db_name = 'mooc'
collection_name = 'documents'

print(MONGO_URL)
client = MongoClient(MONGO_URL)
db = client[db_name]
collection = db[collection_name]


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

