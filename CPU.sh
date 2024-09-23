#!/bin/bash

# Configuración
DURATION=60  # Duración total en segundos
INTERVAL=0.5  # Intervalo entre muestras en segundos
OUTPUT_FILE="glances_data.csv"

# Ejecutar Glances y redirigir la salida a un archivo
glances --quiet --stdout-csv cpu,mem --time $INTERVAL --run-time $DURATION > $OUTPUT_FILE

echo "Datos recolectados y guardados en $OUTPUT_FILE"