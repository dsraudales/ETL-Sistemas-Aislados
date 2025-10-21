import pandas as pd
import pyodbc
from sqlalchemy import create_engine
import urllib
import os
from pathlib import Path
import logging
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# =============================================================================
# CONFIGURACIÓN Y LOGGING
# =============================================================================

# Configurar logging
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_file = log_dir / f"etl_{timestamp}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# =============================================================================
# CONFIGURACIÓN DE CONEXIÓN A SQL SERVER (desde variables de entorno)
# =============================================================================
server = os.getenv('SQL_SERVER')
database = os.getenv('SQL_DATABASE')
username = os.getenv('SQL_USERNAME')
password = os.getenv('SQL_PASSWORD')
driver = os.getenv('SQL_DRIVER', 'ODBC Driver 17 for SQL Server')
use_windows_auth = os.getenv('SQL_USE_WINDOWS_AUTH', 'false').lower() == 'true'
#Use Windows Auth solamente en la fase de testing, cambiar al modo credenciales al finalizar pruebas



# Validar que las variables esenciales estén configuradas
if not server or not database:
    raise ValueError(
        "Error: Faltan variables de entorno para la conexión SQL.\n"
        "Variables requeridas:\n"
        "  - SQL_SERVER (ej: localhost, localhost\\SQLEXPRESS, 127.0.0.1,1433)\n"
        "  - SQL_DATABASE\n"
        "\n"
        "Para autenticación SQL Server (por defecto):\n"
        "  - SQL_USERNAME\n"
        "  - SQL_PASSWORD\n"
        "\n"
        "Para autenticación de Windows:\n"
        "  - SQL_USE_WINDOWS_AUTH=true\n"
        "\n"
        "Puedes usar .env.example como plantilla."
    )

# Construir connection string según el tipo de autenticación
if use_windows_auth:
    # Windows Authentication (Trusted Connection)
    connection_string = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes'
    logger.info("✓ Usando autenticación de Windows (Trusted Connection)")
else:
    # SQL Server Authentication
    if not username or not password:
        raise ValueError(
            "Error: Para autenticación SQL Server se requieren SQL_USERNAME y SQL_PASSWORD.\n"
            "O configura SQL_USE_WINDOWS_AUTH=true para usar autenticación de Windows."
        )
    connection_string = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    logger.info("✓ Usando autenticación SQL Server")

params = urllib.parse.quote_plus(connection_string)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

logger.info("✓ Configuración SQL cargada desde variables de entorno")
logger.info(f"  - Servidor: {server}")
logger.info(f"  - Base de datos: {database}")
if not use_windows_auth:
    logger.info(f"  - Usuario: {username}")

# =============================================================================
# CONFIGURACIÓN DEL ARCHIVO EXCEL (desde variables de entorno)
# =============================================================================
carpeta_excel = os.getenv('EXCEL_FOLDER', 'C:\\Users\\David Raudales\\Documents\\Datos Regulatorios Sistemas Aislados')

if carpeta_excel == 'C:\\Users\\David Raudales\\Documents\\Datos Regulatorios Sistemas Aislados':
    logger.warning("⚠️  Usando ruta de Excel por defecto. Configura EXCEL_FOLDER en .env")

# =============================================================================
# MAPEO CRÍTICO: Excel → SQL Server (NOMBRES EXACTOS)
# =============================================================================

# IMPORTANTE: Los nombres de columnas en SQL tienen acentos, espacios y caracteres especiales
# Debemos mapear exactamente como están en SQL Server

