# **Proyecto: Gestión de Productos Usados y Segundas Oportunidades**

## **1. Descripción del Proyecto**

El objetivo de este proyecto es poder desde la agencia tributaria pedir los datos fiscales de venta de un año determinado de una app de ventas de segunda mano(Segunda Oportunida)cuyos datos tenemos alojados en una org de Salesforce para ver los beneficios de ese año,si los hubiese,con su correspondiente carga fiscal(20% de los beneficios). <br>
Se pide un año fiscal desde la api de python que simula a la agencia tributaria y se obtienen los datos de la org de salesforce en donde están los usuarios de la aplicación Segunda Oportunidad, se actualizan y calculan beneficios, y se generan reportes en formato Excel. Además, se gestionan las ventas y se aplican validaciones específicas sobre los datos.

## **2. Requisitos**

### **2.1. Requisitos del Sistema**

- Python 3.7 o superior
- Salesforce
- MySQL
- Herramientas de desarrollo:
  - Visual Studio Code
  - Postman (para pruebas de API)
  
### **2.2. Requisitos de Bibliotecas**

- `simple_salesforce`
- `mysql-connector-python`
- `openpyxl`
- `pytest` (para pruebas unitarias)

## **3. Configuración del Entorno**

### **3.1. Creación del Entorno Virtual**

```bash
python -m venv venv
source venv/bin/activate (En Windows: venv\Scripts\activate)
```
### **3.2. Instalación de Dependencias**

```bash
pip install -r requirements.txt
```
### **3.3. Variables de Conexión**

```python
USERNAME=tu_usuario_salesforce
PASSWORD=tu_contraseña_salesforce
SECURITY_TOKEN=tu_token_de_seguridad_salesforce
DB_USER=tu_usuario_mysql
DB_HOST=tu_host_mysql
DB_PASSWORD=tu_contraseña_mysql
DB_NAME=nombre_base_datos
```
## **4. Implementación**
### **4.1. Configuración de Salesforce**
### **4.1.1 Objetos Custom creados:**
#### **Objeto Producto_Usado__c en Salesforce**
##### **El objeto Producto_Usado__c tiene los siguientes campos:**
 * CreatedById: Lookup(User)
 * Fecha_Venta__c: Date
 * LastModifiedById: Lookup(User)
 * OwnerId: Lookup(User, Group)
 * Precio_Compra__c: Currency(6, 2)
 * Precio_Venta__c: Currency(6, 2)
 * Name: Text(80)
 * Segunda_Oportunidad__c: Lookup(Segunda_Oportunidad__c)
 * Vendido__c: Checkbox


#### Objeto Segunda_Oportunidad__c en Salesforce
##### El objeto Segunda_Oportunidad__c tiene los siguientes campos:

* CreatedById: Lookup(User)
* DNI__c: Text(80) (Unique Case Insensitive)
* Email__c: Email
* LastModifiedById: Lookup(User)
* OwnerId: Lookup(User, Group)
* Name: Text(80)
### **4.1.2. Triggers y Validaciones**

#### **Trigger: UpdateVentaField:**
```java
    trigger UpdateVentaField on Producto_Usado__c (before insert, before update) {
    for (Producto_Usado__c producto : Trigger.new) {
        if (producto.Fecha_Venta__c != null) {
            producto.Vendido__c = true;
        }
        if (producto.Fecha_Venta__c == null && producto.Vendido__c == true) {
            producto.addError('Vendido no puede estar marcado sin Fecha de Venta.');
        }
        if (producto.Segunda_Oportunidad__c == null) {
            producto.addError('El campo Segunda Oportunidad es obligatorio.');
        }
        if (producto.Precio_Compra__c == null) {
            producto.addError('El campo Precio Compra es obligatorio.');
        }
        if (producto.Precio_Venta__c == null) {
            producto.addError('El campo Precio Venta es obligatorio.');
        }
    }
}
```

#### **Reglas de Validación:**

    DNI y Email obligatorios en Segunda_Oportunidad__c:
    AND(ISBLANK(DNI__c), ISBLANK(Email__c))
### **4.2. Estructura de la base de datos**

```sql
CREATE DATABASE segundoportunidad;

USE segundoportunidad;

CREATE TABLE usuarios (
    nombre VARCHAR(255) NOT NULL,
    dni_hash VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    beneficios_anio DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    cantidad_a_pagar DECIMAL(10,2) NOT NULL DEFAULT 0.00
);
```
## **5 Scripts de Python**
### **5.1 Main Script**

Ejecución de main.py:
```bash
python main.py
```

## **6. Pruebas**
### **6.1. Ejecución de Pruebas Unitarias**

Para ejecutar las pruebas unitarias, utilice el siguiente comando:
```bash
pytest tests/
```

## **7. Generación de Reportes**
### **7.1. Generación de Excel**

El script principal genera un archivo Excel con los datos de usuarios y beneficios calculados:

```python

generar_excel(conn)

```




