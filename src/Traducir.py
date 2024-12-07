from googletrans import Translator
import traceback

translator = Translator()

def Traducir(texto: str)->str:
    '''
    Traduce un texto del inglés al español
    '''
    try:
        print('Traduciendo...')
        translator.translate(texto, src='en', dest='es').text
        print('Exito...')
    except Exception as e:
        print("############## ERROR ##############")
        print(e)
        traceback.print_exc()