from Dataset import LoadDataset
from Traducir import Traducir
from Model import InfoImg
from Tokenizar import Tokenizar
from Limpiar import Limpiar

# Cargar base de datos
print('Inicio...')
print('Cargando dataset...')
data_original = LoadDataset()

# Porcesar dataset
print('Traduciendo dataset...')
data: list[InfoImg] = []
for i in data_original:
    total_proceso = len(data_original[i])
    filtrados = 0
    for j in range(len(data_original[i])):
        if j > 350:
            break
        print(f'Traduciendo {j+1}/{total_proceso}')
        # Limpiar caption
        texto_limpio = Limpiar(data_original[i][j]['caption'])
        # Filtrar
        if "paint" in texto_limpio:
            filtrados += 1
            print(f"Filtrados -> {filtrados}")
            continue
        # Traducir caption y armar dataset
        data.append(InfoImg(j, data_original[i][j]['image'], Traducir(texto_limpio)))

# Tokenizar, procesar y crear JSON
print('Tokenizando dataset...')
total_proceso = len(data)
for num, i in enumerate(data):
    print(f'Tokenizando {num+1}/{total_proceso}')
    tokens = Tokenizar(i.description)
    for token in tokens:
        # print(f"{token.text} ----- {token.pos_}")
        i.tokens.append(token)
    print(f'Procesando {num+1}/{total_proceso}')
    i.extraerEntidades()
    i.relateEntities()
    i.toJSON()
    i.clear()