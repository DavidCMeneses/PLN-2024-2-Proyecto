import spacy
import spacy.cli
from spacy.tokens import Token

modelo = "es_core_news_sm"
spacy.cli.download(modelo)

def Tokenizar(doc: str)->list[Token]:
    nlp = spacy.load(modelo)
    tokenization = nlp(doc)
    return tokenization