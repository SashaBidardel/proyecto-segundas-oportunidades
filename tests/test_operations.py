import pytest
from data_base.operations import resetear_columnas_usuarios, insert_update_usuarios, calcular_cuotas_pagar, eliminar_registros_cero_beneficio, connect_mysql

@pytest.fixture
def db_connection():
    conn = connect_mysql()
    if conn is None:
        pytest.fail("No se pudo conectar a la base de datos")
    yield conn
    conn.close()

def test_resetear_columnas_usuarios(db_connection):
    resetear_columnas_usuarios(db_connection)
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT beneficios_anio, cantidad_a_pagar FROM usuarios")
        result = cursor.fetchall()
        for row in result:
            assert row[0] == 0.00  # beneficios_anio
            assert row[1] == 0.00  # cantidad_a_pagar

def test_insert_update_usuarios(db_connection):
    registros = [
        {'DNI__c': '12345678', 'Name': 'Juan Perez', 'Email__c': 'juan.perez@example.com', 'Beneficio': 100.00},
        {'DNI__c': '87654321', 'Name': 'Maria Lopez', 'Email__c': 'maria.lopez@example.com', 'Beneficio': 200.00}
    ]
    insert_update_usuarios(db_connection, registros)
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE dni_hash = '12345678'")
        result = cursor.fetchone()
        assert result is not None
        assert result[3] == 100.00  # beneficios_anio

def test_calcular_cuotas_pagar(db_connection):
    calcular_cuotas_pagar(db_connection)
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT cantidad_a_pagar FROM usuarios WHERE dni_hash = '12345678'")
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == 20.00  # cantidad_a_pagar

def test_eliminar_registros_cero_beneficio(db_connection):
    eliminar_registros_cero_beneficio(db_connection)
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE beneficios_anio = 0.00")
        result = cursor.fetchall()
        assert len(result) == 0
