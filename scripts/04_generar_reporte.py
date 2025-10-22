#!/usr/bin/env python3
"""
Script 4: Generación de Reporte
Genera visualizaciones y métricas resumidas
"""

import argparse
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json


def calcular_estadisticas(df, columnas_numericas):
    """Calcula estadísticas descriptivas."""
    stats = {}
    for col in columnas_numericas:
        if col in df.columns:
            stats[col] = {
                'mean': float(df[col].mean()),
                'median': float(df[col].median()),
                'std': float(df[col].std()),
                'min': float(df[col].min()),
                'max': float(df[col].max()),
                'q25': float(df[col].quantile(0.25)),
                'q75': float(df[col].quantile(0.75))
            }
    return stats


def generar_reporte(year, input_dir, output_dir, formato='txt', verbose=False):
    """
    Genera reporte con estadísticas y visualizaciones.

    Args:
        year: Año de los datos a procesar
        input_dir: Directorio con datos procesados
        output_dir: Directorio para reportes
        formato: Formato del reporte ('txt' o 'json')
        verbose: Si True, muestra mensajes detallados

    Returns:
        Path del archivo generado
    """
    if verbose:
        print(f"📊 Generando reporte para el año {year}...")
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Leer datos con features
    input_path = Path(input_dir) / f'features_{year}.csv'

    if not input_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {input_path}")

    df = pd.read_csv(input_path)

    if verbose:
        print(
            f"\n📊 Datos cargados: {len(df):,} registros, {len(df.columns)} columnas")

    # Preparar directorio de salida
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    # 1. Estadísticas descriptivas
    columnas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
    stats = calcular_estadisticas(
        df, columnas_numericas[:10])  # Primeras 10 columnas

    # 2. Conteo por categorías
    conteos = {}
    if 'price_category' in df.columns:
        conteos['price_category'] = df['price_category'].value_counts().to_dict()
    if 'income_category' in df.columns:
        conteos['income_category'] = df['income_category'].value_counts().to_dict()

    # 3. Correlaciones principales
    correlaciones = {}
    if 'MedHouseVal' in df.columns:
        corr_con_precio = df[columnas_numericas].corrwith(
            df['MedHouseVal']).sort_values(ascending=False)
        correlaciones['top_5_positivas'] = corr_con_precio.head(
            6).to_dict()  # 6 porque incluye consigo mismo
        correlaciones['top_5_negativas'] = corr_con_precio.tail(5).to_dict()

    # 4. Métricas de calidad
    metricas_calidad = {
        'total_registros': len(df),
        'total_columnas': len(df.columns),
        'registros_completos': int(df.dropna().shape[0]),
        'porcentaje_completos': float((df.dropna().shape[0] / len(df)) * 100),
        'valores_nulos_por_columna': df.isnull().sum().to_dict()
    }

    # 5. Generar reporte
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if formato == 'json':
        # Reporte en formato JSON
        reporte = {
            'metadata': {
                'year': year,
                'fecha_generacion': timestamp,
                'archivo_fuente': str(input_path)
            },
            'estadisticas_descriptivas': stats,
            'conteos_categoricos': conteos,
            'correlaciones': correlaciones,
            'metricas_calidad': metricas_calidad
        }

        output_path = output_dir_path / f'reporte_{year}.json'
        with open(output_path, 'w') as f:
            json.dump(reporte, f, indent=2)

    else:
        # Reporte en formato texto
        output_path = output_dir_path / f'reporte_{year}.txt'

        with open(output_path, 'w') as f:
            f.write("="*70 + "\n")
            f.write(f"REPORTE DE ANÁLISIS - AÑO {year}\n")
            f.write("="*70 + "\n")
            f.write(f"Fecha de generación: {timestamp}\n")
            f.write(f"Archivo fuente: {input_path}\n")
            f.write("="*70 + "\n\n")

            # Sección 1: Métricas de calidad
            f.write("1. MÉTRICAS DE CALIDAD DE DATOS\n")
            f.write("-" * 70 + "\n")
            f.write(
                f"Total de registros: {metricas_calidad['total_registros']:,}\n")
            f.write(
                f"Total de columnas: {metricas_calidad['total_columnas']}\n")
            f.write(
                f"Registros completos: {metricas_calidad['registros_completos']:,}\n")
            f.write(
                f"Porcentaje completos: {metricas_calidad['porcentaje_completos']:.2f}%\n\n")

            # Sección 2: Estadísticas descriptivas
            f.write("2. ESTADÍSTICAS DESCRIPTIVAS (PRINCIPALES VARIABLES)\n")
            f.write("-" * 70 + "\n")
            for col, stat in list(stats.items())[:5]:  # Top 5 variables
                f.write(f"\n{col}:\n")
                f.write(f"  Media: {stat['mean']:.4f}\n")
                f.write(f"  Mediana: {stat['median']:.4f}\n")
                f.write(f"  Desv. Est.: {stat['std']:.4f}\n")
                f.write(f"  Rango: [{stat['min']:.4f}, {stat['max']:.4f}]\n")

            # Sección 3: Distribuciones categóricas
            if conteos:
                f.write("\n3. DISTRIBUCIONES CATEGÓRICAS\n")
                f.write("-" * 70 + "\n")
                for categoria, valores in conteos.items():
                    f.write(f"\n{categoria}:\n")
                    for valor, count in valores.items():
                        porcentaje = (count / len(df)) * 100
                        f.write(f"  {valor}: {count:,} ({porcentaje:.2f}%)\n")

            # Sección 4: Correlaciones
            if correlaciones:
                f.write("\n4. CORRELACIONES CON PRECIO DE VIVIENDA\n")
                f.write("-" * 70 + "\n")
                f.write("\nTop 5 correlaciones positivas:\n")
                for var, corr in list(correlaciones['top_5_positivas'].items())[:5]:
                    f.write(f"  {var}: {corr:.4f}\n")

                f.write("\nTop 5 correlaciones negativas:\n")
                for var, corr in list(correlaciones['top_5_negativas'].items())[:5]:
                    f.write(f"  {var}: {corr:.4f}\n")

            f.write("\n" + "="*70 + "\n")
            f.write("FIN DEL REPORTE\n")
            f.write("="*70 + "\n")

    if verbose:
        print(f"\n📊 Reporte generado exitosamente")
        print(f"   - Formato: {formato.upper()}")
        print(f"   - Variables analizadas: {len(stats)}")
        print(f"   - Categorías analizadas: {len(conteos)}")
        print(f"\n💾 Reporte guardado en: {output_path}")
        print(f"✅ Generación de reporte completada")

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Genera reporte de análisis de datos',
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
        help='Directorio con datos procesados'
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        default='results',
        help='Directorio de salida para reportes'
    )

    parser.add_argument(
        '--formato',
        type=str,
        choices=['txt', 'json'],
        default='txt',
        help='Formato del reporte'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Mostrar mensajes detallados'
    )

    args = parser.parse_args()

    try:
        generar_reporte(
            year=args.year,
            input_dir=args.input_dir,
            output_dir=args.output_dir,
            formato=args.formato,
            verbose=args.verbose
        )
    except Exception as e:
        print(f"❌ Error durante generación de reporte: {e}")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
