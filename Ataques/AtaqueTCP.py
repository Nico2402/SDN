import socket
import threading

def establish_tcp_connection(ip, port):
    try:
        # Crear un socket TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        print(f"Conexión establecida a {ip}:{port}")
        # Mantener la conexión abierta indefinidamente
        while True:
            pass
    except socket.error as e:
        print(f"Error en la conexión: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    target_ip = "10.0.0.1"  # IP del servidor de prueba
    target_port = 80         # Puerto del servidor de prueba

    # Crea múltiples hilos para simular múltiples conexiones simultáneas
    for i in range(1000):  # Ajusta el número de hilos según sea necesario
        thread = threading.Thread(target=establish_tcp_connection, args=(target_ip, target_port))
        thread.start()