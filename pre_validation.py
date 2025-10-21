import pandas as pd
import numpy as np
from pathlib import Path

def validate_excel_for_sql(excel_path, sheet_name):
    """
    Valida un archivo Excel antes de insertarlo en MSSQL
    Identifica problemas potenciales
    """
    print(f"\n{'='*70}")
    print(f"VALIDANDO: {sheet_name}")
    print(f"{'='*70}")
    
    # Leer Excel
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    
    # 1. INFORMACIÓN GENERAL
    print(f"\n📊 INFORMACIÓN GENERAL:")
    print(f"   • Total de filas: {len(df)}")
    print(f"   • Total de columnas: {len(df.columns)}")
    print(f"   • Filas completamente vacías: {df.dropna(how='all').shape[0] - len(df)}")
    
    # 2. ANÁLISIS DE COLUMNAS
    print(f"\n📋 ANÁLISIS DE NOMBRES DE COLUMNAS:")
    problematic_cols = []
    
    for col in df.columns:
        issues = []
        
        # Verificar caracteres problemáticos
        if any(char in str(col) for char in ['á', 'é', 'í', 'ó', 'ú', 'ñ', 'Á', 'É', 'Í', 'Ó', 'Ú', 'Ñ']):
            issues.append("acentos")
        
        if '/' in str(col):
            issues.append("slash")
        
        if ' ' in str(col):
            issues.append("espacios")
        
        if any(char in str(col) for char in ['(', ')', '[', ']', '{', '}', '@', '#', '$', '%']):
            issues.append("caracteres especiales")
        
        if len(str(col)) > 128:
            issues.append("nombre muy largo")
        
        if issues:
            print(f"   ⚠️  '{col}' -> {', '.join(issues)}")
            problematic_cols.append(col)
    
    if not problematic_cols:
        print("   ✓ Todos los nombres de columnas son seguros")
    
    # 3. ANÁLISIS DE DATOS POR COLUMNA
    print(f"\n🔍 ANÁLISIS DE CALIDAD DE DATOS:")
    
    for col in df.columns:
        null_count = df[col].isnull().sum()
        null_pct = (null_count / len(df)) * 100
        
        # Solo mostrar columnas con problemas
        if null_pct > 50:
            print(f"   ⚠️  '{col}': {null_pct:.1f}% valores nulos")
        
        # Detectar valores problemáticos comunes
        if df[col].dtype == 'object':
            problem_values = df[col].astype(str).isin(['nan', 'NaN', 'NA', 'N/A', '#N/A', '-', '/', '']).sum()
            if problem_values > 0:
                print(f"   ⚠️  '{col}': {problem_values} valores texto problemáticos (NA, -, /, etc)")
        
        # Verificar longitud de strings
        if df[col].dtype == 'object':
            max_length = df[col].astype(str).str.len().max()
            if max_length > 255:
                print(f"   ⚠️  '{col}': valor más largo = {max_length} caracteres (revisar límite SQL)")
    
    # 4. ANÁLISIS DE COLUMNAS ESPECÍFICAS SEGÚN HOJA
    print(f"\n🎯 VALIDACIONES ESPECÍFICAS:")
    
    if sheet_name == 'Centro MTBT':
        validate_centro_mtbt(df)
    elif sheet_name == 'Equipos de maniobras':
        validate_equipos_maniobras(df)
    elif sheet_name == 'Interrupciones':
        validate_interrupciones(df)
    
    # 5. VERIFICAR DUPLICADOS
    print(f"\n🔄 VERIFICACIÓN DE DUPLICADOS:")
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        print(f"   ⚠️  {duplicates} filas completamente duplicadas")
    else:
        print(f"   ✓ No hay filas duplicadas")
    
    # 6. RESUMEN
    print(f"\n{'='*70}")
    if problematic_cols:
        print(f"⚠️  ACCIÓN REQUERIDA: {len(problematic_cols)} columnas necesitan normalización")
        print(f"   Usa el script optimizado para normalizar automáticamente")
    else:
        print(f"✓ La hoja '{sheet_name}' está lista para inserción")
    print(f"{'='*70}")
    
    return df

