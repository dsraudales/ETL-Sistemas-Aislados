# 🖥️ Guía de Conexión a SQL Server Local

## Configuraciones Comunes para `.env`

### ✅ OPCIÓN 1: SQL Server Express (Local) con Autenticación de Windows

**Recomendado para desarrollo local - No requiere usuario/contraseña**

```env
SQL_SERVER=localhost\SQLEXPRESS
SQL_DATABASE=tu_base_de_datos
SQL_USE_WINDOWS_AUTH=true
SQL_DRIVER=ODBC Driver 17 for SQL Server
EXCEL_FOLDER=C:/ruta/a/tu/carpeta
```

**Ventajas:**
- ✅ No necesitas gestionar contraseñas
- ✅ Usa tu cuenta de Windows actual
- ✅ Más seguro para desarrollo local

---

### ✅ OPCIÓN 2: SQL Server (Local) con Autenticación SQL

**Para cuando tienes un usuario SQL específico**

```env
SQL_SERVER=localhost
SQL_DATABASE=tu_base_de_datos
SQL_USERNAME=sa
SQL_PASSWORD=tu_contraseña_segura
SQL_DRIVER=ODBC Driver 17 for SQL Server
EXCEL_FOLDER=C:/ruta/a/tu/carpeta
```

**Variaciones del servidor:**
```env
# Instancia por defecto
SQL_SERVER=localhost

# Instancia nombrada (ej: SQLEXPRESS)
SQL_SERVER=localhost\SQLEXPRESS

# Con puerto específico
SQL_SERVER=localhost,1433

# Usando IP local
SQL_SERVER=127.0.0.1
SQL_SERVER=127.0.0.1\SQLEXPRESS
SQL_SERVER=127.0.0.1,1433
```

---

## 🔍 ¿Cómo Identificar tu Instancia de SQL Server?

### Método 1: SQL Server Management Studio (SSMS)
1. Abre SSMS
2. En "Connect to Server", mira el nombre del servidor que usas
3. Ejemplos comunes:
   - `LAPTOP-ABC123\SQLEXPRESS`
   - `localhost\SQLEXPRESS`
   - `(local)`
   - `.` (punto = localhost)

### Método 2: SQL Server Configuration Manager
1. Abre "SQL Server Configuration Manager"
2. Ve a "SQL Server Services"
3. Busca "SQL Server (NOMBRE_INSTANCIA)"
4. El nombre de la instancia está entre paréntesis

### Método 3: PowerShell
```powershell
# Listar instancias SQL Server locales
Get-Service -DisplayName "SQL Server*"
```

### Método 4: Registro de Windows
```powershell
# Ver instancias instaladas
Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Microsoft SQL Server' -Name InstalledInstances
```

---

## 🔧 Ejemplos de Configuración Completos

### Ejemplo 1: SQL Express Local (Windows Auth)
```env
# Desarrollo local - Configuración más simple
SQL_SERVER=localhost\SQLEXPRESS
SQL_DATABASE=DatosRegulatorios
SQL_USE_WINDOWS_AUTH=true
SQL_DRIVER=ODBC Driver 17 for SQL Server
EXCEL_FOLDER=C:/Users/David Raudales/Documents/Excel
```

### Ejemplo 2: SQL Server Local (SQL Auth)
```env
# Con usuario SQL específico
SQL_SERVER=localhost
SQL_DATABASE=DatosRegulatorios
SQL_USERNAME=etl_user
SQL_PASSWORD=MiPassword123!
SQL_DRIVER=ODBC Driver 17 for SQL Server
EXCEL_FOLDER=C:/Users/David Raudales/Documents/Excel
```

### Ejemplo 3: SQL Server en Puerto Personalizado
```env
# SQL Server escuchando en puerto no estándar
SQL_SERVER=localhost,1435
SQL_DATABASE=DatosRegulatorios
SQL_USERNAME=admin
SQL_PASSWORD=Password456!
SQL_DRIVER=ODBC Driver 17 for SQL Server
EXCEL_FOLDER=C:/Users/David Raudales/Documents/Excel
```

---

## 🐛 Troubleshooting - Errores Comunes

### ❌ Error: "Named Pipes Provider: Could not open a connection"

