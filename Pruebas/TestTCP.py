from scapy.all import *

# Enviar el SYN
ip = IP(dst="10.0.0.1")


for i in range(0,5000):
    sport = RandShort()
    tcp_syn = TCP(sport=sport, dport=80, flags="S", seq=0)
    syn_ack = sr1(ip/tcp_syn, timeout=5)

    if syn_ack is not None:
        print(f"Conexion en el puerto {sport}")
    # Enviar el ACK para completar el handshake
    #if syn_ack:
    #    tcp_ack = TCP(sport=syn_ack.dport, dport=80, flags="A", seq=syn_ack.ack, ack=syn_ack.seq + 1)
    #    send(ip/tcp_ack)
