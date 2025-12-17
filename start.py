"""
Launcher simplificado para la aplicación de detección de pose.
Este archivo permite ejecutar la aplicación desde la raíz del proyecto.

Uso:
    python start.py
"""

import sys
import os

# Añadir el directorio src al path de Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importar y ejecutar la aplicación principal
from main import main

if __name__ == "__main__":
    main()