# ETL - Datos Regulatorios Sistemas Aislados 🔌

Sistema ETL (Extract, Transform, Load) para la carga automatizada de datos regulatorios de sistemas eléctricos aislados desde archivos Excel a una base de datos SQL Server.

## 📋 Descripción

Este proyecto automatiza el proceso de extracción, transformación y carga de datos regulatorios para sistemas de distribución eléctrica aislados. Lee información de múltiples hojas de Excel y las carga en tablas normalizadas de SQL Server, asegurando la integridad y consistencia de los datos.

### Datos Procesados

El sistema procesa tres tipos principales de información:

- **Centros de Transformación MT/BT**: Información sobre transformadores, capacidades, propietarios y ubicaciones
- **Equipos de Maniobras**: Cuchillas, interruptores y otros equipos de la red de distribución
- **Interrupciones**: Registro de eventos programados y no programados del servicio eléctrico

##  Características

- ✅ **Carga Masiva**: Procesa múltiples archivos Excel en una sola ejecución
- ✅ **Mapeo Inteligente**: Maneja variaciones en nombres de columnas automáticamente
- ✅ **Limpieza de Datos**: Normaliza espacios, convierte tipos de datos y valida información
- ✅ **Logging Detallado**: Registra todas las operaciones con timestamps y niveles de detalle
- ✅ **Manejo de Errores**: Continúa procesando otros archivos aunque uno falle
- ✅ **Configuración Segura**: Usa variables de entorno para credenciales sensibles
- ✅ **Validaciones**: Detecta problemas de desbordamiento y truncamiento antes de cargar

## 🛠️ Requisitos Previos

### Software Necesario

- **Python 3.8+**
- **SQL Server 2016+** (Express, Standard, o Enterprise)
- **ODBC Driver 17 for SQL Server** (o superior)
- **Microsoft Excel** (para crear/editar archivos fuente)

### Paquetes Python

```
pandas>=1.5.0
pyodbc>=4.0.0
sqlalchemy>=1.4.0
python-dotenv>=0.19.0
openpyxl>=3.0.0
```

## 📦 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/etl-sistemas-aislados.git
cd etl-sistemas-aislados
```

### 2. Crear Entorno Virtual

```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En Linux/Mac
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Configuración SQL Server
SQL_SERVER=localhost\MSSQLSERVER01
SQL_DATABASE=datos_regulatorios_reco
SQL_USERNAME=tu_usuario
SQL_PASSWORD=tu_contraseña
SQL_DRIVER=ODBC Driver 17 for SQL Server
SQL_USE_WINDOWS_AUTH=false

# Ruta de archivos Excel
EXCEL_FOLDER=C:\Datos\Excel
```

**Nota**: Usa `SQL_USE_WINDOWS_AUTH=true` si prefieres autenticación de Windows.

### 5. Crear las Tablas en SQL Server

Ejecuta el script de creación de tablas:

```bash
# Si tienes el script SQL
sqlcmd -S localhost\MSSQLSERVER01 -d datos_regulatorios_reco -i create_tables.sql

# O ejecuta manualmente en SSMS
```

Ver [create_tables.sql](./sql/create_tables.sql) para el script completo.

## Uso

### Ejecución Básica

```bash
python etl_sistemas_aislados.py
```

### Flujo de Trabajo

1. El script busca todos los archivos Excel (`.xlsx`, `.xls`) en la carpeta configurada
2. Para cada archivo, procesa las hojas:
   - `Centro MTBT` → Tabla `Centro MTBT`
   - `Equipos de maniobras` → Tabla `Equipos de maniobras`
   - `Interrupciones` → Tabla `Interrupciones`
3. Limpia y valida los datos antes de cargar
4. Inserta los datos en SQL Server
5. Genera un log detallado en `logs/etl_YYYYMMDD_HHMMSS.log`

### Ejemplo de Salida

```
============================================================
INICIO DEL PROCESO DE CARGA MASIVA
============================================================

✓ Se encontraron 2 archivo(s) Excel:
  1. Plantilla_AGOSTO.xlsx
  2. Plantilla_SEPTIEMBRE.xlsx

============================================================
Procesando: Centro MTBT → Centro MTBT
============================================================
✓ Datos leídos: 857 filas, 6 columnas
✓ Datos limpiados: 857 filas válidas
✓ Datos cargados exitosamente a la tabla 'Centro MTBT'

============================================================
RESUMEN GENERAL DEL PROCESO
============================================================
Total de operaciones exitosas: 6
Total de errores: 0
Total de filas cargadas: 2,240
============================================================
```

## 📊 Estructura de Datos

### Tabla: Centro MTBT

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id` | INT IDENTITY | Identificador único (auto-incremental) |
| `Código Centro de transformación MT/BT` | VARCHAR(100) | Código único del centro de transformación |
| `KVA instalado por transformador` | DECIMAL(10,2) | Capacidad en KVA |
| `Equipo aguas arriba` | VARCHAR(500) | Código(s) del equipo alimentador |
| `Propietario` | VARCHAR(100) | RECO o USUARIO (PRIVADO) |
| `UTM Centro MT/BT Norte` | BIGINT | Coordenada UTM Norte |
| `UTM Centro MT/BT Oeste` | BIGINT | Coordenada UTM Oeste |

