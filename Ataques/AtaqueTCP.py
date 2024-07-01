import socket
import threading
import time

def send_tcp_request(ip, port):
    try:
        # Crear un socket TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # Activar keep-alive
        print(f"Conexión establecida a {ip}:{port}")
        
        # Mantener la conexión activa y enviar datos continuamente
        while True:
            try:
                # Enviar datos
                message = b"GET / HTTP/1.1\r\nHost: " + ip.encode('utf-8') + b"\r\n\r\n"
                sock.sendall(message)
                
                # Esperar un tiempo antes de enviar el próximo mensaje
                time.sleep(1)  # Puedes ajustar el intervalo según sea necesario
            except socket.error as e:
                print(f"Error al enviar datos a {ip}:{port}: {e}")
                break
    except socket.error as e:
        print(f"Error en la conexión: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    target_ip = "10.0.0.1"  # IP del servidor de prueba
    target_port = 80         # Puerto del servidor de prueba

    # Crea múltiples hilos para simular múltiples conexiones simultáneas
    for i in range(1000):  # Ajusta el número de hilos según sea necesario
        thread = threading.Thread(target=send_tcp_request, args=(target_ip, target_port))
        thread.start()
        time.sleep(0.01)  # Retraso breve para escalonar la creación de conexiones