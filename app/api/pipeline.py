import json
# Mes modules
from api.messages import MongoMessages
from api.mistral_embedding import MistralEmbedder
from api.clusts import Clust

class Pipeline:
    def __init__(self):
        pass
    
    def db_messages_pipeline(self):

        messages = MongoMessages()
        messages_data = messages.get_messages_data(limit_=5000, print_=False)

        embedder = MistralEmbedder()
        vectorized_messages = embedder.embed_messages(messages_data, batch_size=250)

        with open('api/outputs/mooc_messages.jsonl', 'w', encoding='utf-8') as f:
            for obj in messages_data:
                f.write(json.dumps(obj, ensure_ascii=False) + '\n')
        clusters = Clust()
        clusters.main_script(jsonl_input="api/outputs/mooc_messages.jsonl", jsonl_output="api/outputs/mooc_messages_clustered.jsonl", n_clusters=95)
        return {"message": "Clustering complet et sauvegardé dans mooc_messages_clustered.jsonl"}