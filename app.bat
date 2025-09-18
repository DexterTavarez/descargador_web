@echo off
REM -------------------------------
REM Setup automático para Windows
REM -------------------------------

echo Creando entorno virtual...
python -m venv venv

echo Activando bypass de PowerShell...
powershell -Command "Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass"

echo Activando entorno virtual...
call venv\Scripts\activate.bat

echo Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt

echo Todo listo. Para iniciar la app, ejecuta:
echo python app.py
pause
