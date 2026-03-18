#!/bin/bash

# Este script carga el entorno virtual de Python de la aplicación
# y lanza la rutina de despliegue en limpio (Destrucción y Reconstrucción total)

echo "=========================================================="
echo "    INICIANDO RUTINA DE DESPLIEGUE EN LIMPIO (FRESH)      "
echo "=========================================================="

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PYTHON_VENV="$DIR/../backend/venv/bin/activate"

if [ -f "$PYTHON_VENV" ]; then
    echo "[*] Activando entorno virtual de Python..."
    source "$PYTHON_VENV"
else
    echo "[!] Advertencia: No se detectó un entorno virtual en ../backend/venv."
    echo "[!] Intentando con la instalación global de Python..."
fi

# Ejecutar el script que contiene la manipulación SSL, SFTP y comandos Docker Destructivos
python3 "$DIR/fresh_deploy.py"
