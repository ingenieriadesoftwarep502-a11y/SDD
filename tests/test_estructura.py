"""Pruebas de TASK-001: estructura base y entorno de pruebas."""
import unittest
from pathlib import Path

from tests import SRC


class TestEstructura(unittest.TestCase):

    def test_TEST_001_importa_paquete_desde_src(self):
        """TEST-001 (DEC-008): el paquete `biblioteca` se importa desde src/."""
        import biblioteca

        ruta_paquete = Path(biblioteca.__file__).resolve()
        self.assertTrue(ruta_paquete.is_relative_to(SRC))


if __name__ == "__main__":
    unittest.main()
