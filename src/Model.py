from PIL.JpegImagePlugin import JpegImageFile

class InfoImg:
    def __init__(self, id: int, img: JpegImageFile, description: str):
        '''
        Codifica la información de una imagen
        '''
        self.id = id
        self.img = img
        self.description = description
        self.entidades: set[str] = set()

    def addEntity(self, entidad: str):
        self.entidades.add(entidad)