**Causa:** SQL Server no está ejecutándose o no acepta conexiones.

**Solución:**
1. Verifica que SQL Server esté corriendo:
   ```powershell
   Get-Service -Name MSSQL*
   ```

2. Si está detenido, inícialo:
   ```powershell
   Start-Service -Name "MSSQL`$SQLEXPRESS"
   ```

3. Habilita conexiones TCP/IP en SQL Server Configuration Manager

---

### ❌ Error: "Login failed for user"

**Causa:** Credenciales incorrectas o modo de autenticación no habilitado.

**Solución Windows Auth:**
- Asegúrate de que tu usuario de Windows tiene permisos en SQL Server
- Verifica que `SQL_USE_WINDOWS_AUTH=true` esté en `.env`

**Solución SQL Auth:**
- Verifica usuario y contraseña en `.env`
- Asegúrate de que SQL Server tenga "Mixed Mode Authentication" habilitado
- Verifica que el usuario SQL existe y tiene permisos

---

### ❌ Error: "Cannot open database"

**Causa:** La base de datos no existe o no tienes acceso.

**Solución:**
1. Verifica que la base de datos existe:
   ```sql
   SELECT name FROM sys.databases;
   ```

2. Crea la base de datos si no existe:
   ```sql
   CREATE DATABASE DatosRegulatorios;
   ```

3. Verifica permisos del usuario en la base de datos

---

### ❌ Error: "Driver not found"

**Causa:** El driver ODBC no está instalado.

**Solución:**
1. Verifica drivers instalados:
   ```powershell
   Get-OdbcDriver -Name "ODBC Driver*SQL Server"
   ```

2. Descarga e instala el driver:
   - [ODBC Driver 17 for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
   - [ODBC Driver 18 for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

3. Si tienes otro driver, actualiza en `.env`:
   ```env
   SQL_DRIVER=ODBC Driver 18 for SQL Server
   ```

---

## 🧪 Probar Conexión

### Test rápido desde PowerShell:
```powershell
# Probar conexión Windows Auth
sqlcmd -S localhost\SQLEXPRESS -E -Q "SELECT @@VERSION"

# Probar conexión SQL Auth
sqlcmd -S localhost\SQLEXPRESS -U tu_usuario -P tu_password -Q "SELECT @@VERSION"
```

### Test desde Python:
```python
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

server = os.getenv('SQL_SERVER')
database = os.getenv('SQL_DATABASE')
driver = os.getenv('SQL_DRIVER')

# Windows Auth
conn_str = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes'

# SQL Auth
# username = os.getenv('SQL_USERNAME')
# password = os.getenv('SQL_PASSWORD')
# conn_str = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

try:
    conn = pyodbc.connect(conn_str)
    print("✓ Conexión exitosa!")
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION")
    print(cursor.fetchone()[0])
    conn.close()
except Exception as e:
    print(f"✗ Error: {e}")
```

---

## 📋 Checklist de Configuración Local

- [ ] SQL Server está instalado
- [ ] SQL Server está corriendo (`Get-Service MSSQL*`)
- [ ] Tengo el nombre correcto de la instancia
- [ ] La base de datos existe
- [ ] He configurado `.env` con los valores correctos
- [ ] Driver ODBC está instalado
- [ ] Mi usuario tiene permisos en la base de datos
- [ ] He probado la conexión con `sqlcmd` o script Python
- [ ] `python-dotenv` está instalado (`pip install python-dotenv`)

---

## 💡 Recomendaciones

### Para Desarrollo Local:
✅ **Usa Windows Authentication** (`SQL_USE_WINDOWS_AUTH=true`)
- Más simple y seguro
- No necesitas gestionar contraseñas
- Funciona automáticamente con tu cuenta

### Para Producción/Remoto:
✅ **Usa SQL Authentication con credenciales dedicadas**
- Crea un usuario específico para el ETL
- Dale solo los permisos necesarios
- Usa contraseñas fuertes
- Considera usar Azure Key Vault o similar para secretos

---

**✅ Configuración actualizada con soporte para SQL Server local**

El script ahora detecta automáticamente si usas Windows Auth o SQL Auth basándose en la variable `SQL_USE_WINDOWS_AUTH`.
