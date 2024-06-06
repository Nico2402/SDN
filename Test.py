import requests
import time

def check_server(ip, port):
    url = f"http://{ip}:{port}"
    try:
        response = requests.get(url)
        # Si la respuesta es 200 OK, el servidor está activo
        if response.status_code == 200:
            print(f"El servidor en {url} está activo.")
        else:
            print(f"El servidor en {url} devolvió el código de estado: {response.status_code}")
    except requests.ConnectionError:
        print(f"El servidor en {url} está caído.")

if __name__ == "__main__":
    ip = "10.0.0.10"  # Reemplaza con la IP de tu servidor
    port = 80         # Reemplaza con el puerto de tu servidor
    while True:
        check_server(ip, port)
        time.sleep(1)