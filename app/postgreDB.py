"""
Module de gestion de l'accès à la base de données PostgreSQL.
Utilise SQLModel et pgvector pour la gestion des messages et des embeddings.
"""

from typing import Optional, List, Any, Dict, Union
import logging

from sqlmodel import Field, Session, SQLModel, create_engine, text, select
from pgvector.sqlalchemy import Vector
from pydantic import ConfigDict

from config import SCHEMA, DATABASE_URL, VECTOR_DIMENSION



# Configuration du logger
logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.INFO,
#                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger.setLevel(logging.WARNING)

try :
    # Création de l'engine de base de données
    engine = create_engine(DATABASE_URL, echo=False)
except Exception :
    engine = 0
    print("No database available.")

class Message(SQLModel, table=True):
    """Modèle représentant un message dans la base de données."""

    __table_args__ = {"schema": SCHEMA}
    __tablename__ = "message"

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: str = Field(default=None, primary_key=True)
    body: Optional[str] = Field(default=None)
    created_at: Optional[str] = Field(default=None)
    parent_id: Optional[str] = Field(default=None)
    thread_id: Optional[str] = Field(default=None)
    course_id: Optional[str] = Field(default=None)
    body_embedding: Optional[Any] = Field(sa_type=Vector(VECTOR_DIMENSION))


# Fonctions de gestion de la base de données

def setup_pgvector():
    """Active l'extension pgvector si nécessaire."""
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS VECTOR;"))
        conn.commit()
        logger.info("Extension pgvector vérifiée/activée")


def create_schema():
    """Crée le schéma s'il n'existe pas."""
    with Session(engine) as session:
        session.exec(text(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}"))
        session.commit()
        logger.info(f"Schéma {SCHEMA} vérifié/créé")


def create_tables(drop_existing=False):
    """
    Crée les tables dans la base de données.

    Args:
        drop_existing: Si True, supprime les tables existantes avant de les recréer
    """
    if drop_existing:
        logger.warning("Suppression des tables existantes")
        SQLModel.metadata.drop_all(engine)

    logger.info("Création des tables")
    SQLModel.metadata.create_all(engine)


def initialize_database(drop_existing=False):
    """
    Initialise complètement la base de données.

    Args:
        drop_existing: Si True, supprime les tables existantes avant de les recréer
    """
    logger.info("Initialisation de la base de données")
    create_schema()
    setup_pgvector()
    create_tables(drop_existing)
    logger.info("Base de données initialisée avec succès")


# Fonctions repository pour les messages

def add_message(message):
    """
    Ajoute un message à la base de données.

    Args:
        message: L'objet Message à ajouter

    Returns:
        str: L'ID du message ajouté
    """
    with Session(engine) as session:
        # Vérifier si le message existe déjà en utilisant l'ID
        existing_message = session.exec(
            select(Message).where(Message.id == message.id)
        ).first()

        if existing_message:
            logger.info(f"Message with ID {message.id} already exists.")
            return existing_message.id

        # Ajout du nouveau message
        session.add(message)
        session.commit()
        session.refresh(message)
        logger.info(f"Message with ID {message.id} added successfully.")
        return message.id


def get_message_by_id(message_id):
    """
    Récupère un message par son ID.

    Args:
        message_id: L'ID du message à récupérer

    Returns:
        Optional[Message]: Le message trouvé ou None
    """
    with Session(engine) as session:
        return session.exec(
            select(Message).where(Message.id == message_id)
        ).first()


def get_all_messages():
    """
    Récupère tous les messages.

    Returns:
        List[Message]: Liste de tous les messages
    """
    with Session(engine) as session:
        return session.exec(select(Message)).all()


def update_message(message):
    """
    Met à jour un message existant.

    Args:
        message: L'objet Message avec les modifications

    Returns:
        bool: True si la mise à jour a réussi, False sinon
    """
    with Session(engine) as session:
        existing_message = session.exec(
            select(Message).where(Message.id == message.id)
        ).first()

        if not existing_message:
            logger.warning(f"Message with ID {
                           message.id} not found for update.")
            return False

        # Mise à jour des attributs
        # model_dump convertit en dict, exclude_unset=True pour ignorer les valeurs par défaut
        for key, value in message.model_dump(exclude_unset=True).items():
            # setattr permet de mettre à jour les attributs dynamiquement
            setattr(existing_message, key, value)

        session.add(existing_message)
        session.commit()
        logger.info(f"Message with ID {message.id} updated successfully.")
        return True


def delete_message(message_id):
    """
    Supprime un message par son ID.

    Args:
        message_id: L'ID du message à supprimer

    Returns:
        bool: True si la suppression a réussi, False sinon
    """
    with Session(engine) as session:
        message = session.exec(
            select(Message).where(Message.id == message_id)
        ).first()

        if not message:
            logger.warning(f"Message with ID {
                           message_id} not found for deletion.")
            return False

        session.delete(message)
        session.commit()
        logger.info(f"Message with ID {message_id} deleted successfully.")
        return True


def main():
    """Fonction principale pour initialiser la base de données."""
    initialize_database(drop_existing=False)
    logger.info(f"Database initialized in schema: {SCHEMA}")

try :
    # On initialise la base de donnees lors de l'importation du module
    initialize_database(drop_existing=False)
except Exception:
    print("No Database available")
if __name__ == "__main__":
    # A exécuter une seule fois pour créer la base de données et les tables
    # Dans main() penser à mettre drop_existing=True si on veut supprimer les tables existantes
    # $ python -m app.postgreDB
    main()
