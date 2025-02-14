from PIL.JpegImagePlugin import JpegImageFile
from spacy.tokens import Token
from Relacionar import Relacionar, nouns_especiales
import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
import io

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
        self.description_generada = ""
        self.description_mejorada = ""
        self.entidades: list[Entity] = []
        self.relaciones: list[Relation] = []
        self.tokens: list[Token] = []
        self.json_path: str = ""

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

    def fromJSON(self) -> str:
        '''
        Carga el archivo JSON y lo procesa para generar una descripción base.
        Devuelve un string con la descripción.
        '''
        # Leer el archivo JSON
        with open(self.json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        
        # Extraer las entidades del JSON
        entities = {item['id']: item['type'] for item in data['objects']}
        
        # Conjunto para almacenar las entidades mencionadas en las relaciones
        mentioned_entities = set()
        
        # Procesar las relaciones
        description = []
        for relation in data['relations']:
            entity1 = entities[relation["obj1"]]
            entity2 = entities[relation["obj2"]]
            description.append(f"{entity1} {relation['type']} {entity2}.")
            
            # Añadir las entidades mencionadas a "mentioned_entities"
            mentioned_entities.add(entity1)
            mentioned_entities.add(entity2)
        
        # Buscar las entidades que no están mencionadas en ninguna relación
        non_mentioned_entities = [entity for id, entity in entities.items() if entity not in mentioned_entities]
        
        # Si hay entidades no mencionadas, agregarlas al final
        if non_mentioned_entities:
            if len(non_mentioned_entities) == 1:
                description.append(f"Hay {non_mentioned_entities[-1]}.")
            else:
                description.append(f"Hay {', '.join(non_mentioned_entities[:-1])} y {non_mentioned_entities[-1]}.")
        
        # Unir todo en un párrafo
        return " ".join(description)

    def generate_pdf(self):
        # Crear el documento PDF
        pdf_filename = os.path.join('src', "RESULTS", f"{self.id}.pdf")
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

        # Crear los elementos para el PDF
        elements = []

        # Convertir el objeto JpegImageFile a un archivo en memoria (BytesIO)
        img_io = io.BytesIO()
        self.img.save(img_io, format='JPEG')
        img_io.seek(0)  # Reposicionar al inicio del archivo en memoria

        # Crear el objeto Image de reportlab usando el archivo en memoria
        img = Image(img_io, width=200, height=100)  # Ajusta el tamaño de la imagen si es necesario
        elements.append(img)

        # Crear la tabla con 3 columnas
        data = [
            ["Descripción Original", "Descripción Generada", "Descripción Mejorada"],
            [self.description, self.description_generada, self.description_mejorada]
        ]

        # Estilos para la tabla
        table_style = TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Color de texto blanco para el encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.blue),  # Color de fondo para el encabezado
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alineación centrada
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Fuente
            ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),  # Espaciado inferior de las celdas
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Añadir bordes a las celdas
        ])

        # Crear la tabla
        table = Table(data)
        table.setStyle(table_style)
        elements.append(table)

        # Generar el PDF
        doc.build(elements)
        
