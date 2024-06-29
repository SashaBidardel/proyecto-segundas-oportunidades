from simple_salesforce import Salesforce
from config.config import USERNAME, PASSWORD, SECURITY_TOKEN

def authenticate_salesforce():
    try:
        sf = Salesforce(username=USERNAME, password=PASSWORD, security_token=SECURITY_TOKEN)
        print("Autenticación en Salesforce exitosa")
        return sf
    except Exception as e:
        print(f"Error al conectar con Salesforce: {e}")
        return None

def query_productos_usados(sf, year):
    try:
        query = f"""
            SELECT Id, Name, Precio_Compra__c, Precio_Venta__c, Segunda_Oportunidad__c
            FROM Producto_Usado__c
            WHERE Vendido__c = True AND CALENDAR_YEAR(Fecha_Venta__c) = {year}
        """
        result = sf.query(query)
        return result['records']
    except Exception as e:
        print(f"Error al ejecutar consulta SOQL para productos usados: {e}")
        return None
