from Dataset import LoadDataset
from Traducir import Traducir
from Model import InfoImg
from Tokenizar import Tokenizar

# Cargar base de datos
print('Inicio...')
print('Cargando dataset...')
data_original = LoadDataset()

# Porcesar dataset
print('Procesando dataset...')
data: list[InfoImg] = []
for i in data_original:
    for j in range(len(data_original[i])):
        # Limpiar caption
        texto: str = data_original[i][j]['caption']
        texto = texto.replace('The image shows a painting of', '')
        texto = texto.strip()
        # Traducir caption y armar dataset
        data.append(InfoImg(j, data_original[i][j]['image'], Traducir(data_original[i][j]['caption'])))
        if j > 20:
            break

# Tokenizar
print('Tokenizando dataset...')
for i in data:
    tokens = Tokenizar(i.description)
    for token in tokens:
        if token.pos_ == 'NOUN':
            i.addEntity(token.text)
    
# Mostrar info
for i in data:
    print(f"\n----------\n{i.description}\n{i.entidades}\n----------\n")