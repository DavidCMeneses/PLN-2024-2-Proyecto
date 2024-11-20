set "DIRECTORIO=%~dp0"
cd /d "%DIRECTORIO%"

start cmd /k "cd /d %DIRECTORIO% && python_pln\Scripts\python Main.py"

pause