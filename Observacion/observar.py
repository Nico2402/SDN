import psutil
import csv
import time

# Nombre del archivo CSV
csv_file = 'cpu_memory_usage.csv'

# Abre el archivo CSV para escritura
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Escribe el encabezado
    writer.writerow(['Timestamp', 'CPU_Usage(%)', 'Memory_Usage(%)'])
    
    try:
        while True:
            # Obtiene el tiempo actual
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            
            # Obtiene el uso de CPU y memoria
            cpu_usage = psutil.cpu_percent(interval=1)  # Intervalo de 1 segundo
            memory_usage = psutil.virtual_memory().percent
            
            # Escribe la fila en el archivo CSV
            writer.writerow([timestamp, cpu_usage, memory_usage])
            
            # Espera 1 segundo antes de la siguiente medición
            time.sleep(1)
    except KeyboardInterrupt:
        print("Captura detenida.")

print(f"Datos guardados en {csv_file}.")
