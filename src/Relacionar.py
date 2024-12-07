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
    'atrás',
    'parte',
    'fondo',
    'plano',
}

patrones: list[list[str]] = [ # Ordenar según longitud de las listas!!!
    ['ADP', 'NOUN', 'ADP'],
    ['AUX', 'ADJ', 'ADP'],
    ['ADP', 'DET'],
    ['ADP']
]

def BuscarPatron(lista: list[Token], patron: list[str]):
    '''
    Busca si el patrón definido se encuentra entre los tokens dados
    '''
    n = len(patron)
    for i in range(len(lista) - n + 1):
        subsecuencia = [obj.pos_ for obj in lista[i:i+n]]
        if subsecuencia == patron:
            return lista[i:i+n]
    return None

def Relacionar(pos_entity1: int, 
               pos_entity2: int, 
               tokens: list[Token])->str | None:
    '''
    Encuentra la relación entre dos entidades (dada su posición de token)
    '''
    tokens_entre = tokens[pos_entity1+1:pos_entity2]
    for patron in patrones:
        relacion = BuscarPatron(tokens_entre, patron)
        if relacion:
            return " ".join([t.text for t in relacion])
    return None
    
