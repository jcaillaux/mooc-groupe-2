from fastapi import FastAPI
import config
import json
# Mes modules
from api.pipeline import Pipeline
from api.clusts import Clust

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

# route pour réccupérer les messages mooc de la base de données et créér un fichier jsonl
@app.get("/mooc_messages_from_db")
def get_mooc_messages_from_db():
    messages = Pipeline()
    messages_data = messages.db_messages_pipeline()
    return messages_data
    
# "J'ai rien compris. le language javascript est hyper complexe... je suis perdu."
# f"📌 Ce message appartient au cluster : {}")

@app.get("/get_closest_messages")
def get_closest_messages():
    """
    Cette fonction permet de récupérer les messages les plus proches d'un message donné.
    :param message: Message à vectoriser et à comparer.
    :return: Liste des messages les plus proches.
    """
    # Vectoriser le message
    embedder = Clust()

    message = "J'ai rien compris. le language javascript est hyper complexe... je suis perdu."
    cluster_id, top10 = embedder.from_messages_get_cluster_and_similar(message)
    
    
    return {"message": f"Le cluster de ce message est : {cluster_id} et les messages les plus proches sont : {top10}"}
        
        
















if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.RELOAD)
