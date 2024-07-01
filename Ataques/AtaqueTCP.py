import socket
import threading
import time

def send_tcp_request(ip, port, message, delay):
    try:
        while True:
            # Crear un socket TCP
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((ip, port))
                sock.sendall(message.encode('utf-8'))  # Enviar un mensaje
                try:
                    response = sock.recv(1024)  # Intentar recibir una respuesta
                    print(f"Respuesta del servidor: {response.decode('utf-8')}")
                except socket.error:
                    # Si no hay respuesta, solo continuar
                    pass
            time.sleep(delay)  # Esperar un pequeño intervalo antes de la siguiente petición
    except socket.error as e:
        print(f"Error en la conexión: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    target_ip = "10.0.0.1"  # Reemplaza con la IP del servidor de prueba
    target_port = 80         # Reemplaza con el puerto del servidor de prueba
    message = "Hello, Server!"  # Mensaje a enviar
    delay = 0.01  # Intervalo en segundos entre peticiones (ajusta según sea necesario)

    # Crea múltiples hilos para simular múltiples clientes
    for i in range(1000):  # Aumenta el número de hilos para mayor presión
        thread = threading.Thread(target=send_tcp_request, args=(target_ip, target_port, message, delay))
        thread.start()