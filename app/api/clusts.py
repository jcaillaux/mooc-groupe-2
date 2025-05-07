import json
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns
from joblib import dump
import pandas as pd
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from mistralai import Mistral



class Clust:
    def __init__(self):
        pass

    # === 1. CHARGER LES MESSAGES JSONL ===
    def load_messages(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f]

    # === 2. SAUVEGARDER AVEC CLUSTER_ID ===
    def save_messages(self, messages, path):
        with open(path, "w", encoding="utf-8") as f:
            for msg in messages:
                f.write(json.dumps(msg, ensure_ascii=False) + "\n")

    # === 3. CLUSTERISER LES VECTEURS ===
    def cluster_embeddings(self, messages, n_clusters=20):
        vectors = np.array([msg['vectorized'] for msg in messages])
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        kmeans.fit(vectors)

        # Ajouter cluster_id à chaque message
        for msg, label in zip(messages, kmeans.labels_):
            msg['cluster_id'] = int(label)

        return messages, kmeans

    # === 4. TROUVER LE CLUSTER D'UN NOUVEAU MESSAGE + SIMILAIRES ===
    def find_similar_messages(self, text, model, kmeans, messages, top_k=5):
        emb = model.encode(text, normalize_embeddings=True)

        cluster = kmeans.predict([emb])[0]
        cluster_msgs = [m for m in messages if m['cluster_id'] == cluster]

        cluster_vectors = np.array([m['vectorized'] for m in cluster_msgs])
        sims = cosine_similarity([emb], cluster_vectors)[0]

        # Ajouter similarité et trier
        for msg, score in zip(cluster_msgs, sims):
            msg['similarity'] = float(score)

        top_msgs = sorted(cluster_msgs, key=lambda m: m['similarity'], reverse=True)[:top_k]
        return cluster, top_msgs

    # === MAIN SCRIPT ===
    def main_script(self, jsonl_input="", jsonl_output="", n_clusters=95, messages=""):
        # === CONFIG ===
        JSONL_INPUT = jsonl_input
        JSONL_OUTPUT = jsonl_output
        N_CLUSTERS = n_clusters

        print("🔹 Chargement des messages...")
        messages = self.load_messages(JSONL_INPUT)

        print("🔹 Clusterisation avec KMeans...")
        messages, kmeans = self.cluster_embeddings(messages, n_clusters=N_CLUSTERS)

        print(f"🔹 Sauvegarde avec 'cluster_id' dans : {JSONL_OUTPUT}")
        self.save_messages(messages, JSONL_OUTPUT)


    # === SAUVEGARDE DU MODÈLE ===
        MODEL_PATH = "api/outputs/kmeans_model_full.pkl"
        dump(kmeans, MODEL_PATH)
        print(f"✅ Modèle KMeans sauvegardé dans : {MODEL_PATH}")

        # === VISUALISATION ===
        print("🔍 Réduction des dimensions pour visualisation...")

        vectors = np.array([msg["vectorized"] for msg in messages])
        labels = [msg["cluster_id"] for msg in messages]

        # t-SNE (2D)
        tsne = TSNE(n_components=2, random_state=42)
        reduced = tsne.fit_transform(vectors)

        # Créer un DataFrame pour visualisation
        df_viz = pd.DataFrame({
            "x": reduced[:, 0],
            "y": reduced[:, 1],
            "cluster": labels
        })

        plt.figure(figsize=(10, 8))
        ax = sns.scatterplot(x="x", y="y", hue="cluster", data=df_viz, palette="tab20", s=20)
        plt.title("Visualisation des clusters (t-SNE)")
        sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
        plt.tight_layout()
        plt.savefig("api/outputs/cluster_visualization_full.png")
        plt.show()

        print("📸 Visualisation enregistrée sous : cluster_visualization_full.png")


    def from_messages_get_cluster_and_similar(self, message=""):
        
        # === 1. Initialiser le client Mistral ===
        api_key = "5D6qWiGcW0q7sMoNJKnz7gvTQ7VinHue"  # ou mettre directement ta clé ici
        client = Mistral(api_key=api_key)

        # === 2. Message à classer ===
        message = message.strip()

        # === 3. Obtenir l'embedding avec Mistral ===
        response = client.embeddings.create(
            inputs=[message],
            model="mistral-embed"
        )
        embedding = response.data[0].embedding

        # === 4. Charger le modèle KMeans ===
        from joblib import load
        kmeans = load("api/outputs/kmeans_model_full.pkl")

        # === 5. Prédire le cluster ===
        cluster_id = kmeans.predict([embedding])[0]

        













        # === 6. Charger les messages vectorisés avec cluster_id ===
        with open("api/outputs/mooc_messages_clustered.jsonl", "r", encoding="utf-8") as f:
            messages = [json.loads(line) for line in f]

        # === 7. Extraire les messages dans le même cluster ===
        cluster_msgs = [m for m in messages if m.get("cluster_id") == int(cluster_id)]

        # === 8. Calculer la similarité cosinus avec ton embedding ===
        X_cluster = np.array([m["vectorized"] for m in cluster_msgs])
        similarities = cosine_similarity([embedding], X_cluster)[0]

        # === 9. Ajouter la similarité aux messages et trier ===
        for msg, score in zip(cluster_msgs, similarities):
            msg["similarity"] = score

        top10 = sorted(cluster_msgs, key=lambda m: m["similarity"], reverse=True)[:10]

        return cluster_id, top10

        # === 10. Afficher les 10 messages les plus proches ===
        # print(f"\n🔍 Top 10 messages les plus proches dans le cluster {cluster_id}:\n")
        # for i, msg in enumerate(top10, 1):
        #     content = msg.get("content", {})
        #     idd = msg.get("_id", "")
        #     body = content.get("body", "")[:120].replace("\n", " ")
        #     votes = content.get("votes", {}).get("count", 0)
        #     replies = content.get("comments_count", 0)

        #     print(f"{i}. {body}...")
        #     print(f"   👍 Votes : {votes} | 💬 Réponses : {replies} | 🔗 Sim : {msg['similarity']:.4f}\n")
            
        #     print(f"{i}. {idd}...")

                

            



























#     def from_messages_get_cluster_and_similar(self):





















    