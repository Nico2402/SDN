from scapy.all import *
import threading
import time

def send_tcp_ack(ip, port):
    # Crear el paquete SYN para iniciar la conexión
    syn = IP(dst=ip)/TCP(dport=port, flags='S')
    syn_ack = sr1(syn, timeout=2)  # Enviar y recibir el SYN-ACK
    
    if syn_ack is None:
        print(f"Conexión a {ip}:{port} falló al recibir SYN-ACK.")
        return

    # Crear el paquete ACK para completar el three-way handshake
    ack = IP(dst=ip)/TCP(dport=port, sport=syn_ack[TCP].dport, flags='A', seq=syn_ack.ack, ack=syn_ack.seq + 1)
    send(ack)
    print(f"Conexión establecida a {ip}:{port}")

    # Enviar paquetes TCP con la bandera ACK para mantener la conexión viva
    while True:
        try:
            # El paquete ACK para mantener la conexión
            keep_alive = IP(dst=ip)/TCP(dport=port, sport=ack[TCP].sport, flags='A', seq=ack.seq, ack=ack.ack)
            send(keep_alive)
            print(f"Enviando ACK a {ip}:{port}")
            time.sleep(1)  # Pausa breve entre los envíos
        except KeyboardInterrupt:
            print("Interrumpido por el usuario.")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    target_ip = "10.0.0.1"  # IP del servidor de prueba
    target_port = 80        # Puerto del servidor de prueba

    # Crea múltiples hilos para simular múltiples conexiones simultáneas
    for i in range(1):  # Ajusta el número de hilos según sea necesario
        thread = threading.Thread(target=send_tcp_ack, args=(target_ip, target_port))
        thread.start()
        time.sleep(10)  # Retraso breve para escalonar la creación de conexiones
