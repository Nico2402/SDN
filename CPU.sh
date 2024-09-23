#!/bin/bash

# Configuración
DURATION=60  # Duración total en segundos
INTERVAL=0.5  # Intervalo entre muestras en segundos
OUTPUT_FILE="glances_data.csv"

# Usar timeout y redirigir la salida a un archivo
timeout $DURATION glances --quiet --stdout-csv cpu,mem --time $INTERVAL > $OUTPUT_FILE

echo "Datos recolectados y guardados en $OUTPUT_FILE"