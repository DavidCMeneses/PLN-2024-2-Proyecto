from Dataset import LoadDataset
from Traducir import Traducir
from Model import InfoImg
from Tokenizar import Tokenizar
from Limpiar import Limpiar
from Training import ModelTrainer
from Evaluate import ModelEvaluate
from sklearn.model_selection import KFold
import os
import time

# Cargar base de datos
print('\033[32mInicio...\033[0m')
time_ini = time.time()
print('\033[32mCargando dataset...\033[0m')
data_original = LoadDataset()

# Porcesar dataset
print('\033[32mTraduciendo dataset...\033[0m')
data: list[InfoImg] = []
for i in data_original:
    total_proceso = len(data_original[i])
    filtrados = 0
    for j in range(len(data_original[i])):
        print(f'Traduciendo {j+1}/{total_proceso}')
        # Limpiar caption
        texto_limpio = Limpiar(data_original[i][j]['caption'])
        # Filtrar
        if "paint" in texto_limpio:
            filtrados += 1
            print(f"\033[31mFiltrado -> {filtrados}\033[0m")
            continue
        # Traducir caption y armar dataset
        try:
            data.append(InfoImg(j, data_original[i][j]['image'], Traducir(texto_limpio)))
        except:
            time.sleep(5)
            try:
                data.append(InfoImg(j, data_original[i][j]['image'], Traducir(texto_limpio)))
            except:
                continue

# Creación de datos de entrenamiento suponiendo que el modelo 'es_core_news_md' etiqueta bien
print('\033[32mEtiquetando data...\033[0m')
data_etiquetada: list[tuple[str, dict]] = []
total_proceso = len(data)
for num in range(total_proceso):
    print(f'Etiquetando {num+1}/{total_proceso}')
    tokens = Tokenizar(data[num].description, "es_core_news_md")
    data_etiquetada.append((tokens.text, {"tags": []}))
    for token in tokens:
        data_etiquetada[-1][-1]['tags'].append(token.pos_)

# Entrenar modelos y validar con validación cruzada
print('\033[32mGenerando modelos...\033[0m')
num_modelos = 10
epochs = 10
mini_batch_size = 10
kf = KFold(n_splits=num_modelos, shuffle=True)
evaluations: list[float] = []
# Iterar sobre cada split que genera KFold
for idx, (train_index, val_index) in enumerate(kf.split(data_etiquetada)):
    # Dividir los datos en entrenamiento y validación
    print('\033[33mGenerando datos de entrenamiento...\033[0m')
    train_data = [data_etiquetada[i] for i in train_index]
    val_data = [data_etiquetada[i] for i in val_index]

    # Entrenar el modelo con los datos de entrenamiento
    os.makedirs(os.path.join('src', 'MODEL'), exist_ok=True)
    print(f"\033[33mEntrenando modelo {idx+1}/{num_modelos}\033[0m")
    ModelTrainer(train_data, epochs, mini_batch_size, os.path.join('src', 'MODEL', f'modelo_pos_es_{idx}'))

    # Evaluar el modelo con el conjunto de validación
    print(f"\033[33mEvaluando modelo {idx+1}/{num_modelos}\033[0m")
    evaluations.append(ModelEvaluate(val_data, os.path.join('src', 'MODEL', f'modelo_pos_es_{idx}')))

# Mostrar los resultados de la evaluación de cada modelo
print('\033[33mRESULTADO MODELOS:\033[0m')
for i, eval_result in enumerate(evaluations):
    print(f"Modelo {i + 1}: {eval_result}")
mejor_modelo = evaluations.index(max(evaluations))
print(f'\033[33mMejor modelo: {mejor_modelo}\033[0m')

# Tokenizar, procesar y crear JSON
print('\033[32mCreando JSONS...\033[0m')
total_proceso = len(data)
for num, i in enumerate(data):
    if num < 50: # Empezar desde textos que no se usaron para entrenar
        continue
    print(f'\033[33mTokenizando {num+1}/{total_proceso}\033[0m')
    tokens = Tokenizar(i.description, os.path.join('src', 'MODEL', f'modelo_pos_es_{mejor_modelo}'))
    for token in tokens:
        token.pos_ = token.tag_
        i.tokens.append(token)
    print(f'\033[32mProcesando {num+1}/{total_proceso}\033[0m')
    i.extraerEntidades()
    i.relateEntities()
    i.toJSON()
    i.clear()
print(f"Duración segundos: {time.time() - time_ini}")