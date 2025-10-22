# Pipeline de Procesamiento de Datos - Ejemplo de Clase

Este proyecto es un ejemplo completo de parametrización, estructura de carpetas y pipelines para análisis de datos.

## 📁 Estructura del Proyecto

```
proyecto_ejemplo/
├── data/
│   ├── raw/              # Datos originales (no modificar)
│   └── processed/        # Datos procesados
├── results/              # Reportes y visualizaciones
├── scripts/              # Scripts del pipeline
│   ├── 01_extraer_datos.py
│   ├── 02_limpiar_datos.py
│   ├── 03_crear_features.py
│   ├── 04_generar_reporte.py
│   ├── run_pipeline.sh
│   └── run_pipeline.py
├── logs/                 # Logs de ejecución
├── .env.example          # Template de variables de ambiente
├── .gitignore
├── requirements.txt
└── README.md
```

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone 
cd proyecto_ejemplo
```

### 2. Crear ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de ambiente

```bash
cp .env.example .env
# Editar .env con tus valores
```

## 📊 Uso

### Opción 1: Ejecutar pipeline completo con Bash

```bash
chmod +x scripts/run_pipeline.sh
./scripts/run_pipeline.sh
```

### Opción 2: Ejecutar pipeline completo con Python

```bash
python scripts/run_pipeline.py
```

### Opción 3: Ejecutar scripts individuales

```bash
# Paso 1: Extracción
python scripts/01_extraer_datos.py --year 2024 --verbose

# Paso 2: Limpieza
python scripts/02_limpiar_datos.py --year 2024 --verbose

# Paso 3: Feature Engineering
python scripts/03_crear_features.py --year 2024 --verbose

# Paso 4: Reporte
python scripts/04_generar_reporte.py --year 2024 --formato txt --verbose
```

## 🔧 Parámetros Disponibles

Todos los scripts aceptan los siguientes parámetros:

- `--year`: Año de los datos a procesar (requerido)
- `--verbose` o `-v`: Mostrar mensajes detallados
- `--help`: Mostrar ayuda

### Script 01: Extracción

```bash
python scripts/01_extraer_datos.py --year 2024 --output-dir data/raw -v
```

### Script 02: Limpieza

```bash
python scripts/02_limpiar_datos.py --year 2024 --no-remove-outliers -v
```

### Script 03: Feature Engineering

```bash
python scripts/03_crear_features.py --year 2024 -v
```

### Script 04: Reporte

```bash
python scripts/04_generar_reporte.py --year 2024 --formato json -v
```

## 📦 Archivos Generados

Después de ejecutar el pipeline, se generarán

<!-- TODO Continuar -->