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
    




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.RELOAD)