COLUMN_MAPPINGS = {
    'Centro MTBT': {
        # Excel puede tener variaciones → SQL Server nombre exacto
        'Código Centro MT/BT': 'Código Centro de transformación MT/BT',
        'Codigo Centro MT/BT': 'Código Centro de transformación MT/BT',
        'Código Centro de transformación MT/BT': 'Código Centro de transformación MT/BT',
        'KVA instalado por transformador': 'KVA instalado por transformador',
        'Equipo aguas arriba': 'Equipo aguas arriba',
        'Propietario': 'Propietario',
        'UTM Centro MT/BT Norte': 'UTM Centro MT/BT Norte',
        'UTM Centro MT/BT Oeste': 'UTM Centro MT/BT Oeste',
    },
    'Equipos de maniobras': {
        # Manejar variaciones de capitalización
        'Código de Equipo': 'Código de equipo',  # Nota: SQL tiene minúscula
        'Código de equipo': 'Código de equipo',
        'Codigo de Equipo': 'Código de equipo',
        'Codigo de equipo': 'Código de equipo',
        'Tipo de Equipo': 'Tipo de equipo',
        'Tipo de equipo': 'Tipo de equipo',
        'Código de subestación': 'Código de subestación',
        'Codigo de Equipo Aguas Arriba': 'Codigo de Equipo Aguas Arriba',
        'Nivel de tensión': 'Nivel de tensión',
        'Nivel de tension': 'Nivel de tensión',
        'Corriente máxima': 'Corriente máxima',
        'Corriente maxima': 'Corriente máxima',
        'UTM Equipo Norte': 'UTM Equipo Norte',
        'UTM Equipo Oeste': 'UTM Equipo Oeste',
    },
    'Interrupciones': {
        'ID_Interrupcion': 'ID_Interrupcion',
        'ID Interrupcion': 'ID_Interrupcion',
        'Fecha y Hora_Inicio': 'Fecha y Hora_Inicio',
        'Fecha y Hora Inicio': 'Fecha y Hora_Inicio',
        'Fecha y Hora_Cierre': 'Fecha y Hora_Cierre',
        'Fecha y Hora Cierre': 'Fecha y Hora_Cierre',
        'Causa': 'Causa',
        'Fecha Notificacion al Usuario': 'Fecha Notificacion al Usuario',
        'Fecha Notificación al Usuario': 'Fecha Notificacion al Usuario',
        'Origen del evento': 'Origen del evento',
        'Código de Equipo': 'Código de Equipo',
        'Codigo de Equipo': 'Código de Equipo',
        'Enlace Medio de Notificacion a los Usuarios': 'Enlace Medio de Notificacion a los Usuarios',
        'Observaciones': 'Observaciones',
    }
}

# Nombres de tablas SQL exactos (con espacios)
TABLE_NAMES = {
    'Centro MTBT': 'Centro MTBT',
    'Equipos de maniobras': 'Equipos de maniobras',
    'Interrupciones': 'Interrupciones'
}

# =============================================================================
# FUNCIÓN PARA OBTENER ARCHIVOS EXCEL
# =============================================================================
def obtener_archivos_excel(carpeta):
    """Obtiene todos los archivos Excel (.xlsx, .xls) de una carpeta"""
    ruta = Path(carpeta)
    archivos_excel = []
    
    for extension in ['*.xlsx', '*.xls']:
        archivos_excel.extend(ruta.glob(extension))
    
    return sorted(archivos_excel)

# =============================================================================
# FUNCIÓN PARA MAPEAR COLUMNAS
# =============================================================================
def mapear_columnas(df, tabla):
    """Mapea columnas de Excel a nombres exactos de SQL Server"""
    mapeo = COLUMN_MAPPINGS.get(tabla, {})
    
    # Crear diccionario de mapeo solo para columnas que existen en el DataFrame
    columnas_a_renombrar = {}
    columnas_no_mapeadas = []
    
    for col_excel in df.columns:
        if col_excel in mapeo:
            columnas_a_renombrar[col_excel] = mapeo[col_excel]
            logger.info(f"   Mapeo: '{col_excel}' → '{mapeo[col_excel]}'")
        else:
            # Columna no está en el mapeo - mantener nombre original
            columnas_no_mapeadas.append(col_excel)
            logger.warning(f"   ⚠️  Columna '{col_excel}' no está en mapeo - manteniendo nombre original")
    
    # Renombrar columnas
    df = df.rename(columns=columnas_a_renombrar)
    
    return df

