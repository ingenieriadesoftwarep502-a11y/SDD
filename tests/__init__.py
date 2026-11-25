"""Paquete de pruebas.

Agrega src/ al path de importación para que las pruebas usen el paquete
`biblioteca` sin instalarlo (DEC-008). Se ejecuta con `python -m unittest -v`
desde la raíz del repositorio.
"""
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
