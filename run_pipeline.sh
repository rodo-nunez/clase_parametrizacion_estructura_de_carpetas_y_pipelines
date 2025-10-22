#!/bin/bash

################################################################################
# Pipeline de Procesamiento de Datos
# Ejecuta secuencialmente todos los pasos del pipeline
################################################################################

# Configuración
PYTHON=python3
SCRIPTS_DIR=scripts
YEAR=2024
VERBOSE="-v"  # Comentar esta línea para ejecución silenciosa

# Colores para output (opcional)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir headers
print_header() {
    echo ""
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Función para verificar éxito de comando
check_status() {
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Error en: $1${NC}"
        echo -e "${RED}Pipeline detenido.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ $1 completado${NC}"
}

################################################################################
# INICIO DEL PIPELINE
################################################################################

print_header "🚀 INICIANDO PIPELINE"
echo "Año a procesar: $YEAR"
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Crear directorios necesarios
mkdir -p data/raw
mkdir -p data/processed
mkdir -p results
mkdir -p logs

################################################################################
# PASO 1: EXTRACCIÓN DE DATOS
################################################################################

print_header "📥 PASO 1: EXTRACCIÓN DE DATOS"
$PYTHON $SCRIPTS_DIR/01_extraer_datos.py --year $YEAR $VERBOSE
check_status "Extracción de datos"

################################################################################
# PASO 2: LIMPIEZA DE DATOS
################################################################################

print_header "🧹 PASO 2: LIMPIEZA DE DATOS"
$PYTHON $SCRIPTS_DIR/02_limpiar_datos.py --year $YEAR $VERBOSE
check_status "Limpieza de datos"

################################################################################
# PASO 3: FEATURE ENGINEERING
################################################################################

print_header "⚙️  PASO 3: FEATURE ENGINEERING"
$PYTHON $SCRIPTS_DIR/03_crear_features.py --year $YEAR $VERBOSE
check_status "Feature Engineering"

################################################################################
# PASO 4: GENERACIÓN DE REPORTE
################################################################################

print_header "📊 PASO 4: GENERACIÓN DE REPORTE"
$PYTHON $SCRIPTS_DIR/04_generar_reporte.py --year $YEAR --formato txt $VERBOSE
check_status "Generación de reporte"

# Generar también versión JSON
echo ""
echo "Generando reporte en formato JSON..."
$PYTHON $SCRIPTS_DIR/04_generar_reporte.py --year $YEAR --formato json
check_status "Reporte JSON"

################################################################################
# FINALIZACIÓN
################################################################################

print_header "🎉 PIPELINE COMPLETADO EXITOSAMENTE"
echo "Timestamp final: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""
echo "Archivos generados:"
echo "  - data/raw/raw_data_${YEAR}.csv"
echo "  - data/processed/clean_data_${YEAR}.csv"
echo "  - data/processed/features_${YEAR}.csv"
echo "  - results/reporte_${YEAR}.txt"
echo "  - results/reporte_${YEAR}.json"
echo ""
echo -e "${GREEN}¡Pipeline ejecutado correctamente!${NC}"