# =============================================================================
# FUNCIÓN PARA LIMPIAR Y PREPARAR DATOS
# =============================================================================
def limpiar_dataframe(df, nombre_tabla):
    """Limpia y prepara el DataFrame según la tabla destino"""
    df = df.dropna(axis=1, how='all')
    df = df.dropna(axis=0, how='all')
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()  # Remove leading/trailing spaces
        df[col] = df[col].str.replace(r'\s+', ' ', regex=True)  # Replace multiple spaces with single space
        df[col] = df[col].replace('nan', None)  # Convert 'nan' strings back to None
    
    df = mapear_columnas(df, nombre_tabla)
    
    if nombre_tabla == 'Centro MTBT':
        if 'KVA instalado por transformador' in df.columns:
            df['KVA instalado por transformador'] = pd.to_numeric(
                df['KVA instalado por transformador'], errors='coerce'
            )
            valores_grandes = df['KVA instalado por transformador'] > 99.9999
            if valores_grandes.any():
                logger.warning(
                    f"   ⚠️  {valores_grandes.sum()} valores de KVA > 99.9999 serán truncados"
                )
        
        #  FIXED: Proper Int64 conversion
        if 'UTM Centro MT/BT Norte' in df.columns:
            df['UTM Centro MT/BT Norte'] = pd.to_numeric(
                df['UTM Centro MT/BT Norte'], errors='coerce'
            ).round().astype('Int64')  # Round first, then convert
            
        if 'UTM Centro MT/BT Oeste' in df.columns:
            df['UTM Centro MT/BT Oeste'] = pd.to_numeric(
                df['UTM Centro MT/BT Oeste'], errors='coerce'
            ).round().astype('Int64')
    
    elif nombre_tabla == 'Equipos de maniobras':
        if 'Nivel de tensión' in df.columns:
            df['Nivel de tensión'] = pd.to_numeric(
                df['Nivel de tensión'], errors='coerce'
            )
            valores_grandes = df['Nivel de tensión'] > 9.99
            if valores_grandes.any():
                logger.warning(
                    f"   ⚠️  {valores_grandes.sum()} valores > 9.99 kV serán truncados"
                )
        
        if 'Corriente máxima' in df.columns:
            df['Corriente máxima'] = pd.to_numeric(
                df['Corriente máxima'], errors='coerce'
            ).round().astype('Int64')  
        
        #  FIXED: UTM coordinates
        if 'UTM Equipo Norte' in df.columns:
            df['UTM Equipo Norte'] = pd.to_numeric(
                df['UTM Equipo Norte'], errors='coerce'
            ).round().astype('Int64')
            
        if 'UTM Equipo Oeste' in df.columns:
            df['UTM Equipo Oeste'] = pd.to_numeric(
                df['UTM Equipo Oeste'], errors='coerce'
            ).round().astype('Int64')
    
    elif nombre_tabla == 'Interrupciones':
        # Date conversions
        for col in ['Fecha y Hora_Inicio', 'Fecha y Hora_Cierre', 'Fecha Notificacion al Usuario']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        if 'Código de Equipo' in df.columns:
            df['CódigoDePrimerEquipo'] = df['Código de Equipo'].astype(str).apply(
                lambda x: x.split(',')[0].strip() if pd.notna(x) and x != 'nan' else None
            )
            logger.info("   ✓ Creada columna 'CódigoDePrimerEquipo'")
    
    if 'id' in df.columns:
        df = df.drop(columns=['id'])
        logger.info("   ✓ Removida columna 'id' (IDENTITY en SQL)")
    
    return df
