# Migración de Credenciales SQL a Variables de Entorno

## ✅ Cambios Implementados

### 1. Archivos Creados

#### `.env` (Credenciales reales - **NO compartir**)
- Contiene las credenciales reales de SQL Server
- Variables: `SQL_SERVER`, `SQL_DATABASE`, `SQL_USERNAME`, `SQL_PASSWORD`, `SQL_DRIVER`
- También incluye: `EXCEL_FOLDER`
- ⚠️ **Este archivo está en .gitignore para proteger tus credenciales**

#### `.env.example` (Plantilla pública)
- Plantilla sin credenciales reales
- Puede compartirse en repositorios
- Sirve como guía para otros usuarios

#### `.gitignore`
- Protege archivos sensibles (`.env`, logs, etc.)
- Evita que las credenciales se suban a Git

### 2. Código Modificado

#### `etl_sistemas_aislados.py`

**Cambios realizados:**

1. **Importación de dotenv:**
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

2. **Lectura de variables de entorno:**
   ```python
   server = os.getenv('SQL_SERVER')
   database = os.getenv('SQL_DATABASE')
   username = os.getenv('SQL_USERNAME')
   password = os.getenv('SQL_PASSWORD')
   driver = os.getenv('SQL_DRIVER', 'ODBC Driver 17 for SQL Server')
   carpeta_excel = os.getenv('EXCEL_FOLDER', 'C:/ruta/a/tu/carpeta')
   ```

3. **Validación de configuración:**
   - El script valida que todas las variables necesarias estén definidas
   - Muestra un error claro si falta alguna variable
   - Registra la configuración cargada en los logs (sin mostrar la contraseña)

## 📋 Instrucciones de Uso

### Para ti (usuario actual):
El archivo `.env` ya tiene tus credenciales configuradas. Solo necesitas:

1. **Instalar python-dotenv** (si aún no lo has hecho):
   ```powershell
   pip install python-dotenv
   ```

2. **Verificar el archivo .env:**
   - Abre `.env` y confirma que las credenciales son correctas
   - Actualiza `EXCEL_FOLDER` con la ruta real de tus archivos Excel

3. **Ejecutar el ETL:**
   ```powershell
   python etl_sistemas_aislados.py
   ```

### Para otros usuarios:
1. Copiar `.env.example` a `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Editar `.env` con sus credenciales reales

3. Instalar dependencias y ejecutar

## 🔒 Seguridad

### ✅ Ventajas de este enfoque:
- ✅ Credenciales fuera del código
- ✅ Protección automática con `.gitignore`
- ✅ Fácil cambio de credenciales sin modificar código
- ✅ Diferentes entornos (desarrollo, producción) con diferentes `.env`
- ✅ Plantilla `.env.example` para documentación

### ⚠️ Importante:
- **NUNCA** compartas el archivo `.env`
- **NUNCA** subas `.env` a Git (ya está en `.gitignore`)
- **SÍ** comparte `.env.example` (no contiene credenciales reales)

## 🔄 Variables Disponibles

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `SQL_SERVER` | Servidor SQL Server | `tcp:192.168.2.5,53937` |
| `SQL_DATABASE` | Nombre de la base de datos | `tu_base_de_datos` |
| `SQL_USERNAME` | Usuario SQL | `mmejia` |
| `SQL_PASSWORD` | Contraseña SQL | `********` |
| `SQL_DRIVER` | Driver ODBC (opcional) | `ODBC Driver 17 for SQL Server` |
| `EXCEL_FOLDER` | Carpeta de archivos Excel | `C:/ruta/a/tu/carpeta` |

## 🐛 Troubleshooting

### Error: "Faltan variables de entorno"
**Causa:** El archivo `.env` no existe o está vacío.
**Solución:** Crear `.env` basándote en `.env.example`

### Error: "Import 'dotenv' could not be resolved"
**Causa:** Falta instalar `python-dotenv`.
**Solución:** 
```powershell
pip install python-dotenv
```

### Error de conexión SQL
**Causa:** Credenciales incorrectas en `.env`.
**Solución:** Verificar y corregir las variables en `.env`

## 📝 Próximos Pasos Recomendados

1. ✅ Verificar que `python-dotenv` esté instalado
2. ✅ Probar la conexión ejecutando el ETL
3. ✅ Actualizar `EXCEL_FOLDER` en `.env` con la ruta correcta
4. ⚠️ Cambiar contraseñas débiles por contraseñas más seguras
5. 📚 Compartir `.env.example` con tu equipo (no `.env`)

## 💡 Tips Adicionales

### Múltiples entornos:
Puedes crear archivos `.env.dev`, `.env.prod`, etc. y cargarlos según el entorno:
```python
from dotenv import load_dotenv
load_dotenv('.env.prod')  # Cargar entorno específico
```

### Valores por defecto:
El código ya incluye valores por defecto seguros:
```python
driver = os.getenv('SQL_DRIVER', 'ODBC Driver 17 for SQL Server')
carpeta_excel = os.getenv('EXCEL_FOLDER', 'C:/ruta/a/tu/carpeta')
```

---

**✅ Implementación completada exitosamente**
