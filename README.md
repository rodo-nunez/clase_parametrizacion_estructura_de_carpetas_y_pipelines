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
│   └── procesar_ventas.py
├── logs/                 # Logs de ejecución
├── .env.example          # Template de variables de ambiente
├── .gitignore
├── requirements.txt
└── README.md
```

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repo>
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

Después de ejecutar el pipeline, se generarán los siguientes archivos:

```
data/raw/raw_data_2024.csv              # Datos extraídos
data/processed/clean_data_2024.csv      # Datos limpios
data/processed/features_2024.csv        # Datos con features
results/reporte_2024.txt                # Reporte en texto
results/reporte_2024.json               # Reporte en JSON
```

## 🎯 Características del Proyecto

### ✅ Parametrización

- Variables definidas una sola vez al inicio
- Uso de argumentos CLI con `argparse`
- Soporte para variables de ambiente con `.env`
- Queries SQL parametrizadas

### ✅ Modularización

- Un script por responsabilidad
- Funciones reutilizables
- Manejo de errores robusto
- Logging detallado

### ✅ Orquestación

- Pipeline ejecutable con Bash o Python
- Verificación de errores en cada paso
- Reporte de tiempo de ejecución
- Modo verbose para debugging

## 🔍 Ejemplos de Uso Avanzado

### Procesar múltiples años

```bash
for year in 2020 2021 2022 2023 2024; do
    python scripts/run_pipeline.py --year $year
done
```

### Ejecutar solo pasos específicos

```bash
# Solo limpieza y features
python scripts/02_limpiar_datos.py --year 2024 -v
python scripts/03_crear_features.py --year 2024 -v
```

### Generar reportes en ambos formatos

```bash
python scripts/04_generar_reporte.py --year 2024 --formato txt
python scripts/04_generar_reporte.py --year 2024 --formato json
```

## 🛠️ Personalización

### Agregar un nuevo paso al pipeline

1. Crear script numerado: `05_mi_nuevo_paso.py`
2. Usar `argparse` para parámetros
3. Agregar al orquestador (`run_pipeline.sh` o `run_pipeline.py`)

Ejemplo de estructura para nuevo script:

```python
#!/usr/bin/env python3
import argparse

def mi_funcion(year, verbose=False):
    # Tu lógica aquí
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int, required=True)
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()
    
    mi_funcion(args.year, args.verbose)

if __name__ == '__main__':
    main()
```

### Modificar parámetros por defecto

Editar las variables de configuración en cada script:

```python
# En 02_limpiar_datos.py
UMBRAL_OUTLIERS = 1.5  # Cambiar este valor

# En 03_crear_features.py
BINS_PRICE = [0, 2, 4, 6, np.inf]  # Modificar bins
```

## 📚 Recursos Adicionales

- **Documentación de argparse**: https://docs.python.org/3/library/argparse.html
- **Python-dotenv**: https://pypi.org/project/python-dotenv/
- **Cookiecutter Data Science**: https://github.com/drivendata/cookiecutter-data-science
- **Ejemplo de modularización**: https://github.com/rodo-nunez/ejemplo_de_modularizacion_de_proyecto

## 🐛 Troubleshooting

### Error: "No module named 'sklearn'"

```bash
pip install scikit-learn
```

### Error: "FileNotFoundError"

Asegúrate de ejecutar los scripts en orden o usar el orquestador completo.

### Los scripts Bash no se ejecutan en Windows

Usa Git Bash o WSL, o ejecuta la versión Python del orquestador:

```bash
python scripts/run_pipeline.py
```

### Permisos denegados en Linux/Mac

```bash
chmod +x scripts/run_pipeline.sh
```

## 📝 Notas Importantes

- **NUNCA** subir el archivo `.env` a Git (contiene credenciales)
- Los datos en `data/raw/` no deben modificarse directamente
- Usar siempre modo verbose (`-v`) durante desarrollo
- Revisar logs en caso de errores

## 🤝 Contribuciones

Este es un proyecto educativo. Siéntete libre de:

- Agregar nuevos pasos al pipeline
- Mejorar el manejo de errores
- Agregar tests unitarios
- Crear visualizaciones adicionales

## 📄 Licencia

Este proyecto es para uso educativo y está disponible bajo licencia MIT.

---

**¿Preguntas?** Abre un issue o contacta al instructor del curso.