# =============================================================================
# FUNCIÓN PRINCIPAL PARA CARGAR DATOS
# =============================================================================
def cargar_excel_a_sql(archivo_excel, tabla_sheet_map, engine, if_exists='append'):
    """
    Lee las hojas del Excel y las carga en las tablas SQL correspondientes
    """
    resultados = {}
    nombre_archivo = os.path.basename(archivo_excel)
    
    for hoja_excel, tabla_sql in tabla_sheet_map.items():
        try:
            logger.info(f"\n{'='*60}")
            logger.info(f"Archivo: {nombre_archivo}")
            logger.info(f"Procesando: {hoja_excel} → {tabla_sql}")
            logger.info(f"{'='*60}")
            
            # Leer la hoja de Excel
            df = pd.read_excel(archivo_excel, sheet_name=hoja_excel)
            logger.info(f"✓ Datos leídos: {len(df)} filas, {len(df.columns)} columnas")
            logger.info(f"   Columnas originales: {list(df.columns)}")
            
            # Limpiar y preparar datos
            df = limpiar_dataframe(df, hoja_excel)
            logger.info(f"✓ Datos limpiados: {len(df)} filas válidas")
            logger.info(f"   Columnas finales para SQL: {list(df.columns)}")
            
            # Mostrar primeras filas
            logger.info("\n   Primeras 3 filas:")
            for i, row in df.head(3).iterrows():
                logger.info(f"   {i}: {row.to_dict()}")
            
            # Verificar que no haya columnas que excedan límites de SQL
            for col in df.select_dtypes(include=['object']):
                max_len = df[col].astype(str).str.len().max()
                if max_len > 255:
                    logger.warning(
                        f"   ⚠️  Columna '{col}' tiene valores hasta {max_len} caracteres "
                        f"(límite SQL puede ser 255)"
                    )
            
            # Cargar a SQL Server
            rows_inserted = df.to_sql(
                name=tabla_sql,
                con=engine,
                if_exists=if_exists,
                index=False,
                chunksize=500
            )
            
            logger.info(f"✓ Datos cargados exitosamente a la tabla '{tabla_sql}'")
            resultados[f"{nombre_archivo} - {tabla_sql}"] = {
                'estado': 'éxito', 
                'filas': len(df)
            }
            
        except Exception as e:
            logger.error(f"✗ Error procesando {hoja_excel}: {str(e)}")
            resultados[f"{nombre_archivo} - {tabla_sql}"] = {
                'estado': 'error', 
                'mensaje': str(e)
            }
    
    return resultados

# =============================================================================
# EJECUTAR EL PROCESO
# =============================================================================
if __name__ == "__main__":
    logger.info("="*60)
    logger.info("INICIO DEL PROCESO DE CARGA MASIVA")
    logger.info("="*60)
    
    try:
        # Obtener todos los archivos Excel de la carpeta
        archivos = obtener_archivos_excel(carpeta_excel)
        
        if not archivos:
            logger.error(f"\n✗ No se encontraron archivos Excel en la carpeta: {carpeta_excel}")
            exit()
        
        logger.info(f"\n✓ Se encontraron {len(archivos)} archivo(s) Excel:")
        for idx, archivo in enumerate(archivos, 1):
            logger.info(f"  {idx}. {archivo.name}")
        
        # Procesar cada archivo
        todos_resultados = {}
        
        for archivo in archivos:
            logger.info(f"\n{'#'*60}")
            logger.info(f"PROCESANDO ARCHIVO: {archivo.name}")
            logger.info(f"{'#'*60}")
            
            # Ejecutar la carga para este archivo
            resultados = cargar_excel_a_sql(
                archivo_excel=str(archivo),
                tabla_sheet_map=TABLE_NAMES,
                engine=engine,
                if_exists='append'  # Cambiar a 'replace' para reemplazar datos existentes
            )
            
            todos_resultados.update(resultados)
        
        # Resumen final
        logger.info("\n" + "="*60)
        logger.info("RESUMEN GENERAL DEL PROCESO")
        logger.info("="*60)
        
        exitosos = 0
        errores = 0
        total_filas = 0
        
        for clave, resultado in todos_resultados.items():
            if resultado['estado'] == 'éxito':
                logger.info(f"✓ {clave}: {resultado['filas']} filas cargadas")
                exitosos += 1
                total_filas += resultado['filas']
            else:
                logger.error(f"✗ {clave}: ERROR - {resultado['mensaje']}")
                errores += 1
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Total de operaciones exitosas: {exitosos}")
        logger.info(f"Total de errores: {errores}")
        logger.info(f"Total de filas cargadas: {total_filas}")
        logger.info(f"{'='*60}")
        
        logger.info("\n¡Proceso completado!")
        logger.info(f"Log guardado en: {log_file}")
        
    except Exception as e:
        logger.error(f"\n✗ Error general en el proceso: {str(e)}")
    
    finally:
        engine.dispose()
        logger.info("\nConexión cerrada.")