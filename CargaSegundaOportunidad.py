import random
import string
import hashlib
import traceback
from simple_salesforce import Salesforce
from config.config import USERNAME, PASSWORD, SECURITY_TOKEN

# Función para autenticar en Salesforce
def authenticate_salesforce():
    try:
        sf = Salesforce(username=USERNAME, password=PASSWORD, security_token=SECURITY_TOKEN)
        print("Autenticación en Salesforce exitosa")
        return sf
    except Exception as e:
        print(f"Error al conectar con Salesforce: {e}")
        return None

# Cargar registros aleatorios en Segunda Oportunidad en Salesforce
def load_random_records(sf, num_records):
    segunda_oportunidad_records = []
    for _ in range(num_records):
        random_string = generate_random_string(10)  # Genera una cadena aleatoria
        dni_hash = hashlib.sha256(random_string.encode()).hexdigest()[:15]  # Genera un hash SHA-256 y toma los primeros 15 caracteres
        email = f"{random_string.replace(' ', '').lower()}@example.com"  # Genera un email usando el nombre generado (asegura que esté en minúsculas)

        record = {
            'Name': random_string,
            'DNI__c': dni_hash,  # Usa el hash como valor para DNI__c
            'Email__c':email  # Genera un email usando el nombre generado

            
        }
        segunda_oportunidad_records.append(record)
    
    result = sf.bulk.Segunda_Oportunidad__c.insert(segunda_oportunidad_records)
    return result

# Función auxiliar para generar una cadena aleatoria
def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

if __name__ == "__main__":
    num_records = int(input("Ingrese el número de registros aleatorios que desea cargar en Segunda Oportunidad: "))

    # Autenticación en Salesforce
    sf = authenticate_salesforce()
    if not sf:
        exit()

    try:
        # Cargar registros aleatorios en Segunda Oportunidad en Salesforce
        result = load_random_records(sf, num_records)
        print(f"Se cargaron {len(result)} registros en Segunda Oportunidad.")
    except Exception as e:
        print(f"Error al cargar registros en Salesforce: {e}")
        traceback.print_exc()
