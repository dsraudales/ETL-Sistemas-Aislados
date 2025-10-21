# 📁 Guía de Rutas de Carpetas en .env

## ✅ Formatos CORRECTOS para Rutas con Espacios

### **Opción 1: Forward Slashes /** (RECOMENDADO)
```env
EXCEL_FOLDER=C:/Users/David Raudales/Documents/Datos Regulatorios Sistemas Aislados
EXCEL_FOLDER=C:/Users/David Raudales/Documents/Datos Regulatorios Sistemas Aislados/Archivos
```
- ✅ Funciona perfectamente en Windows
- ✅ No necesita escapes
- ✅ Más fácil de leer
- ✅ Compatible con Linux/Mac si migras

### **Opción 2: Backslashes Dobles \\\\**
```env
EXCEL_FOLDER=C:\\Users\\David Raudales\\Documents\\Datos Regulatorios Sistemas Aislados
EXCEL_FOLDER=C:\\Users\\David Raudales\\Documents\\Datos Regulatorios Sistemas Aislados\\Archivos
```
- ✅ Funciona en Windows
- ⚠️ Más difícil de escribir (doble backslash)

### **Opción 3: Con Comillas** (solo si tu parser lo requiere)
```env
EXCEL_FOLDER="C:/Users/David Raudales/Documents/Datos Regulatorios Sistemas Aislados"
```
- ✅ Funciona con algunos parsers
- ⚠️ `python-dotenv` no las necesita, pero las acepta

---

## ❌ Formatos INCORRECTOS

### ❌ NO usar sintaxis de Python
```env
# ❌ INCORRECTO - No uses r'...' en .env
EXCEL_FOLDER=r'C:\Users\David Raudales\Documents\...'

# ❌ INCORRECTO - No uses comillas simples Python
EXCEL_FOLDER='C:/Users/David Raudales/Documents/...'
```

### ❌ NO usar backslash simple
```env
# ❌ INCORRECTO - Backslash simple causa problemas
EXCEL_FOLDER=C:\Users\David Raudales\Documents\...
```
El `\D` se interpreta como secuencia de escape.

---

## 🎯 Tu Caso Específico

### Para la Carpeta del Proyecto
```env
EXCEL_FOLDER=C:/Users/David Raudales/Documents/Datos Regulatorios Sistemas Aislados
```

### Para la Subcarpeta "Archivos"
```env
EXCEL_FOLDER=C:/Users/David Raudales/Documents/Datos Regulatorios Sistemas Aislados/Archivos
```

### Para Subcarpetas con Más Espacios
```env
# Ejemplo con múltiples espacios
EXCEL_FOLDER=C:/Users/David Raudales/Documents/Mis Documentos de Trabajo/Excel Files 2024
```

---

## 🧪 Verificar que la Ruta es Correcta

### Desde PowerShell:
```powershell
# Ver contenido de la carpeta
Get-ChildItem "C:\Users\David Raudales\Documents\Datos Regulatorios Sistemas Aislados\Archivos"

# O con forward slashes (también funciona)
Get-ChildItem "C:/Users/David Raudales/Documents/Datos Regulatorios Sistemas Aislados/Archivos"

# Ver solo archivos Excel
Get-ChildItem "C:/Users/David Raudales/Documents/Datos Regulatorios Sistemas Aislados/Archivos" -Filter *.xlsx
```

### Desde Python (para probar):
```python
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Leer la variable
excel_folder = os.getenv('EXCEL_FOLDER')
print(f"Ruta configurada: {excel_folder}")

# Verificar que existe
ruta = Path(excel_folder)
if ruta.exists():
    print(f"✓ La carpeta existe")
    print(f"✓ Es una carpeta: {ruta.is_dir()}")
    
    # Listar archivos Excel
    archivos_excel = list(ruta.glob("*.xlsx")) + list(ruta.glob("*.xls"))
    print(f"✓ Archivos Excel encontrados: {len(archivos_excel)}")
    for archivo in archivos_excel:
        print(f"  - {archivo.name}")
else:
    print(f"✗ La carpeta NO existe")
```

---

## 📋 Ejemplo Completo de .env

