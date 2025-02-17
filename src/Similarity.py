from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy

# Convertir los textos en vectores TF-IDF
vectorizer = TfidfVectorizer()

# Cargar el modelo en español
nlp = spacy.load("es_core_news_sm")

def Similitud(txt1: str, txt2: str)->float:
    doc1 = " ".join([token.lemma_ for token in nlp(txt1)])
    doc2 = " ".join([token.lemma_ for token in nlp(txt2)])
    tfidf_matrix = vectorizer.fit_transform([doc1, doc2])

    # Calcular la similitud del coseno entre los dos vectores
    similitud = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return similitud[0][0]
