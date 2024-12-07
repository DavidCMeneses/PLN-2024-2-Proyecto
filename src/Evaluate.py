from Tokenizar import Tokenizar
import numpy as np

def ModelEvaluate(validation: list[tuple[str, dict]], model_path: str)->float:
    '''
    Toma un modelo y lo evalua con los datos de validación
    '''
    valor_evaluacion: list[float] = []

    for (doc, tags) in validation:
        # Tokenizar textos con el modelo
        tokens = Tokenizar(doc, model_path)

        # Contar aciertos y errores
        aciertos = 0
        errores = 0
        for i in range(len(tokens)):
            if tokens[i].tag_ == tags['tags'][i]:
                aciertos += 1
            else:
                errores += 1

        # Calcular porcentaje de éxito
        valor_evaluacion.append(aciertos / (aciertos + errores))
    
    # Devolvemos el promedio de los porcentajes de éxito
    return np.mean(valor_evaluacion)
