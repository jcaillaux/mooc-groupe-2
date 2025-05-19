### Mongo2PG.py ###
"""
Script de transfert des messages de MongoDB vers PostgreSQL.
Utilise les modules Mongo_functions et PGSQL_functions.
"""

import sys
import os
import time

# Add parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import functions

from app.Mongo_functions import read_msg, read_msg_by_id
from config import MONGO_COLLECTION_CLEANED
from google import genai # pip install google-genai
from mistralai import Mistral
from sentence_transformers import SentenceTransformer
from app.postgreDB import Message, add_message


model = SentenceTransformer(
    'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
print ("Modèle chargé : ", model)

def main():


    all_msg = read_msg(MONGO_COLLECTION_CLEANED)
    nb_msg_total = len(all_msg)
    print(f"Nombre total de messages : {nb_msg_total}")
    cpt_total = 0
    cpt_saved = 0
    time_begin = time.time()

    for msg in all_msg:
        # On cree une instance de la classe message
        mymessage = Message()
        cpt_total += 1

        # On ne veut pas enregistrer les messages dont le body est inexistant
        mymessage.body = msg.get('body', None)
        if mymessage.body is not None:
            mymessage.id = msg.get('id')
            mymessage.created_at = msg.get('created_at', None)
            mymessage.parent_id = msg.get('parent_id', None)
            mymessage.thread_id = msg.get('thread_id', None)

            mymessage.body_embedding = model.encode(
                mymessage.body, show_progress_bar=False)
            mymessage.body_embedding = mymessage.body_embedding.tolist()

            add_message(mymessage)
            cpt_saved += 1

        os.system('clear')
        print(f"Message {cpt_total}/{nb_msg_total} traité")
        print(f"{cpt_saved} messages  enregistrés dans la base de données")
        print(f"\rPourcentage d'avancement : {
              round(cpt_total/nb_msg_total*100, 2)}%", end="", flush=True)
        time_delta = time.time() - time_begin
        print(f"Temps écoulé : {round(time_delta, 2)} secondes")
        # input()


if __name__ == "__main__":
    main()
