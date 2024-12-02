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
print('Procesando dataset...')
data: list[InfoImg] = []
for i in data_original:
    total_proceso = len(data_original[i])
    filtrados = 0
    for j in range(len(data_original[i])):
        if j > 40:
            break
        print(f'Limpiando {j}/{total_proceso}')
        # Limpiar caption
        texto_limpio = Limpiar(data_original[i][j]['caption'])
        # Filtrar
        if "paint" in texto_limpio:
            filtrados += 1
            print(f"Filtrados -> {filtrados}")
            continue
        # Traducir caption y armar dataset
        data.append(InfoImg(j, data_original[i][j]['image'], Traducir(texto_limpio)))

# Tokenizar
print('Tokenizando dataset...')
for i in data:
    tokens = Tokenizar(i.description)
    for token in tokens:
        print(f"{token.text} --- {token.pos_}")
        if token.pos_ == 'NOUN' | token.pos_ == 'PROPN':
            i.addEntity(token.text)
    
# Mostrar info
for i in data:
    print(f"\n----------\n{i.description}\n\n{i.entidades}\n----------\n")