from PIL.JpegImagePlugin import JpegImageFile
from spacy.tokens import Token
from Relacionar import Relacionar, nouns_especiales
import json
import os
class Entity:
    '''
    Una entidad del texto
    '''
    def __init__(self, id: int, tipo: str, pos: int):
        self.id = id
        self.tipo = tipo
        self.pos_token = pos

class Relation:
    '''
    Una relación entre dos entidades del texto
    '''
    def __init__(self, 
                 entity1: Entity, 
                 entity2: Entity, 
                 tokens: list[Token]):
        self.id1 = entity1.id
        self.id2 = entity2.id
        self.relation = Relacionar(entity1.pos_token, entity2.pos_token, tokens)

class InfoImg:
    '''
    Codifica la información de una imagen
    '''
    def __init__(self, id: int, img: JpegImageFile, description: str):
        '''
        Inicializa la información de la imagen
        '''
        self.id = id
        self.img = img
        self.description = description
        self.entidades: list[Entity] = []
        self.relaciones: list[Relation] = []
        self.tokens: list[Token] = []

    def clear(self):
        '''
        Limpiar memoria (correr después de generar el JSON)
        '''
        self.entidades = []
        self.relaciones = []
        self.tokens = []

    def extraerEntidades(self):
        '''
        Extrae las entidades desde los tokens del texto
        '''
        for pos, token in enumerate(self.tokens):
            if token.text not in nouns_especiales and (token.pos_ == 'NOUN' or token.pos_ == 'PROPN'):
                self.addEntity(token.text, pos)

    def addEntity(self, entidad: str, pos: int):
        '''
        Añade una entidad
        '''
        self.entidades.append(Entity(len(self.entidades) + 1, entidad, pos))

    def relateEntities(self):
        '''
        Busca las relaciones entre las entidades del texto
        '''
        for i in range(len(self.entidades) - 1):
            relation = Relation(self.entidades[i], self.entidades[i+1], self.tokens)
            if relation.relation:
                self.relaciones.append(relation)

    def toJSON(self):
        '''
        Guarda las entidades y relaciones en un .json
        '''
        json_obj = {
            'objects':[{'id': entity.id, 'type': entity.tipo} for entity in self.entidades],
            'relations':[{'type': relation.relation, 'obj1': relation.id1, 'obj2': relation.id2} for relation in self.relaciones]
        }
        os.makedirs(os.path.join('src', 'JSON'), exist_ok=True)
        with open(os.path.join('src', 'JSON', f"{self.id}.json"), "w") as archivo_json:
            json.dump(json_obj, archivo_json, indent=4) 
        
