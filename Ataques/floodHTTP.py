import requests
import threading

def send_request(url):
    try:
        while True:
            response = requests.get(url)
            print(f"Petición enviada: {response.status_code}")
    except requests.ConnectionError:
        print("Servidor no accesible.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    target_ip = "10.0.0.10"  # Reemplaza con la IP del servidor de prueba
    target_port = 80      # Reemplaza con el puerto del servidor de prueba
    url = f"http://{target_ip}:{target_port}"

    # Crea múltiples hilos para simular múltiples clientes
    for i in range(150):  # Ajusta el número de hilos según sea necesario
        thread = threading.Thread(target=send_request, args=(url,))
        thread.start()