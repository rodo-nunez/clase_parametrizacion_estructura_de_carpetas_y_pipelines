#!/usr/bin/env python3
"""
Orquestador de Pipeline en Python
Ejecuta todos los pasos del pipeline secuencialmente
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Colores para terminal (ANSI)
class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'  # No Color

def print_header(message):
    """Imprime un header destacado."""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.NC}")
    print(f"{Colors.BLUE}{message}{Colors.NC}")
    print(f"{Colors.BLUE}{'='*60}{Colors.NC}")

def run_step(step_name, script_path, args=None, required=True):
    """
    Ejecuta un paso del pipeline.
    
    Args:
        step_name: Nombre descriptivo del paso
        script_path: Ruta al script Python
        args: Lista de argumentos para el script
        required: Si True, detiene el pipeline si falla
    
    Returns:
        Código de salida del script
    """
    print(f"\n{Colors.YELLOW}▶️  Ejecutando: {step_name}{Colors.NC}")
    print(f"Script: {script_path}")
    
    # Construir comando
    cmd = f"python {script_path}"
    if args:
        cmd += " " + " ".join(args)
    
    print(f"Comando: {cmd}")
    print("-" * 60)
    
    # Ejecutar comando
    exit_code = os.system(cmd)
    
    if exit_code != 0:
        if required:
            print(f"\n{Colors.RED}❌ Error en {step_name}{Colors.NC}")
            print(f"{Colors.RED}Código de salida: {exit_code}{Colors.NC}")
            print(f"{Colors.RED}Pipeline detenido.{Colors.NC}")
            sys.exit(1)
        else:
            print(f"\n{Colors.YELLOW}⚠️  Advertencia en {step_name} (no crítico){Colors.NC}")
    else:
        print(f"\n{Colors.GREEN}✅ {step_name} completado{Colors.NC}")
    
    return exit_code

def crear_directorios():
    """Crea estructura de directorios necesaria."""
    directorios = [
        'data/raw',
        'data/processed',
        'results',
        'logs'
    ]
    
    for directorio in directorios:
        Path(directorio).mkdir(parents=True, exist_ok=True)
    
    print(f"{Colors.GREEN}✅ Directorios creados/verificados{Colors.NC}")

def main():
    """Ejecuta el pipeline completo."""
    
    # Registrar tiempo de inicio
    start_time = datetime.now()
    
    print_header("🚀 INICIANDO PIPELINE DE PROCESAMIENTO DE DATOS")
    print(f"Timestamp de inicio: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Directorio de trabajo: {os.getcwd()}")
    
    # Crear directorios necesarios
    print("\n📁 Preparando estructura de directorios...")
    crear_directorios()
    
    # Configuración del pipeline
    YEAR = 2024
    VERBOSE = "-v"  # Usar "" para desactivar verbose
    
    print(f"\n⚙️  Configuración:")
    print(f"   - Año a procesar: {YEAR}")
    print(f"   - Modo verbose: {'Activado' if VERBOSE else 'Desactivado'}")
    
    # Definir pasos del pipeline
    steps = [
        {
            'name': 'PASO 1: Extracción de Datos',
            'icon': '📥',
            'script': 'scripts/01_extraer_datos.py',
            'args': ['--year', str(YEAR), VERBOSE],
            'required': True
        },
        {
            'name': 'PASO 2: Limpieza de Datos',
            'icon': '🧹',
            'script': 'scripts/02_limpiar_datos.py',
            'args': ['--year', str(YEAR), VERBOSE],
            'required': True
        },
        {
            'name': 'PASO 3: Feature Engineering',
            'icon': '⚙️',
            'script': 'scripts/03_crear_features.py',
            'args': ['--year', str(YEAR), VERBOSE],
            'required': True
        },
        {
            'name': 'PASO 4: Generación de Reporte (TXT)',
            'icon': '📊',
            'script': 'scripts/04_generar_reporte.py',
            'args': ['--year', str(YEAR), '--formato', 'txt', VERBOSE],
            'required': True
        },
        {
            'name': 'PASO 5: Generación de Reporte (JSON)',
            'icon': '📄',
            'script': 'scripts/04_generar_reporte.py',
            'args': ['--year', str(YEAR), '--formato', 'json'],
            'required': False  # Este paso no es crítico
        }
    ]
    
    # Ejecutar cada paso
    print("\n" + "="*60)
    print("EJECUTANDO PIPELINE")
    print("="*60)
    
    for i, step in enumerate(steps, 1):
        print_header(f"{step['icon']} {step['name']}")
        run_step(
            step_name=step['name'],
            script_path=step['script'],
            args=step['args'],
            required=step['required']
        )
    
    # Resumen final
    end_time = datetime.now()
    duration = end_time - start_time
    
    print_header("🎉 PIPELINE COMPLETADO EXITOSAMENTE")
    print(f"Timestamp de finalización: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duración total: {duration}")
    
    print(f"\n{Colors.GREEN}📦 Archivos generados:{Colors.NC}")
    archivos = [
        f"data/raw/raw_data_{YEAR}.csv",
        f"data/processed/clean_data_{YEAR}.csv",
        f"data/processed/features_{YEAR}.csv",
        f"results/reporte_{YEAR}.txt",
        f"results/reporte_{YEAR}.json"
    ]
    
    for archivo in archivos:
        existe = "✅" if Path(archivo).exists() else "❌"
        print(f"  {existe} {archivo}")
    
    print(f"\n{Colors.GREEN}¡Pipeline ejecutado correctamente!{Colors.NC}")
    
    return 0

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Pipeline interrumpido por el usuario{Colors.NC}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error inesperado: {e}{Colors.NC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)