from scapy.all import *
import threading
import time
from pypacker.layer12 import ethernet
from pypacker.layer3 import ip
from pypacker.layer4 import tcp
import socket

def create_syn_packet(src_ip, dst_ip, src_port, dst_port):
    # Crear el paquete Ethernet
    eth = ethernet.Ethernet(dst='ff:ff:ff:ff:ff:ff', src='52:6f:7b:49:78:20', type=0x0800)

    # Crear el paquete IP
    ip_pkt = ip.IP(src=src_ip, dst=dst_ip)

    # Crear el paquete TCP SYN
    tcp_pkt = tcp.TCP(sport=src_port, dport=dst_port, flags='S', seq=1000)

    # Convertir cada capa a bytes
    eth_bytes = bytes(eth)
    ip_bytes = bytes(ip_pkt)
    tcp_bytes = bytes(tcp_pkt)

    # Ensamblar el paquete completo: Ethernet + IP + TCP
    pkt = eth_bytes + ip_bytes + tcp_bytes
    return pkt

def send_packet(packet, iface):
    # Crear un socket raw
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
    
    # Configurar la interfaz
    sock.bind((iface, 0))

    # Enviar el paquete
    sock.send(packet)
    print("Paquete SYN enviado!")

if __name__ == "__main__":
    # Configura las direcciones IP y puertos
    source_ip = "10.0.0.2"
    destination_ip = "10.0.0.1"
    source_port = 12345
    destination_port = 80

    # Crear el paquete SYN
    syn_packet = create_syn_packet(source_ip, destination_ip, source_port, destination_port)
    
    # Enviar el paquete SYN a través de la interfaz h2-eth0
    send_packet(syn_packet, 'h2-eth0')
