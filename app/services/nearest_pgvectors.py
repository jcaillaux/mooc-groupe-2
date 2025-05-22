
from app.postgreDB import Message, engine
from sqlmodel import Session, text, select
from config import SCHEMA, DATABASE_URL, VECTOR_DIMENSION, NB_MESSAGES_PROPOSES
from pgvector.sqlalchemy import Vector
from app.services.text_embedding import get_text_embedding


def get_neareast_threads(prompt, k=5, courses=None):
    """ 
    A Faire mais auparavant il me faut une BDD en bonne forme car je n'ai pas de course_id dans la base postgreSQL

    Args:
        prompt: Le texte à comparer
        k: Nombre de thread à proposer
        courses: Liste des k thread_id
    Returns:
        List[thread_id]: Liste des thread_id les plus proches
    """
    
    global engine

    # Embedding du prompt
    embedded_prompt = get_text_embedding(prompt)
    
    with Session(engine) as session:
       
        query = text(f"""
            SELECT *  
            FROM {SCHEMA}.message
            WHERE course_id = :course_id
            ORDER by body_embedding <=> :embedding      
            LIMIT :limit  
        """)
        
        embedded_prompt_str = '[' + ','.join([str(val) for val in embedded_prompt]) + ']'
        nb_msg = k * 5
        
        result = session.exec(query, params={
            "embedding": embedded_prompt_str,
            "limit": nb_msg,
            "course_id": courses
        })

        ensemble_thread_id = set()
        for msg in result:
            if msg.thread_id != '':
                ensemble_thread_id.add(msg.thread_id)
            else:
                ensemble_thread_id.add(msg.id)
        
        list_thread_id = list(ensemble_thread_id)[:k]    
    return list_thread_id


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

    # Test des fonctions       
    test_prompt = "ingénieur développeur"
    test_course_id = 'course-v1:MinesTelecom+04024+session01'
    #list_msg = get_nearest_messages(test_prompt)

    #Affichage des ID et des corps des messages
    #for msg in list_msg:
    #    print(f"ID: {msg.id}")
    #    print(f"Body: {msg.body[:500]}...")  # Print first 500 chars
    #    print("-" * 80)

    list_threads_id = get_neareast_threads(test_prompt, k=7, courses=test_course_id)
    print(f"{list_threads_id}")
    # Test de la fonction

if __name__ == "__main__":
    main()

