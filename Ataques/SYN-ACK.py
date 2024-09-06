from scapy.all import *
import threading
import time

from pypacker.layer12 import ethernet
from pypacker.layer3 import ip
from pypacker.layer4 import tcp
import socket

def create_syn_packet(src_ip, dst_ip, dst_port):

    source_ports = list(range(1024, 65535))
    sport = random.choice(source_ports)
    eth = ethernet.Ethernet(dst='ff:ff:ff:ff:ff:ff', src='52:6f:7b:49:78:20', type=0x0800)
    ip_pkt = ip.IP(src=src_ip, dst=dst_ip)
    tcp_pkt = tcp.TCP(sport=sport, dport=dst_port, flags='S', seq=1000)
    pkt = eth / ip_pkt / tcp_pkt
    return pkt

def send_packet(packet, iface):
    # Crear un socket raw
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
    
    # Configurar la interfaz
    sock.bind((iface, 0))

    # Enviar el paquete
    sock.send(packet.bytes)
    print("Paquete SYN enviado!")


if __name__ == "__main__":
    source_ip= "10.0.0.2"
    target_ip = "10.0.0.1"  # IP del servidor de prueba
    destination_port = 80      # Puerto del servidor de prueba
    #for i in range(0):
    syn_packet = create_syn_packet(source_ip, target_ip,destination_port)
    send_packet(syn_packet, 'h2-eth0')




#--------------------------------------------------------------------------------------------------------------



    # Crear el paquete SYN para iniciar la conexión
    #source_ports = list(range(1024, 65535))
    #sport = random.choice(source_ports)
    
    #syn = IP(dst=ip)/TCP(sport=1024, dport=port, flags='S')
    #send(syn,timeout=1000)
    #time.sleep(2)
    #syn_ack = sr1(syn, timeout=1000, verbose=0)  # Enviar y recibir el SYN-ACK

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
