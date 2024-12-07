from googletrans import Translator

translator = Translator()

def Traducir(texto: str)->str:
    '''
    Traduce un texto del inglés al español
    '''
    return translator.translate(texto, src='en', dest='es').text