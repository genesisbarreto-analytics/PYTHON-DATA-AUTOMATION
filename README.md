# 🐍 Python Data Automation

Repositorio público con ejemplos anonimizados de **automatización, procesamiento y transformación de datos con Python**, basados en flujos profesionales de Data Analytics.

El objetivo es mostrar cómo utilizo Python para reducir tareas manuales, validar información, transformar archivos y automatizar cargas hacia bases de datos.

> 🔒 Las rutas, servidores, bases de datos, nombres internos, URLs productivas e identificadores sensibles fueron reemplazados por configuraciones genéricas para proteger información confidencial.

---

## 🎯 ¿Qué demuestra este repositorio?

- Automatización de procesos repetitivos.
- Procesamiento de archivos Excel y CSV con `Pandas`.
- Validación de estructuras y columnas.
- Limpieza y normalización de datos.
- Aplicación de reglas de negocio.
- Generación automática de archivos CSV.
- Integración con SQL Server mediante `PyODBC`.
- Cargas masivas mediante batch processing.
- Manejo de errores y generación de logs.
- Uso de variables de entorno para configuraciones.
- Preparación de datos para procesos analíticos posteriores.

---

# 📄 Proyecto 01 — Automated Data Cleaning & CSV Generation

### Problema

La preparación de archivos para campañas o procesos operativos puede requerir múltiples tareas manuales:

- validar columnas;
- revisar formatos;
- filtrar registros;
- limpiar información;
- generar estructuras específicas;
- exportar el archivo final.

Esto aumenta el tiempo operativo y el riesgo de errores.

### Solución

Desarrollé un proceso en Python que automatiza la transformación de una base Excel en un archivo CSV estructurado y validado.

El script:

1. Lee automáticamente el archivo de origen.
2. Valida que existan las columnas requeridas.
3. Normaliza los valores.
4. Aplica reglas de calidad.
5. Filtra registros válidos.
6. Genera parámetros de salida.
7. Construye el archivo CSV final.
8. Ejecuta validaciones antes de finalizar el proceso.

### Flujo del proceso

`Excel`

↓

`Validación de estructura`

↓

`Limpieza`

↓

`Reglas de negocio`

↓

`Filtrado`

↓

`Transformación`

↓

`CSV final`

### Técnicas utilizadas

`Python` `Pandas` `Data Validation` `Data Cleaning` `CSV` `URL Encoding`

### 📄 Ver código

➡️ [01_automated_data_cleaning_csv.py](./01_automated_data_cleaning_csv.py)

---

# ⚙️ Proyecto 02 — CSV to SQL Server ETL Automation

### Problema

Los procesos de carga de información pueden requerir identificar manualmente archivos, revisar su estructura, limpiar columnas y posteriormente insertar los registros en una base de datos.

Cuando estos procesos se ejecutan de manera recurrente, la operación manual aumenta el tiempo de ejecución y dificulta la trazabilidad.

### Solución

Desarrollé un proceso ETL con Python que automatiza el flujo desde la identificación del archivo hasta su carga en SQL Server.

El proceso:

1. Identifica automáticamente el archivo CSV más reciente.
2. Detecta el delimitador utilizado.
3. Detecta el encoding del archivo.
4. Lee la información utilizando Pandas.
5. Limpia y normaliza los nombres de las columnas.
6. Elimina duplicidades en los nombres de campos.
7. Estandariza valores nulos.
8. Establece conexión con SQL Server mediante ODBC.
9. Valida o crea la tabla destino.
10. Ejecuta inserciones en lotes.
11. Genera logs del proceso.
12. Maneja errores mediante excepciones.

### Flujo del proceso

`CSV`

↓

`Detección de archivo`

↓

`Encoding + delimitador`

↓

`Pandas`

↓

`Limpieza y normalización`

↓

`Validación`

↓

`ODBC`

↓

`Batch Insert`

↓

`SQL Server`

↓

`Logs`

### Técnicas utilizadas

`Python` `Pandas` `PyODBC` `ETL` `Batch Processing` `Logging` `SQL Server`

### 📄 Ver código

➡️ [02_csv_to_sql_server_etl.py](./02_csv_to_sql_server_etl.py)

---

# 🔍 Decisiones técnicas

## Procesamiento con Pandas

Pandas permite trabajar con archivos estructurados de forma flexible, aplicando reglas de limpieza, validación y transformación antes de exponer la información a otros procesos.

## Validaciones antes de procesar

Los scripts incorporan controles para evitar continuar cuando:

- faltan columnas requeridas;
- el archivo está vacío;
- existen valores inválidos;
- no se encuentra el archivo esperado;
- falla la conexión con la base de datos.

## Batch Processing

En cargas SQL se utilizan inserciones por lotes para evitar ejecutar una operación independiente por cada registro.

Esto permite estructurar procesos más escalables.

## Logging

Los procesos generan información de ejecución para facilitar:

- seguimiento;
- diagnóstico de errores;
- validación de registros procesados;
- trazabilidad de cargas.

## Configuración externa

La versión pública utiliza variables de entorno para evitar incorporar en el código:

- servidores;
- bases de datos;
- rutas productivas;
- configuraciones sensibles.

---

# 🧠 Cómo utilizo Python dentro de Analytics

Python funciona como una capa complementaria dentro de mis procesos de datos.

Mi flujo habitual puede representarse como:

`Fuente de datos`

↓

`Python`

↓

`Limpieza / Validación`

↓

`Transformación`

↓

`Base de datos`

↓

`SQL`

↓

`Power BI`

Esto permite automatizar tareas que anteriormente requerían intervención manual y preparar información consistente para análisis posterior.

---

# 🛠️ Tecnologías

### Programming

`Python`

### Data Processing

`Pandas` `Excel` `CSV`

### Database Integration

`PyODBC` `SQL Server`

### Automation

`ETL` `Batch Processing` `Logging`

### Data Management

`Data Cleaning` `Data Validation` `Data Transformation`

---

# 🔐 Privacidad

Los scripts publicados son versiones **portfolio-safe** basadas en procesos profesionales.

No contienen:

- credenciales;
- contraseñas;
- servidores internos;
- nombres de bases corporativas;
- rutas personales;
- nombres de clientes;
- RUT;
- teléfonos reales;
- correos internos;
- URLs privadas.

Las configuraciones sensibles fueron reemplazadas por ejemplos genéricos y variables de entorno.

---

# 👩‍💻 Sobre mí

**Genesis Barreto**

Data Analytics | Business Intelligence

Trabajo transformando datos en información accionable mediante **Power BI, SQL, Python y Databricks**, combinando automatización, análisis y conocimiento de negocio.

### Conecta conmigo

💼 [LinkedIn](https://www.linkedin.com/in/g%C3%A9nesis-barreto-884620137/)

🐙 [GitHub](https://github.com/genesisbarreto-analytics)

---

### Datos → Automatización → Transformación → Analytics → Decisión
