
from app.postgreDB import Message, engine
from sqlmodel import Session, text, select
from config import SCHEMA, DATABASE_URL, VECTOR_DIMENSION, NB_MESSAGES_PROPOSES
from pgvector.sqlalchemy import Vector
from app.services.text_embedding import get_text_embedding


def get_neareast_threads(prompt, k=NB_MESSAGES_PROPOSES, courses=None):
    """ 
    A Faire mais auparavant il me faut une BDD en bonne forme car je n'ai pas de course_id dans la base postgreSQL

    """

    global engine

    embedded_prompt = get_text_embedding(prompt)
    with Session(engine) as session:
        # Option 1: Utiliser text() avec les paramètres directement dans la requête
        # Note: avec SQLModel.exec(), on ne peut pas passer de paramètres séparément comme avec execute()

        query = text(f"""
            SELECT *
            FROM {SCHEMA}.message
            WHERE course_id = :course_id
            ORDER by body_embedding <=> :embedding
            LIMIT :limit
        """)

        embedded_prompt_str = '[' + \
            ','.join([str(val) for val in embedded_prompt]) + ']'

        result = session.exec(query, params={
            "embedding": embedded_prompt_str,
            "limit": k,
            "course_id": courses
        })

        # Reconstruction des objets Message à partir des résultats
        list_threads_id = set()
        for row in result:
            list_threads_id.add(row.thread_id)

    return list_threads_id


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

        embedded_prompt_str = '[' + \
            ','.join([str(val) for val in embedded_prompt]) + ']'

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
                body=row.body,
                thread_id=row.thread_id
            )
            messages.append(msg)

        return messages


def main():

    # Test de la fonction
    test_prompt = "ingénieur"
    test_course_id = 'CNAM/01002/Trimestre_1_2014'
    # list_msg = get_nearest_messages(test_prompt)

    # Affichage des ID et des corps des messages
    # for msg in list_msg:
    #    print(f"ID: {msg.id}")
    #    print(f"Body: {msg.body[:500]}...")  # Print first 500 chars
    #    print("-" * 80)

    list_threads_id = get_neareast_threads(
        test_prompt, k=10, courses=test_course_id)

    print("Liste des threads ID : ", list_threads_id)
    # Test de la fonction


if __name__ == "__main__":
    main()
