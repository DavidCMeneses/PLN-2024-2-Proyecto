cd /d "%~dp0"

python -m venv python_pln 2>NUL

if errorlevel 1 (
    echo No se pudo encontrar el comando "python", intentando con "python3"...
    python3 -m venv python_pln
    if errorlevel 1 (
        echo Error: No se pudo encontrar ni "python" ni "python3". Por favor, asegúrate de tener Python instalado.
        pause
        exit /b
    )
)

call python_pln\Scripts\pip install datasets nltk pandas matplotlib spacy

echo.
echo ========================================
echo Todas las librerías han sido instaladas.
echo ========================================
echo Cierre esta ventana.
pause
