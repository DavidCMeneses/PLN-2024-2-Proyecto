from googletrans import Translator

translator = Translator()

def Traducir(texto: str)->str:
    return translator.translate(texto, src='en', dest='es').text