```env
# =============================================================================
# VARIABLES DE ENTORNO - .env
# =============================================================================
# IMPORTANTE: NO SUBIR ESTE ARCHIVO A CONTROL DE VERSIONES

# =============================================================================
# CONFIGURACIÓN DE CONEXIÓN A SQL SERVER
# =============================================================================

SQL_SERVER=localhost\MSSQLSERVER01
SQL_DATABASE=datos_regulatorios_reco
SQL_USE_WINDOWS_AUTH=true
SQL_DRIVER=ODBC Driver 17 for SQL Server

# Nota: SQL_USERNAME y SQL_PASSWORD no son necesarios con Windows Auth
# Si necesitas SQL Authentication, descomenta y configura:
# SQL_USERNAME=your_username
# SQL_PASSWORD=your_password

# =============================================================================
# CONFIGURACIÓN DE RUTAS - Usa forward slashes (/)
# =============================================================================

# Carpeta donde están los archivos Excel
EXCEL_FOLDER=C:/Users/David Raudales/Documents/Datos Regulatorios Sistemas Aislados/Archivos

# Si tienes múltiples carpetas, puedes agregar más variables:
# BACKUP_FOLDER=C:/Users/David Raudales/Documents/Backups Excel
# OUTPUT_FOLDER=C:/Users/David Raudales/Documents/Resultados ETL
```

---

## 🔍 Rutas Relativas vs Absolutas

### Rutas Absolutas (Recomendado para producción)
```env
# Especifica la ruta completa
EXCEL_FOLDER=C:/Users/David Raudales/Documents/Datos Regulatorios Sistemas Aislados/Archivos
```
- ✅ Siempre funciona sin importar desde dónde ejecutes el script
- ✅ Más claro y explícito

### Rutas Relativas (Para desarrollo)
```env
# Relativa al directorio del script
EXCEL_FOLDER=./Archivos
EXCEL_FOLDER=../Archivos
```
- ⚠️ Depende del directorio actual
- ⚠️ Puede causar problemas si ejecutas desde otra ubicación

---

## 🐛 Troubleshooting

### Error: "No se encontraron archivos Excel"

**Verifica:**
1. **La ruta está correctamente escrita** (sin typos)
2. **Usas forward slashes** o backslashes dobles
3. **La carpeta existe** (cópiala y pégala en el explorador)
4. **Hay archivos Excel** (.xlsx o .xls) en la carpeta
5. **Tienes permisos** de lectura en la carpeta

**Comando para verificar:**
```powershell
# Verificar que la carpeta existe
Test-Path "C:/Users/David Raudales/Documents/Datos Regulatorios Sistemas Aislados/Archivos"

# Ver archivos Excel
Get-ChildItem "C:/Users/David Raudales/Documents/Datos Regulatorios Sistemas Aislados/Archivos" -Filter *.xlsx
```

### Error: "Invalid escape sequence"

**Causa:** Usaste backslash simple en vez de doble.

**Solución:**
```env
# ❌ INCORRECTO
EXCEL_FOLDER=C:\Users\David Raudales\...

# ✅ CORRECTO - Opción 1
EXCEL_FOLDER=C:/Users/David Raudales/...

# ✅ CORRECTO - Opción 2
EXCEL_FOLDER=C:\\Users\\David Raudales\\...
```

---

## 💡 Tips Adicionales

### 1. **Estructura de Carpetas Recomendada**
```
C:/Users/David Raudales/Documents/
└── Datos Regulatorios Sistemas Aislados/
    ├── .env                    (configuración)
    ├── etl_sistemas_aislados.py
    ├── Archivos/               (Excel de entrada)
    │   ├── datos_enero.xlsx
    │   └── datos_febrero.xlsx
    ├── logs/                   (logs del ETL)
    └── backup/                 (respaldos opcionales)
```

### 2. **Variables Adicionales Útiles**
```env
# Múltiples carpetas para diferentes propósitos
INPUT_FOLDER=C:/Users/David Raudales/Documents/Datos Regulatorios Sistemas Aislados/Archivos
OUTPUT_FOLDER=C:/Users/David Raudales/Documents/Datos Regulatorios Sistemas Aislados/Resultados
BACKUP_FOLDER=C:/Users/David Raudales/Documents/Datos Regulatorios Sistemas Aislados/Backup
LOG_FOLDER=C:/Users/David Raudales/Documents/Datos Regulatorios Sistemas Aislados/logs
```

### 3. **Copiar Ruta Fácilmente en Windows**
1. Mantén presionado `Shift`
2. Click derecho en la carpeta
3. Selecciona "Copiar como ruta de acceso"
4. Pega en `.env`
5. **Cambia los `\` por `/`**

---

## ✅ Tu Configuración Recomendada

```env
# =============================================================================
# VARIABLES DE ENTORNO - .env
# =============================================================================

# SQL Server Local
SQL_SERVER=localhost\MSSQLSERVER01
SQL_DATABASE=datos_regulatorios_reco
SQL_USE_WINDOWS_AUTH=true
SQL_DRIVER=ODBC Driver 17 for SQL Server

# Carpeta de Archivos Excel (con forward slashes)
EXCEL_FOLDER=C:/Users/David Raudales/Documents/Datos Regulatorios Sistemas Aislados/Archivos
```

**¡Listo para usar!** 🚀
