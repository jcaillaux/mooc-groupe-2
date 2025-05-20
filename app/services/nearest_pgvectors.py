
from app.postgreDB import Message, engine
from sqlmodel import Session, text, select
from config import SCHEMA, DATABASE_URL, VECTOR_DIMENSION, NB_MESSAGES_PROPOSES
from pgvector.sqlalchemy import Vector
from app.services.text_embedding import get_text_embedding

def get_nearest_messages(prompt, k=NB_MESSAGES_PROPOSES):
    """
    Récupère les k vecteurs les plus proches de la base de données PostgreSQL.
    
    Args:
        prompt: Le texte à comparer
        k: Nombre de messages à proposer
    Returns:
        List[Message]: Liste des messages les plus proches
    """
    global engine
    
    embedded_prompt = get_text_embedding(prompt)

    with Session(engine) as session:
        # Option 1: Utiliser text() avec les paramètres directement dans la requête
        # Note: avec SQLModel.exec(), on ne peut pas passer de paramètres séparément comme avec execute()
        
        query = text(f"""
            SELECT *  FROM {SCHEMA}.message
            ORDER by body_embedding <=> :embedding      
            LIMIT :limit  
        """)

        embedded_prompt_str = '[' + ','.join([str(val) for val in embedded_prompt]) + ']'
        
        result = session.exec(query, params={
            "embedding": embedded_prompt_str,
            "limit": k  
        })
        
        # Reconstruction des objets Message à partir des résultats
        messages = []
        for row in result:
            msg = Message(
                id=row.id,
                body_embedding=row.body_embedding,
                body=row.body            
            )
            messages.append(msg)
        
        return messages


def main():

    # Test de la fonction       
    test_prompt = "émotion"
    list_msg = get_nearest_messages(test_prompt)

    #Affichage des ID et des corps des messages
    for msg in list_msg:
        print(f"ID: {msg.id}")
        print(f"Body: {msg.body[:500]}...")  # Print first 500 chars
        print("-" * 80)


if __name__ == "__main__":
    main()

