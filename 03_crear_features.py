#!/usr/bin/env python3
"""
Script 3: Feature Engineering
Crea variables derivadas y transformaciones para análisis
"""

import argparse
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime


def crear_features(year, input_dir, output_dir, verbose=False):
    """
    Crea features derivadas de los datos limpios.

    Args:
        year: Año de los datos a procesar
        input_dir: Directorio con datos limpios
        output_dir: Directorio para datos con features
        verbose: Si True, muestra mensajes detallados

    Returns:
        Path del archivo generado
    """
    if verbose:
        print(f"⚙️  Creando features para el año {year}...")
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Leer datos limpios
    input_path = Path(input_dir) / f'clean_data_{year}.csv'

    if not input_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {input_path}")

    df = pd.read_csv(input_path)
    columnas_iniciales = len(df.columns)

    if verbose:
        print(
            f"\n📊 Datos iniciales: {len(df):,} registros, {columnas_iniciales} columnas")

    # 1. Feature: Rooms per Household
    if 'AveRooms' in df.columns and 'AveBedrms' in df.columns:
        df['rooms_per_household'] = df['AveRooms'] / df['AveBedrms']
        df['rooms_per_household'] = df['rooms_per_household'].replace(
            [np.inf, -np.inf], np.nan)
        df['rooms_per_household'] = df['rooms_per_household'].fillna(
            df['rooms_per_household'].median())

    # 2. Feature: Population Density
    if 'Population' in df.columns and 'AveOccup' in df.columns:
        df['population_density'] = df['Population'] / \
            (df['AveOccup'] + 1)  # +1 para evitar división por 0

    # 3. Feature: Income per capita (proxy)
    if 'MedInc' in df.columns and 'AveOccup' in df.columns:
        df['income_per_capita'] = df['MedInc'] / df['AveOccup']

    # 4. Feature: Bedroom ratio
    if 'AveBedrms' in df.columns and 'AveRooms' in df.columns:
        df['bedroom_ratio'] = df['AveBedrms'] / \
            (df['AveRooms'] + 0.01)  # +0.01 para evitar división por 0

    # 5. Feature: Price category (basada en quantiles)
    if 'MedHouseVal' in df.columns:
        df['price_category'] = pd.qcut(
            df['MedHouseVal'],
            q=4,
            labels=['low', 'medium', 'high', 'very_high']
        )

    # 6. Feature: Income category
    if 'MedInc' in df.columns:
        df['income_category'] = pd.cut(
            df['MedInc'],
            bins=[0, 3, 5, 7, np.inf],
            labels=['low', 'medium', 'high', 'very_high']
        )

    # 7. Feature: House age category
    if 'HouseAge' in df.columns:
        df['house_age_category'] = pd.cut(
            df['HouseAge'],
            bins=[0, 10, 25, 40, np.inf],
            labels=['new', 'modern', 'old', 'very_old']
        )

    # 8. Feature: Logarithmic transformations (útiles para modelos)
    numeric_cols = ['MedInc', 'HouseAge', 'AveRooms', 'Population']
    for col in numeric_cols:
        if col in df.columns:
            # log1p = log(1 + x) para evitar log(0)
            df[f'{col}_log'] = np.log1p(df[col])

    # 9. Feature: Interaction terms
    if 'MedInc' in df.columns and 'HouseAge' in df.columns:
        df['income_age_interaction'] = df['MedInc'] * df['HouseAge']

    # 10. Feature: Standardized scores (útiles para comparaciones)
    if 'MedInc' in df.columns:
        mean_income = df['MedInc'].mean()
        std_income = df['MedInc'].std()
        df['income_zscore'] = (df['MedInc'] - mean_income) / std_income

    # Crear directorio de salida
    output_path = Path(output_dir) / f'features_{year}.csv'
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Guardar datos con features
    df.to_csv(output_path, index=False)

    columnas_finales = len(df.columns)
    features_creadas = columnas_finales - columnas_iniciales

    if verbose:
        print(f"\n📊 Resumen de feature engineering:")
        print(f"   - Registros procesados: {len(df):,}")
        print(f"   - Columnas iniciales: {columnas_iniciales}")
        print(f"   - Columnas finales: {columnas_finales}")
        print(f"   - Features creadas: {features_creadas}")
        print(f"\n🆕 Nuevas features:")
        nuevas_cols = [
            col for col in df.columns if col not in pd.read_csv(input_path).columns]
        for i, col in enumerate(nuevas_cols, 1):
            print(f"   {i}. {col}")
        print(f"\n💾 Datos con features guardados en: {output_path}")
        print(f"✅ Feature engineering completado exitosamente")

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Crea features derivadas de los datos limpios',
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
        default='data/processed',
        help='Directorio con datos limpios'
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        default='data/processed',
        help='Directorio de salida para datos con features'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Mostrar mensajes detallados'
    )

    args = parser.parse_args()

    try:
        crear_features(
            year=args.year,
            input_dir=args.input_dir,
            output_dir=args.output_dir,
            verbose=args.verbose
        )
    except Exception as e:
        print(f"❌ Error durante feature engineering: {e}")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
