from app.postgreDB import Message, engine
from sqlmodel import Session, text, select
from config import SCHEMA, DATABASE_URL, VECTOR_DIMENSION
from pgvector.sqlalchemy import Vector


def get_nearest_pgvectors(vector, k=5):
    """
    Récupère les k vecteurs les plus proches de la base de données PostgreSQL.

    Args:
        vector: Le vecteur à comparer
        k: Nombre de vecteurs à récupérer

    Returns:
        List[Message]: Liste des messages les plus proches
    """
    
    global engine
    
    with Session(engine) as session:
        # Option 1: Utiliser text() avec les paramètres directement dans la requête
        # Note: avec SQLModel.exec(), on ne peut pas passer de paramètres séparément comme avec execute()
        query_vector_str = str(vector).replace('[', '{').replace(']', '}')
        query = text(f"""
            SELECT id, content, body_embedding 
            FROM message
            ORDER BY body_embedding <-> '{query_vector_str}'::float[]
            LIMIT {k}
        """)
        
        result = session.exec(query)
        
        # Reconstruction des objets Message à partir des résultats
        messages = []
        for row in result:
            msg = Message(
                id=row.id,
                content=row.content,
                body_embedding=row.body_embedding
            )
            messages.append(msg)
        
        return messages


def main():
    with Session(engine) as session:
        test_message = session.exec(
            select(Message)
            .where(Message.id == '52ef5f60919cec5e32000962')
        ).first()
        
        if test_message is None:
            print("Test message not found")
            return
        
        list_msg = get_nearest_pgvectors(test_message.body_embedding, k=5)
        
        for msg in list_msg:
            print(f"ID: {msg.id}")
            print(f"Body: {msg.body[:100]}...")  # Print first 100 chars
            print("-" * 80)

         #   print(f"ID: {msg.id}, Body: {msg.body}, Distance: {msg.body_embedding.l2_distance(test_message.body_embedding)}")

if __name__ == "__main__":
    main()

