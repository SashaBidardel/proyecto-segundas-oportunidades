
from config.config import USERNAME, PASSWORD, SECURITY_TOKEN, DB_USER, DB_HOST, DB_PASSWORD, DB_NAME
from excel.generate_excel import generar_excel
from decimal import Decimal, ROUND_HALF_UP
from salesforce.salesforce_operations import authenticate_salesforce
from data_base.operations import connect_mysql, resetear_columnas_usuarios, insert_update_usuarios,calcular_cuotas_pagar, eliminar_registros_cero_beneficio,procesar_productos_usados

def main():
    sf = authenticate_salesforce()
    if not sf:
        return
    
    conn = connect_mysql()
    if not conn:
        return
    
    resetear_columnas_usuarios(conn)
    
    try:
        year = input("Ingrese el año fiscal que desea consultar: ")
        
        registros_actualizar= procesar_productos_usados(sf, year)
        
        # Actualizar MySQL con los registros obtenidos
        insert_update_usuarios(conn, registros_actualizar)
        
        # Calcular y actualizar cuotas a pagar
        calcular_cuotas_pagar(conn)
        
        # Eliminar registros donde beneficios_anio sea cero
        eliminar_registros_cero_beneficio(conn)
        
        # Generar archivo Excel con los datos de usuarios y beneficios
        generar_excel(conn)
        
    except Exception as e:
        print(f"Error durante la ejecución: {e}")
    finally:
        if conn:
            conn.close()
            print("Conexión a MySQL cerrada")

if __name__ == "__main__":
    main()
