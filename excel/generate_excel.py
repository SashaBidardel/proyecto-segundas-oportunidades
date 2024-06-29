import pandas as pd
import mysql.connector
from config.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def generar_excel(conn):
    try:
        with conn.cursor() as cursor:
            # Obtener datos de usuarios de MySQL
            sql_select = "SELECT dni_hash, nombre, email, beneficios_anio, cantidad_a_pagar FROM usuarios"
            cursor.execute(sql_select)
            result = cursor.fetchall()

            # Crear DataFrame con los datos
            df = pd.DataFrame(result, columns=['DNI Hash', 'Nombre', 'Email', 'Beneficios Anio', 'Cantidad a Pagar'])

            # Guardar DataFrame como archivo Excel
            excel_file = 'usuarios_data.xlsx'
            df.to_excel(excel_file, index=False)
            
            print(f"Archivo Excel '{excel_file}' generado exitosamente")

    except mysql.connector.Error as e:
        print(f"Error al generar archivo Excel: {e}")
