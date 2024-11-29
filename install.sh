#!/bin/bash

# Cambia al directorio donde se encuentra el script
cd "$(dirname "$0")"

# Intentar crear un entorno virtual usando "python"
python -m venv python_pln 2>/dev/null

# Si el comando anterior falla, intentar con "python3"
if [ $? -ne 0 ]; then
    echo "No se pudo encontrar el comando 'python', intentando con 'python3'..."
    python3 -m venv python_pln
    if [ $? -ne 0 ]; then
        echo "Error: No se pudo encontrar ni 'python' ni 'python3'. Por favor, asegúrate de tener Python instalado."
        exit 1
    fi
fi

# Instalar las bibliotecas necesarias
python_pln/bin/pip install datasets nltk pandas matplotlib spacy pillow googletrans==4.0.0-rc1

# Informar al usuario que la instalación ha sido completada
echo
echo "========================================"
echo "Todas las librerías han sido instaladas."
echo "========================================"
echo "Cierre esta ventana."