def validate_centro_mtbt(df):
    """Validaciones específicas para Centro MTBT"""
    
    # Verificar columnas clave
    key_cols = ['Código Centro MT/BT', 'KVA instalado por transformador', 
                'UTM Centro MT/BT Norte', 'UTM Centro MT/BT Oeste']
    
    for col in key_cols:
        if col in df.columns:
            if col == 'KVA instalado por transformador':
                non_numeric = pd.to_numeric(df[col], errors='coerce').isnull().sum()
                if non_numeric > 0:
                    print(f"   ⚠️  '{col}': {non_numeric} valores no numéricos")
                    # Mostrar ejemplos
                    examples = df[df[col].notna() & pd.to_numeric(df[col], errors='coerce').isna()][col].head(3).tolist()
                    if examples:
                        print(f"      Ejemplos: {examples}")
            
            elif 'UTM' in col:
                # Validar que sean enteros
                non_numeric = pd.to_numeric(df[col], errors='coerce').isnull().sum()
                if non_numeric > 0:
                    print(f"   ⚠️  '{col}': {non_numeric} valores no numéricos para coordenadas")

def validate_equipos_maniobras(df):
    """Validaciones específicas para Equipos de maniobras"""
    
    key_cols = ['Código de Equipo', 'Nivel de tensión', 'Corriente máxima']
    
    for col in key_cols:
        if col in df.columns:
            if col == 'Código de Equipo':
                # Verificar códigos vacíos
                empty = df[col].isnull().sum()
                if empty > 0:
                    print(f"   ⚠️  '{col}': {empty} códigos vacíos (PK no puede ser NULL)")
            
            elif col in ['Nivel de tensión', 'Corriente máxima']:
                non_numeric = pd.to_numeric(df[col], errors='coerce').isnull().sum()
                if non_numeric > 0:
                    print(f"   ⚠️  '{col}': {non_numeric} valores no numéricos")

def validate_interrupciones(df):
    """Validaciones específicas para Interrupciones"""
    
    date_cols = ['Fecha y Hora_Inicio', 'Fecha y Hora_Cierre', 'Fecha Notificacion al Usuario']
    
    for col in date_cols:
        if col in df.columns:
            # Intentar convertir a fecha
            invalid_dates = pd.to_datetime(df[col], errors='coerce').isnull().sum()
            total_non_null = df[col].notna().sum()
            
            if invalid_dates > 0 and total_non_null > 0:
                print(f"   ⚠️  '{col}': {invalid_dates} fechas inválidas de {total_non_null} no-nulas")
                
                # Mostrar ejemplos de fechas problemáticas
                problematic = df[df[col].notna() & pd.to_datetime(df[col], errors='coerce').isna()][col].head(3).tolist()
                if problematic:
                    print(f"      Ejemplos: {problematic}")
    
    # Verificar lógica de fechas
    if 'Fecha y Hora_Inicio' in df.columns and 'Fecha y Hora_Cierre' in df.columns:
        inicio = pd.to_datetime(df['Fecha y Hora_Inicio'], errors='coerce')
        cierre = pd.to_datetime(df['Fecha y Hora_Cierre'], errors='coerce')
        
        # Verificar que cierre > inicio
        logic_errors = ((cierre < inicio) & inicio.notna() & cierre.notna()).sum()
        if logic_errors > 0:
            print(f"   ⚠️  {logic_errors} registros donde Fecha_Cierre < Fecha_Inicio (lógica incorrecta)")
    
    # Verificar columna de código de equipo múltiple
    if 'Código de Equipo' in df.columns:
        multi_codes = df['Código de Equipo'].astype(str).str.contains(',', na=False).sum()
        if multi_codes > 0:
            print(f"   ℹ️  {multi_codes} registros con múltiples códigos de equipo (separados por coma)")
            print(f"      La columna 'Primer Código de Equipo' será creada automáticamente")

# =============================================================================
# EJECUTAR VALIDACIÓN
# =============================================================================

if __name__ == "__main__":
    # Configurar ruta del archivo
    excel_file = 'Plantilla de Datos Regulatorios Para Sistemas Aislados_RECO_AGOSTO.xlsx'
    
    print("="*70)
    print("VALIDACIÓN DE DATOS ANTES DE INSERCIÓN EN MSSQL")
    print("="*70)
    
    # Validar cada hoja
    sheets_to_validate = ['Centro MTBT', 'Equipos de maniobras', 'Interrupciones']
    
    for sheet in sheets_to_validate:
        try:
            df = validate_excel_for_sql(excel_file, sheet)
        except Exception as e:
            print(f"\n❌ ERROR validando '{sheet}': {str(e)}")
    
    print("\n" + "="*70)
    print("VALIDACIÓN COMPLETADA")
    print("="*70)
    print("\n📝 RECOMENDACIONES:")
    print("   1. Corregir todos los warnings (⚠️) antes de insertar")
    print("   2. Usar el script optimizado para normalizar nombres de columnas")
    print("   3. Revisar que las tablas SQL tengan los tipos de datos correctos")
    print("   4. Considerar agregar constraints (NOT NULL, CHECK) en SQL")
    print("="*70)