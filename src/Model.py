from PIL.JpegImagePlugin import JpegImageFile

class Entity:
    def __init__(self, id: int, tipo: str):
        self.id = id
        self.tipo = tipo

class Relation:
    def __init__(self, 
                 entity1: Entity, 
                 entity2: Entity, 
                 texto: str,
                 entidades: set[str]):
        self.id1 = entity1.id
        self.id2 = entity2.id
        self.relation = None
        self.calcularRelation(texto, entidades)

    def calcularRelation(self, 
                         texto: str, 
                         entidades: set[str]):
        pass
class InfoImg:
    def __init__(self, id: int, img: JpegImageFile, description: str):
        '''
        Codifica la información de una imagen
        '''
        self.id = id
        self.img = img
        self.description = description
        self.entidades: list[Entity] = []
        self.entidades_set: set[str] = set()
        self.verbos_set: set[str] = set()
        self.auxiliary: set[str] = set()
        self.relaciones: list[Relation]

    def addEntity(self, entidad: str):
        self.entidades_set.add(entidad)
        self.entidades.append(Entity(len(self.entidades) + 1, entidad))

    def addVerb(self, verbo: str):
        pass

    def relateEntities(self):
        total_entidades = len(self.entidades)
        for i in range(total_entidades):
            for j in range(i+1, total_entidades):
                relation = Relation(self.entidades[i], self.entidades[j], self.description, self.entidades_set)
                if relation:
                    self.relaciones.append(relation)