import spacy
from spacy.training.example import Example
from spacy.util import minibatch

def ModelTrainer(training: list[tuple[str, dict]], epochs: int, minibatch_size: int, model_path: str):
    '''
    Toma una lista de textos, con las etiquetas de sus tokens ordenados.
    Entrena un modelo con Part Of Speech (POS) y lo guarda en src/modelo_pos_es
    '''
    # Crea un modelo spacy vacío en español y le agrega el componente para haer 'tags'
    nlp = spacy.blank("es")
    tagger = nlp.add_pipe("tagger", last=True)

    # Añade las posibles etiquetas al modelo spacy
    etiquetas = ["ADJ", 
                 "ADP", 
                 "ADV", 
                 "AUX", 
                 "CCONJ", 
                 "INTJ", 
                 "NUM", 
                 "PART", 
                 "PROPN", 
                 "PUNCT", 
                 "SCONJ", 
                 "SYM", 
                 "X", 
                 "DET", 
                 "NOUN", 
                 "VERB", 
                 "PRON"
                 ]
    for etiqueta in etiquetas:
        tagger.add_label(etiqueta)

    # Convierte los datos de entrenamiento al formato de spacy
    examples: list[Example] = []
    for text, annotations in training:
        doc = nlp.make_doc(text)
        examples.append(Example.from_dict(doc, annotations))

    # Inicializar el optimizador
    optimizer = nlp.initialize()

    # Realizar múltiples épocas de entrenamiento
    for epoch in range(epochs):
        batches = minibatch(examples, size=minibatch_size)
        for batch in batches:
            nlp.update(batch, sgd=optimizer)
        print(f"Epoch {epoch+1}/{epochs}")
        
    # Guardar el modelo entrenado
    nlp.to_disk(model_path)
