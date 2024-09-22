from scapy.all import *

# Enviar el SYN
ip = IP(src="10.0.0.2", dst="10.0.0.1")
tcp_syn = TCP(sport=RandShort(), dport=80, flags="S", seq=0)
syn_ack = sr1(ip/tcp_syn, timeout=5)

for i in range(0,5000):
    if syn_ack is None:
        print(f"Conexión a 10.0.0.1:80 falló al recibir SYN-ACK.")

    # Enviar el ACK para completar el handshake
    if syn_ack:
        tcp_ack = TCP(sport=syn_ack.dport, dport=80, flags="A", seq=syn_ack.ack, ack=syn_ack.seq + 1)
        send(ip/tcp_ack)
