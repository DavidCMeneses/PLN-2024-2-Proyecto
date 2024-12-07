import re

def Limpiar(texto: str)->str:
    '''
    Limpia las descripciones del dataset alfredplpl/artbench-pd-256x256
    para obtener descripciones más útiles
    '''
    texto = re.sub(r'[tT]he image shows a .*?painting of', '', texto)
    texto = re.sub(r'[pP]ainted by .*?\.', '.', texto)
    texto = re.sub(r'[tT]he painting is .*?\.', '', texto)
    texto = re.sub(r'[tT]he painting .*?a', 'a', texto)
    texto = re.sub(r'of the painting.', '.', texto)
    texto = re.sub(r', .*?the painting.*?.', '.', texto)
    texto = re.sub(r'[tT]he painting.*? of', '', texto)
    texto = texto.replace('  ', ' ')
    texto = texto.replace(' .', '.')
    texto = texto.replace(',.', '.')
    texto = texto.strip()
    return texto