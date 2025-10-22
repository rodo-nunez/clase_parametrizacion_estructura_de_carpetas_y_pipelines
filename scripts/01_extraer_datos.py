#!/usr/bin/env python3
"""
Script 1: Extracción de Datos
Extrae datos del dataset California Housing de sklearn
"""

import argparse
import pandas as pd
from pathlib import Path
from sklearn.datasets import fetch_california_housing
from datetime import datetime


def extraer_datos(year, output_dir, verbose=False):
    """
    Extrae datos de California Housing y los guarda como CSV.

    Args:
        year: Año para etiquetar los datos
        output_dir: Directorio donde guardar los datos
        verbose: Si True, muestra mensajes detallados

    Returns:
        Path del archivo generado
    """
    if verbose:
        print(f"📥 Extrayendo datos para el año {year}...")
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Cargar dataset de California Housing
    california = fetch_california_housing(as_frame=True)
    df = california.frame

    # Agregar columna de año para simular datos temporales
    df['year'] = year
    df['extraction_date'] = datetime.now().strftime('%Y-%m-%d')

    # Crear directorio si no existe
    output_path = Path(output_dir) / f'raw_data_{year}.csv'
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Guardar datos
    df.to_csv(output_path, index=False)

    if verbose:
        print(f"\n📊 Resumen de extracción:")
        print(f"   - Registros extraídos: {len(df):,}")
        print(f"   - Columnas: {len(df.columns)}")
        print(
            f"   - Tamaño en memoria: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        print(f"\n💾 Datos guardados en: {output_path}")
        print(f"✅ Extracción completada exitosamente")

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Extrae datos de California Housing',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '--year',
        type=int,
        required=True,
        help='Año para etiquetar los datos'
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        default='data/raw',
        help='Directorio de salida para datos crudos'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Mostrar mensajes detallados'
    )

    args = parser.parse_args()

    try:
        extraer_datos(
            year=args.year,
            output_dir=args.output_dir,
            verbose=args.verbose
        )
    except Exception as e:
        print(f"❌ Error durante la extracción: {e}")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
