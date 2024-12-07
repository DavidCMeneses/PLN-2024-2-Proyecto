from googletrans import Translator
from Dataset import LoadDataset
import os
import traceback
from Limpiar import Limpiar
import time

def Traducir(texto: str)->str:
    '''
    Traduce un texto del inglés al español
    '''
    translator = Translator()
    return translator.translate(texto, src='en', dest='es').text

# Cargar base de datos
print('\033[32mInicio...\033[0m')
print('\033[32mCargando dataset...\033[0m')
data_original = LoadDataset()

# Porcesar dataset
desde = 0
hasta = 2000
total_proceso = hasta - desde
print('\033[32mTraduciendo dataset...\033[0m')
os.makedirs(os.path.join('src', 'ESP'), exist_ok=True)
for i in data_original:
    for j in range(desde, hasta):
        print(f'Traduciendo {j+1}/{total_proceso}')
        # Limpiar caption
        texto_limpio = Limpiar(data_original[i][j]['caption'])
        # Filtrar
        if "paint" in texto_limpio:
            continue
        # Traducir caption y armar dataset
        try:
            traduccion = Traducir(texto_limpio)
        except:
            time.sleep(5)
            try:
                traduccion = Traducir(texto_limpio)
            except:
                print(f"\033[31mERROR {j}\033[0m")
                traceback.print_exc()
                continue
        with open(os.path.join('src', 'ESP', f'{j}.txt'), 'w') as archivo:
            archivo.write(traduccion)
            archivo.close()