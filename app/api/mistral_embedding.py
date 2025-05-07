from mistralai import Mistral

import time

class MistralEmbedder:
    def __init__(self, client=Mistral(api_key="5D6qWiGcW0q7sMoNJKnz7gvTQ7VinHue"), model="mistral-embed", batch_size=16):
        self.client = client
        self.model = model
        self.batch_size = batch_size

    
    def embed_messages(self, messages, batch_size=250):
        """
        Vectorise les messages par batchs, ajoute 'vectorized' à chacun.
        Gère les erreurs 429 avec retry.
        """
        total = len(messages)
        print(f"🚀 Traitement de {total} messages par batchs de {batch_size}...")

        for i in range(0, total, batch_size):
            batch = messages[i:i + batch_size]
            texts = []
            valid_msgs = []

            for msg in batch:
                text = msg.get('content', '').get('body', '').strip()
                if text:
                    texts.append(text)
                    valid_msgs.append(msg)

            if not texts:
                continue

            retries = 0
            success = False

            while not success and retries < 5:
                try:
                    response = self.client.embeddings.create(
                        inputs=texts,
                        model=self.model
                    )

                    for msg, emb in zip(valid_msgs, response.data):
                        msg['vectorized'] = emb.embedding
                        print(f"✅ {i + 1}/{total} : OK")

                    success = True

                except Exception as e:
                    if "429" in str(e) or "rate limit" in str(e).lower():
                        wait = 10 * (retries + 1)
                        print(f"⚠️ Rate limit — attente {wait}s (essai {retries+1}/5)")
                        time.sleep(wait)
                        retries += 1
                    else:
                        print(f"❌ Erreur batch {i}-{i+batch_size} : {e}")
                        for msg in valid_msgs:
                            msg['vectorized'] = None
                        break

            time.sleep(0.3)  # Pause entre chaque batch (important)

        print("✅ Tous les messages ont été traités.")
        return messages
    
    



