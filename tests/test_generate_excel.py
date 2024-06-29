import unittest
from unittest.mock import patch, MagicMock
from excel.generate_excel import generar_excel

class TestGenerarExcel(unittest.TestCase):

    @patch('excel.generate_excel.pd.DataFrame.to_excel')
    @patch('builtins.print')
    def test_generar_excel(self, mock_print, mock_to_excel):
        # Crear una conexión mock
        conn = MagicMock()
        cursor = conn.cursor.return_value.__enter__.return_value
        cursor.fetchall.return_value = [
            ('12345678X', 'Juan Perez', 'juan@example.com', 100.00, 20.00)
        ]

        # Llamar a la función a probar
        generar_excel(conn)

        # Verificar que se llamó a cursor.execute con la consulta SQL correcta
        cursor.execute.assert_called_once_with("SELECT dni_hash, nombre, email, beneficios_anio, cantidad_a_pagar FROM usuarios")

        # Verificar que se llamó a to_excel con el archivo correcto
        mock_to_excel.assert_called_once_with('usuarios_data.xlsx', index=False)

        # Verificar que se imprimió el mensaje correcto
        mock_print.assert_called_with("Archivo Excel 'usuarios_data.xlsx' generado exitosamente")

if __name__ == '__main__':
    unittest.main()
