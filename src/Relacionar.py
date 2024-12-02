from spacy.tokens import Token

nouns_especiales: set[str] = {
    'medio',
    'arriba',
    'abajo',
    'izquierda',
    'derecha',
    'debajo',
    'lado',
    'frente',
    'detrás',
    'atrás'
}

def BuscarPatron(lista: list[Token], patron: list[str]):
    n = len(patron)
    for i in range(len(lista) - n + 1):
        subsecuencia = [obj.pos_ for obj in lista[i:i+n]]
        if subsecuencia == patron:
            return lista[i:i+n]
    return None

def Relacionar(pos_entity1: int, 
               pos_entity2: int, 
               tokens: list[Token])->str | None:
    tokens_entre = tokens[pos_entity1+1:pos_entity2]
    relacion = BuscarPatron(tokens_entre, ['ADP', 'NOUN', 'ADP'])
    if relacion:
        return " ".join([t.text for t in relacion])
    relacion = BuscarPatron(tokens_entre, ['AUX', 'ADJ', 'ADP'])
    if relacion:
        return " ".join([t.text for t in relacion])
    return None
    
