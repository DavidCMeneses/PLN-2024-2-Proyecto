#!/bin/bash

# Captura el directorio donde se encuentra el script
DIRECTORIO=$(cd "$(dirname "$0")" && pwd)

# Este comando inicia la API de la base de datos ICREA en una nueva terminal
osascript -e "tell application \"Terminal\" to do script \"cd '$DIRECTORIO' && python_pln/bin/python3 Main.py\""
