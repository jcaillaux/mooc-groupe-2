from config import SCHEMA, DATABASE_URL, VECTOR_DIMENSION
import os
from typing import Optional, List, Any
from sqlmodel import Field, Session, SQLModel, create_engine, text, select # pip install sqlmodel
from sqlalchemy import Column
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import mapped_column
from pydantic import BaseModel, ConfigDict, ValidationError


engine = create_engine(DATABASE_URL)


class message(SQLModel, table=True):
    __table_args__ = {'schema' : SCHEMA}
    __tablename__ = "message"

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: str = Field(default=None, primary_key=True)
    body: Optional[str] = Field(default=None)
    created_at: Optional[str] = Field(default=None)
    parent_id: Optional[str] = Field(default=None)
    thread_id: Optional[str] = Field(default=None)
    body_embedding : Optional[Any] = Field(sa_type=Vector(VECTOR_DIMENSION))

# Pour activer l'extension pgvector si nécessaire
def setup_pgvector():
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS VECTOR;"))
        conn.commit()

def create_db_and_tables():
    # Créer le schéma s'il n'existe pas
    with Session(engine) as session:
        session.exec(text(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}"))
        session.commit()
    # Créer l'extension pgvector si nécessaire
    setup_pgvector()
    # Créer les tables s'il n'existent pas
    SQLModel.metadata.create_all(engine)


def add_message(msg):
    with Session(engine) as session:
        # Vérifier si le message existe déjà en utilisant l'ID
        sql_request = select(message).where(message.id == msg.id)
        print(sql_request)
        existing_message = session.exec(sql_request).first()
        print(existing_message)
        
        if existing_message:
            # Si le message existe déjà, retourner son ID
            print(f"Message with ID {msg.id} already exists.")
            return existing_message.id
        else:
            # Si le message n'existe pas, l'ajouter et retourner son nouvel ID
            session.add(msg)
            session.commit()
            # Rafraîchir l'objet pour obtenir l'ID généré
            session.refresh(msg)
            return msg.id



        


def read_message(message_id: Optional[int] = None):
    with Session(engine) as session:
        if message_id:
            # Lecture d'un message spécifique
            sql_request = select(message).where(message.id == message_id)
            return session.exec(sql_request).first()
        else:
            # Lecture de tous les messages
            sql_request = select(message)
            return session.exec(sql_request).all()
        


def main():

   create_db_and_tables()
   print(SCHEMA)

if __name__ == "__main__":
    # A executer une seule fois pour créer la base de données et les tables
    # $ python -m app.PGSQL_functions
    main()

