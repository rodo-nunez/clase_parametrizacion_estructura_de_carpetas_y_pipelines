#!/usr/bin/env python3
"""
Script 2: Limpieza de Datos
Limpia datos crudos: maneja nulos, outliers y validaciones
"""

import argparse
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

def detectar_outliers_iqr(df, columna, factor=1.5):
    """
    Detecta outliers usando el método IQR.
    
    Args:
        df: DataFrame
        columna: Nombre de la columna
        factor: Factor multiplicador del IQR (default 1.5)
    
    Returns:
        Serie booleana indicando outliers
    """
    Q1 = df[columna].quantile(0.25)
    Q3 = df[columna].quantile(0.75)
    IQR = Q3 - Q1
    
    limite_inferior = Q1 - factor * IQR
    limite_superior = Q3 + factor * IQR
    
    return (df[columna] < limite_inferior) | (df[columna] > limite_superior)

def limpiar_datos(year, input_dir, output_dir, remove_outliers=True, verbose=False):
    """
    Limpia datos crudos aplicando validaciones y filtros.
    
    Args:
        year: Año de los datos a procesar
        input_dir: Directorio con datos crudos
        output_dir: Directorio para datos limpios
        remove_outliers: Si True, remueve outliers
        verbose: Si True, muestra mensajes detallados
    
    Returns:
        Path del archivo generado
    """
    if verbose:
        print(f"🧹 Limpiando datos del año {year}...")
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Leer datos crudos
    input_path = Path(input_dir) / f'raw_data_{year}.csv'
    
    if not input_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {input_path}")
    
    df = pd.read_csv(input_path)
    registros_iniciales = len(df)
    
    if verbose:
        print(f"\n📊 Datos iniciales: {registros_iniciales:,} registros")
    
    # 1. Validar que no haya columnas completamente nulas
    columnas_nulas = df.columns[df.isnull().all()].tolist()
    if columnas_nulas:
        print(f"⚠️  Eliminando columnas completamente nulas: {columnas_nulas}")
        df = df.drop(columns=columnas_nulas)
    
    # 2. Eliminar duplicados
    duplicados = df.duplicated().sum()
    if duplicados > 0:
        if verbose:
            print(f"🔍 Eliminando {duplicados} registros duplicados")
        df = df.drop_duplicates()
    
    # 3. Remover outliers en columna de precio (MedHouseVal)
    if remove_outliers and 'MedHouseVal' in df.columns:
        outliers_mask = detectar_outliers_iqr(df, 'MedHouseVal')
        n_outliers = outliers_mask.sum()
        
        if verbose:
            print(f"📉 Detectados {n_outliers} outliers en MedHouseVal")
        
        df = df[~outliers_mask]
    
    # 4. Validar rangos lógicos
    if 'AveRooms' in df.columns:
        # Las casas no pueden tener promedio negativo de habitaciones
        df = df[df['AveRooms'] > 0]
    
    if 'Population' in df.columns:
        # Población debe ser positiva
        df = df[df['Population'] > 0]
    
    # 5. Agregar columna de calidad de datos
    df['data_quality_score'] = 1.0  # Todos pasaron las validaciones
    
    # Crear directorio de salida
    output_path = Path(output_dir) / f'clean_data_{year}.csv'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Guardar datos limpios
    df.to_csv(output_path, index=False)
    
    registros_finales = len(df)
    registros_eliminados = registros_iniciales - registros_finales
    porcentaje_retenido = (registros_finales / registros_iniciales) * 100
    
    if verbose:
        print(f"\n📊 Resumen de limpieza:")
        print(f"   - Registros iniciales: {registros_iniciales:,}")
        print(f"   - Registros finales: {registros_finales:,}")
        print(f"   - Registros eliminados: {registros_eliminados:,}")
        print(f"   - Porcentaje retenido: {porcentaje_retenido:.2f}%")
        print(f"\n💾 Datos limpios guardados en: {output_path}")
        print(f"✅ Limpieza completada exitosamente")
    
    return output_path

def main():
    parser = argparse.ArgumentParser(
        description='Limpia datos crudos aplicando validaciones',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        '--year',
        type=int,
        required=True,
        help='Año de los datos a procesar'
    )
    
    parser.add_argument(
        '--input-dir',
        type=str,
        default='data/raw',
        help='Directorio con datos crudos'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='data/processed',
        help='Directorio de salida para datos limpios'
    )
    
    parser.add_argument(
        '--no-remove-outliers',
        action='store_true',
        help='No remover outliers'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Mostrar mensajes detallados'
    )
    
    args = parser.parse_args()
    
    try:
        limpiar_datos(
            year=args.year,
            input_dir=args.input_dir,
            output_dir=args.output_dir,
            remove_outliers=not args.no_remove_outliers,
            verbose=args.verbose
        )
    except Exception as e:
        print(f"❌ Error durante la limpieza: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())