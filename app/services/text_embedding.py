from sentence_transformers import SentenceTransformer

model =  SentenceTransformer(
        'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
print("Modèle chargé : ", model)


def get_text_embedding(input_text):
    """
    Calcule l'embedding d'un texte donné.

    Args:
        text: Le texte à encoder

    Returns:
        List[float]: L'embedding du texte
    """

    embedded_text = model.encode(
                   input_text, show_progress_bar=False)
    
    return embedded_text.tolist()

if __name__ == "__main__":
    # Test de la fonction
    text = "Bonjour, comment ça va ?"
    embedding = get_text_embedding(text)
    print("Embedding : ", embedding)
    print("Taille de l'embedding : ", len(embedding))

