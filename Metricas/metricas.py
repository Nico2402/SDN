import psutil
import time
import csv
from datetime import datetime

def get_cpu_percent():
    return psutil.cpu_percent(interval=0.5)

def main():
    duration = 60  # duración total en segundos
    interval = 0.5  # intervalo entre muestras en segundos
    filename = "cpu_usage.csv"

    print(f"Iniciando monitoreo de CPU por {duration} segundos...")
    print(f"Intervalo de muestreo: {interval} segundos")
    print(f"Los datos se guardarán en: {filename}")

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "CPU Usage (%)"])
        print("Archivo CSV creado y encabezados escritos.")

        end_time = time.time() + duration
        sample_count = 0
        print("Comenzando la recolección de datos...")
        while time.time() < end_time:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            cpu_percent = get_cpu_percent()
            writer.writerow([timestamp, cpu_percent])
            sample_count += 1
            if sample_count % 10 == 0:  # Informar cada 10 muestras
                print(f"Muestra {sample_count}: Timestamp: {timestamp}, CPU Usage: {cpu_percent}%")
            time.sleep(max(0, interval - 0.5))  # Restamos 0.5 porque psutil.cpu_percent ya toma 0.5s

    print(f"\nMonitoreo completado. Se recolectaron {sample_count} muestras.")
    print(f"Datos de CPU recolectados y guardados en {filename}")

if __name__ == "__main__":
    print("Iniciando script de monitoreo de CPU...")
    main()
    print("Script finalizado.")