### Tabla: Equipos de maniobras

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id` | INT IDENTITY | Identificador único |
| `Código de equipo` | VARCHAR(100) | Código único del equipo |
| `Tipo de equipo` | VARCHAR(100) | Cuchilla monopolar, cortacircuito, etc. |
| `Código de subestación` | VARCHAR(100) | Subestación asociada |
| `Codigo de Equipo Aguas Arriba` | VARCHAR(500) | Equipo(s) alimentador(es) |
| `Nivel de tensión` | DECIMAL(6,2) | Tensión en kV |
| `Corriente máxima` | BIGINT | Corriente nominal en Amperes |
| `UTM Equipo Norte` | BIGINT | Coordenada UTM Norte |
| `UTM Equipo Oeste` | BIGINT | Coordenada UTM Oeste |

### Tabla: Interrupciones

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id` | INT IDENTITY | Identificador único |
| `ID_Interrupcion` | VARCHAR(50) | Código de la interrupción (IP#### o I####) |
| `Fecha y Hora_Inicio` | DATETIME2 | Inicio de la interrupción |
| `Fecha y Hora_Cierre` | DATETIME2 | Fin de la interrupción |
| `Causa` | VARCHAR(255) | Despeje Programado / No Programado |
| `Fecha Notificacion al Usuario` | DATETIME2 | Fecha de notificación previa |
| `Origen del evento` | VARCHAR(100) | DISTRIBUCION / TRANSMISION / EXTERNO |
| `Código de Equipo` | VARCHAR(500) | Equipo(s) afectado(s) |
| `Enlace Medio de Notificacion a los Usuarios` | VARCHAR(500) | URL de notificación (Facebook, etc.) |
| `Observaciones` | VARCHAR(MAX) | Descripción detallada del evento |
| `CódigoDePrimerEquipo` | VARCHAR(100) | Primer equipo de la lista (automático) |

## 📁 Estructura del Proyecto

```
etl-sistemas-aislados/
│
├── etl_sistemas_aislados.py    # Script principal del ETL
├── .env                         # Variables de entorno (no incluir en Git)
├── .env.example                 # Plantilla de variables de entorno
├── requirements.txt             # Dependencias Python
├── README.md                    # Este archivo
│
├── logs/                        # Logs de ejecución (auto-generados)
│   └── etl_YYYYMMDD_HHMMSS.log
│
├── sql/                         # Scripts SQL
│   ├── create_tables.sql       # Creación de tablas
│   └── fix_columns.sql         # Correcciones de estructura
│
└── data/                        # Archivos Excel (ejemplo)
    └── Plantilla_Template.xlsx
```

## 🔧 Configuración Avanzada

### Cambiar Comportamiento de Carga

En `etl_sistemas_aislados.py`, línea ~285:

```python
resultados = cargar_excel_a_sql(
    archivo_excel=str(archivo),
    tabla_sheet_map=TABLE_NAMES,
    engine=engine,
    if_exists='append'  # Opciones: 'append', 'replace', 'fail'
)
```

**Opciones**:
- `'append'`: Agrega datos a tablas existentes (por defecto)
- `'replace'`: Reemplaza todos los datos existentes
- `'fail'`: Falla si la tabla ya existe

### Personalizar Mapeo de Columnas

Edita el diccionario `COLUMN_MAPPINGS` (línea ~80) para agregar variaciones de nombres:

```python
COLUMN_MAPPINGS = {
    'Centro MTBT': {
        'Código Centro MT/BT': 'Código Centro de transformación MT/BT',
        'Codigo Centro MTBT': 'Código Centro de transformación MT/BT',
        # Agregar más variaciones aquí
    }
}
```

##  Solución de Problemas

### Error: "cannot safely cast non-equivalent float64 to int64"

**Causa**: Valores NaN en columnas numéricas.

**Solución**: Ya manejado en el código con `.round().astype('Int64')`

### Error: "Arithmetic overflow error converting float to data type numeric"

**Causa**: Valores que exceden la precisión del DECIMAL en SQL.

**Solución**: Ejecutar `sql/fix_columns.sql` para aumentar precisión de columnas.

### Error: "String or binary data would be truncated"

**Causa**: Textos más largos que el límite de VARCHAR.

**Solución**: Aumentar tamaño de columnas en SQL:

```sql
ALTER TABLE [Centro MTBT]
ALTER COLUMN [Equipo aguas arriba] VARCHAR(500) NULL;
```

### Error: "Invalid column name"

**Causa**: La columna no existe en la tabla SQL.

**Solución**: Verificar nombres exactos con:

```sql
SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'Centro MTBT';
```

## 📈 Mejores Prácticas

### Antes de Ejecutar

1. ✅ **Backup**: Respalda la base de datos antes de cargas grandes
2. ✅ **Validación**: Revisa los archivos Excel para datos anómalos
3. ✅ **Prueba**: Ejecuta primero en un ambiente de desarrollo

### Durante la Ejecución

1. 📊 **Monitorea los logs** en tiempo real
2. ⚠️ **Atiende las advertencias** sobre truncamiento
3. 🔍 **Verifica** los conteos de filas procesadas

### Después de Ejecutar

1. ✔️ **Revisa el resumen** al final del log
2. 🔎 **Consulta las tablas** para validar los datos
3. 📝 **Documenta** cualquier problema encontrado

## 🔐 Seguridad

- ⚠️ **NUNCA** hagas commits del archivo `.env` al repositorio
- 🔒 **Usa autenticación de Windows** en desarrollo
- 🛡️ **Limita permisos** de la cuenta SQL a solo las tablas necesarias
- 📋 **Audita** los logs regularmente para detectar anomalías



**Versión**: 1.0.0  
**Última Actualización**: Octubre 2025



