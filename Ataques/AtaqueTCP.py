import socket
import threading
import time

def send_tcp_request(ip, port):
    try:
        # Crear un socket TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        print(f"Conexión establecida a {ip}:{port}")
        while True:
            try:
                # Enviar datos constantemente
                sock.sendall(b"GET / HTTP/1.1\r\nHost: " + ip.encode('utf-8') + b"\r\n\r\n")
                time.sleep(0.1)  # Pausa breve para evitar abrumar el sistema local
            except socket.error:
                print(f"Error al enviar datos a {ip}:{port}")
                break
    except socket.error as e:
        print(f"Error en la conexión: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    target_ip = "10.0.0.1"  # IP del servidor de prueba
    target_port = 80         # Puerto del servidor de prueba

    # Crea múltiples hilos para simular múltiples conexiones simultáneas
    for i in range(2000):  # Aumenta el número de hilos para generar más carga
        thread = threading.Thread(target=send_tcp_request, args=(target_ip, target_port))
        thread.start()
        time.sleep(0.01)  # Retraso breve para escalonar la creación de conexiones
