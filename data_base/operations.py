import mysql.connector
from config.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from salesforce.salesforce_operations import query_productos_usados

def connect_mysql():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        print("Conexión a MySQL exitosa")
        return conn
    except mysql.connector.Error as e:
        print(f"Error al conectar con MySQL: {e}")
        return None

def resetear_columnas_usuarios(conn):
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE usuarios SET beneficios_anio = 0.00, cantidad_a_pagar = 0.00"
            cursor.execute(sql)
        conn.commit()
        print("Columnas reseteadas en MySQL")
    except mysql.connector.Error as e:
        print(f"Error al resetear columnas en MySQL: {e}")

def procesar_productos_usados(sf, year):
    try:
        productos_usados = query_productos_usados(sf, year)
        
        registros_actualizar = []
        total_beneficios = 0.0
        
        for producto in productos_usados:
            precio_compra = float(producto['Precio_Compra__c'])
            precio_venta = float(producto['Precio_Venta__c'])
            beneficio = round(precio_venta - precio_compra, 2)
            
            if beneficio > 0:
                # Obtener información de la segunda oportunidad relacionada
                segunda_oportunidad_id = producto['Segunda_Oportunidad__c']
                query_so = f"""
                    SELECT Id, Name, DNI__c, Email__c
                    FROM Segunda_Oportunidad__c
                    WHERE Id = '{segunda_oportunidad_id}'
                """
                result_so = sf.query(query_so)
                if result_so['totalSize'] > 0:
                    oportunidad = result_so['records'][0]
                    dni = oportunidad['DNI__c']
                    nombre = oportunidad['Name']
                    email = oportunidad['Email__c']
                    
                    # Crear o actualizar registro en MySQL
                    registros_actualizar.append({
                        'DNI__c': dni,
                        'Name': nombre,
                        'Email__c': email,
                        'Beneficio': beneficio
                    })
                    
                    # Sumar al total de beneficios
                    total_beneficios += beneficio
        
        return registros_actualizar
    
    except Exception as e:
        print(f"Error durante el procesamiento de productos usados: {e}")
        return [], 0.0

def insert_update_usuarios(conn, registros):
    try:
        with conn.cursor() as cursor:
            for registro in registros:
                nombre = registro['Name']
                email = registro['Email__c']
                dni = registro['DNI__c']
                beneficio = round(float(registro['Beneficio']), 2)
                
                # Verificar si el DNI existe en la base de datos
                sql_select = "SELECT * FROM usuarios WHERE dni_hash = %s"
                cursor.execute(sql_select, (dni,))
                result = cursor.fetchone()
                
                if result:
                    # Actualizar registro existente
                    sql_update = "UPDATE usuarios SET beneficios_anio = beneficios_anio + %s WHERE dni_hash = %s"
                    cursor.execute(sql_update, (beneficio, dni))
                else:
                    # Insertar nuevo registro
                    sql_insert = "INSERT INTO usuarios (dni_hash, nombre, email, beneficios_anio) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql_insert, (dni, nombre, email, beneficio))
            
            conn.commit()
            print("Inserción o actualización de Segundas Oportunidades en MySQL completada")
    except mysql.connector.Error as e:
        print(f"Error al insertar o actualizar Usuarios en MySQL: {e}")

def calcular_cuotas_pagar(conn):
    try:
        with conn.cursor() as cursor:
            # Calcular el 20% de beneficios_anio y actualizar cantidad_a_pagar
            sql_update = """
                UPDATE usuarios
                SET cantidad_a_pagar = ROUND(beneficios_anio * 0.2, 2)
            """
            cursor.execute(sql_update)
        
        conn.commit()
        print("Cuota a pagar calculada y actualizada en MySQL")
    except mysql.connector.Error as e:
        print(f"Error al calcular cuota a pagar en MySQL: {e}")

def eliminar_registros_cero_beneficio(conn):
    try:
        with conn.cursor() as cursor:
            # Eliminar registros donde beneficios_anio sea cero
            sql_delete = "DELETE FROM usuarios WHERE beneficios_anio = 0.00"
            cursor.execute(sql_delete)
        
        conn.commit()
        print("Registros con beneficios cero eliminados en MySQL")
    except mysql.connector.Error as e:
        print(f"Error al eliminar registros con beneficios cero en MySQL: {e}")

