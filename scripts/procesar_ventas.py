#!/usr/bin/env python3
"""
Script de ejemplo: Procesamiento de ventas con argparse
Demuestra diferentes tipos de argumentos y buenas prácticas
"""

import argparse
import pandas as pd
from pathlib import Path
from datetime import datetime


def procesar_ventas(year, umbral, formato='csv', verbose=False, dry_run=False):
    """
    Procesa ventas de un año específico y filtra clientes importantes.

    Args:
        year: Año a procesar
        umbral: Umbral mínimo para considerar cliente importante
        formato: Formato de salida ('csv', 'json', 'excel')
        verbose: Si True, muestra mensajes detallados
        dry_run: Si True, simula la ejecución sin guardar archivos

    Returns:
        Número de clientes importantes encontrados
    """
    if verbose:
        print(f"{'='*60}")
        print(f"PROCESAMIENTO DE VENTAS - AÑO {year}")
        print(f"{'='*60}")
        print(f"Parámetros:")
        print(f"  - Año: {year}")
        print(f"  - Umbral: ${umbral:,.2f}")
        print(f"  - Formato: {formato}")
        print(f"  - Dry run: {'Sí' if dry_run else 'No'}")
        print(f"{'='*60}\n")

    # Simular carga de datos
    if verbose:
        print("📂 Leyendo datos...")

    # Crear datos de ejemplo
    n_clientes = 100
    df = pd.DataFrame({
        'cliente_id': [f'CLI_{i:04d}' for i in range(1, n_clientes + 1)],
        'nombre': [f'Cliente {i}' for i in range(1, n_clientes + 1)],
        'total_compras': [500 + i * 15 for i in range(n_clientes)],
        'num_transacciones': [5 + (i % 20) for i in range(n_clientes)],
        'fecha_ultima_compra': [f'{year}-{(i % 12) + 1:02d}-15' for i in range(n_clientes)]
    })

    if verbose:
        print(f"✅ Datos cargados: {len(df):,} clientes\n")

    # Filtrar clientes importantes
    if verbose:
        print(f"🔍 Filtrando clientes con compras > ${umbral:,.2f}...")

    clientes_importantes = df[df['total_compras'] > umbral].copy()

    # Agregar métricas adicionales
    clientes_importantes['ticket_promedio'] = (
        clientes_importantes['total_compras'] /
        clientes_importantes['num_transacciones']
    )

    if verbose:
        print(
            f"✅ Encontrados {len(clientes_importantes)} clientes importantes\n")

        # Mostrar estadísticas
        print("📊 Estadísticas:")
        print(f"  - Total clientes: {len(df):,}")
        print(f"  - Clientes importantes: {len(clientes_importantes):,}")
        print(
            f"  - Porcentaje: {(len(clientes_importantes)/len(df)*100):.1f}%")
        print(
            f"  - Compra promedio: ${clientes_importantes['total_compras'].mean():,.2f}")
        print(
            f"  - Compra máxima: ${clientes_importantes['total_compras'].max():,.2f}")
        print(
            f"  - Compra mínima: ${clientes_importantes['total_compras'].min():,.2f}\n")

    # Guardar resultados
    if not dry_run:
        output_dir = Path('results')
        output_dir.mkdir(exist_ok=True)

        if formato == 'csv':
            output_file = output_dir / f'clientes_importantes_{year}.csv'
            clientes_importantes.to_csv(output_file, index=False)
        elif formato == 'json':
            output_file = output_dir / f'clientes_importantes_{year}.json'
            clientes_importantes.to_json(
                output_file, orient='records', indent=2)
        elif formato == 'excel':
            output_file = output_dir / f'clientes_importantes_{year}.xlsx'
            clientes_importantes.to_excel(output_file, index=False)

        if verbose:
            print(f"💾 Resultados guardados en: {output_file}")
    else:
        if verbose:
            print("🔸 Modo dry-run: No se guardaron archivos")

    return len(clientes_importantes)


def main():
    """Función principal con configuración de argparse."""

    # Crear parser con descripción detallada
    parser = argparse.ArgumentParser(
        description='Procesa ventas y filtra clientes importantes según umbral de compras',
        epilog='Ejemplo: python procesar_ventas.py --year 2024 --umbral 1500 -v',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter  # Muestra valores por defecto
    )

    # ========================================
    # ARGUMENTOS REQUERIDOS
    # ========================================

    parser.add_argument(
        '--year',
        type=int,
        required=True,
        help='Año a procesar (ej: 2024)',
        metavar='YYYY'
    )

    # ========================================
    # ARGUMENTOS OPCIONALES CON VALORES POR DEFECTO
    # ========================================

    parser.add_argument(
        '--umbral',
        type=float,
        default=1000,
        help='Umbral mínimo de compras para considerar cliente importante',
        metavar='MONTO'
    )

    parser.add_argument(
        '--formato',
        type=str,
        choices=['csv', 'json', 'excel'],
        default='csv',
        help='Formato de archivo de salida'
    )

    # ========================================
    # BANDERAS BOOLEANAS (FLAGS)
    # ========================================

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Mostrar mensajes detallados durante la ejecución'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simular ejecución sin guardar archivos (útil para testing)'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    # ========================================
    # PARSEAR ARGUMENTOS
    # ========================================

    args = parser.parse_args()

    # ========================================
    # VALIDACIONES ADICIONALES
    # ========================================

    # Validar que el año sea razonable
    current_year = datetime.now().year
    if args.year < 2000 or args.year > current_year + 1:
        parser.error(f"El año debe estar entre 2000 y {current_year + 1}")

    # Validar que el umbral sea positivo
    if args.umbral <= 0:
        parser.error("El umbral debe ser un valor positivo")

    # ========================================
    # EJECUTAR PROCESAMIENTO
    # ========================================

    try:
        n_clientes = procesar_ventas(
            year=args.year,
            umbral=args.umbral,
            formato=args.formato,
            verbose=args.verbose,
            dry_run=args.dry_run
        )

        if not args.verbose:
            # Si no está en modo verbose, al menos mostrar resultado final
            print(
                f"✅ Proceso completado: {n_clientes} clientes importantes encontrados")

        return 0

    except FileNotFoundError as e:
        print(f"❌ Error: Archivo no encontrado - {e}")
        return 1
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())
