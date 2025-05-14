"""
 Script Python pour importer un fichier JSON dans MongoDB
 Ce script lit un fichier JSON et insère les données dans une collection MongoDB.   
"""

import os
import json
from pymongo import MongoClient # pip install pymongo
from config import MONGO_URL, MONGO_DB_NAME, MONGO_COLLECTION_ORIGINAL, DATA_DIR


def loadjson2mongo():
    """
    Fonction principale pour charger un fichier JSON dans MongoDB.
    """
    # Connexion à MongoDB
    client = MongoClient(MONGO_URL)  # Modifiez l'URL selon votre configuration
    db = client[MONGO_DB_NAME]  # Nom de votre base de données
    collection = db[MONGO_COLLECTION_ORIGINAL]  # Nom de votre collection

    # Chemin vers votre fichier JSON
    fichier_json = os.path.join(DATA_DIR, "link_to_MOOC_forum.json")
    #fichier_json = '/Users/cyriljeanneau/Documents/02. Professionnel/00. Formation Dev IA/Projets/07. mooc/cours_avant_projet/MOOC_forum.json'

    # Chargement des données JSON
    with open(fichier_json, 'r', encoding='utf-8') as file:
            try:
                contenu = file.read()
                
                # Nettoyer le contenu si nécessaire
                contenu = contenu.replace('\n', '')  # on supprime les sauts de ligne
                contenu = contenu.replace('}{', '},{') # on sépare les objets JSON par des virgules
                contenu = f'[{contenu}]'  # Envelopper dans un tableau si nécessaire
                donnees_json = json.loads(contenu)

            except json.JSONDecodeError as e:
                print(f"Erreur de décodage JSON : {str(e)}")
                print(f"Erreur à la position : {e.pos}")
                print(f"Ligne : {e.lineno}, Colonne : {e.colno}")
                return

    # Insertion des données dans MongoDB
    if isinstance(donnees_json, list):
        # Si votre JSON est un tableau d'objets
        collection.insert_many(donnees_json)
        print(f"{len(donnees_json)} documents insérés avec succès.")
    else:
        # Si votre JSON est un seul objet
        collection.insert_one(donnees_json)
        print("Document inséré avec succès.")

    # Vérification
    count = collection.count_documents({})
    print(f"Nombre total de documents dans la collection: {count}")
    # Fermeture de la connexion
    client.close()
    print("Connexion à MongoDB fermée.")


if __name__ == "__main__":
    loadjson2mongo()
    # A exécuter une seule fois pour trnsferer le fichier JSON dans MongoDB
    # $ python -m scripts.json2mongoDB


    
    

