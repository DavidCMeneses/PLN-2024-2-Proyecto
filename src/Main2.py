from Dataset import LoadDataset
from Model import InfoImg
from Gemini import GeminiModel
import os
import time

# Cargar base de datos
print('\033[32mInicio...\033[0m')
time_ini = time.time()
print('\033[32mCargando dataset...\033[0m')
data_original = LoadDataset()

# Porcesar dataset
print('\033[32mObteniendo traducciones...\033[0m')
data: list[InfoImg] = []
for i in data_original:
    total_proceso = len(data_original[i])
    filtrados = 0
    for j in range(len(data_original[i])):
        # Armar dataset leyendo las traducciones
        print(f'Leyendo {j+1}/{total_proceso}')
        try:
            with open(os.path.join('src', 'ESP', f'{j}.txt')) as traduccion:
                data.append(InfoImg(j, data_original[i][j]['image'], traduccion.readline()))
        except: 
            filtrados += 1
            print(f"\033[31mFiltrados -> {filtrados}\033[0m")

# Referenciar JSONS
print('\033[32mGenerando Textos...\033[0m')
total_proceso = len(data)
for j, i in enumerate(data):
    print(f'Procesando {j+1}/{total_proceso}')
    i.json_path = os.path.join('src', 'JSON', f"{i.id}.json")
    if os.path.exists(i.json_path):
        i.description_generada = i.fromJSON()
        i.description_mejorada = GeminiModel(i.description_generada)
        time.sleep(3)
        i.generate_pdf()
        break
    else:
        print(f"\033[31mSin JSON\033[0m")
