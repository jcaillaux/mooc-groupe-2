import sys
import os
import time

# Add parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import functions
from app.Mongo_functions import read_msg, read_msg_by_id
from app.PGSQL_functions import message, add_message, read_message
from config import GEMINI_API_KEY, MISTRAL_API_KEY
from google import genai # pip install google-genai
from mistralai import Mistral
from sentence_transformers import SentenceTransformer

#client = genai.Client(api_key=GEMINI_API_KEY)
#model="gemini-embedding-exp-03-07"

#client = Mistral(api_key=MISTRAL_API_KEY)
#model = "mistral-embed"
# embeddings_batch_response = client.embeddings.create(
#    model=model,
#    inputs=["Embed this sentence.", "As well as this one."],
#)

# Modele sentence-transformers
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
#embeddings = model.encode(sentences)

def main(): 

    all_msg = read_msg()

    for msg in all_msg:
        # On cree une instance de la classe message
        mymessage = message()

        #On ne veut pas enregoistrer les messages dont le body est inexistant
        mymessage.body = msg.get('body', None)
        if mymessage.body is not None:
            mymessage.id = msg.get('id')
            mymessage.parent_id = msg.get('parent_id', None)
            mymessage.thread_id = msg.get('thread_id', None)
            #mymessage.body_embedding = client.models.embed_content(
            #    model=model,
            #    contents=mymessage.body
            #).embeddings[0].values
            
            #mymessage.body_embedding = client.embeddings.create(
            #    model=model,
            #    inputs=["Embed this sentence.", "As well as this one."],
            #)

            mymessage.body_embedding = model.encode(mymessage.body)
            mymessage.body_embedding = mymessage.body_embedding.tolist()
            
            print(len(mymessage.body_embedding))
            #add_message(mymessage)
            #time.sleep(1)
            input()
            
            
        #

        #read_message(mymessage.id)
        
            
        # Add message to PostgreSQL
        #add_message(mymessage)
        

    


if __name__ == "__main__":
    main()


