import spacy
import spacy.cli
from spacy.tokens import Token

spacy.cli.download("es_core_news_md")

def Tokenizar(doc: str, modelo: str)->list[Token]:
    '''
    Toma un documento (doc) y lo tokeniza utilizando el modelo Spacy (modelo)
    '''
    nlp = spacy.load(modelo)
    tokenization = nlp(doc)
    return tokenization