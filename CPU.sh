#!/bin/bash

# Configuración
DURATION=60  # Duración total en segundos
INTERVAL=0.5  # Intervalo entre muestras en segundos
OUTPUT_FILE="glances_data.csv"

# Ejecutar Glances en modo CSV y redirigir la salida a un archivo
glances --quiet --export-csv $OUTPUT_FILE --time $INTERVAL --run-time $DURATION

echo "Datos recolectados y guardados en $OUTPUT_FILE"