import subprocess
from scapy.all import Ether, IP, sendp
import random
import time

# Configura el OVS para enviar todos los paquetes al controlador
bridge_name = "br0"  # Nombre del puente OVS
subprocess.run(["ovs-ofctl", "add-flow", bridge_name, "priority=100,actions=controller"])

# Función para generar una dirección MAC aleatoria
def random_mac():
    return "02:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )

# Enviar paquetes al bridge con direcciones MAC de destino aleatorias
def flood_packets(interface, count):
    for _ in range(count):
        pkt = Ether(dst=random_mac()) / IP(dst="10.0.0.1")
        sendp(pkt, iface=interface, verbose=0)
        time.sleep(0.01)  # Pequeña pausa para no saturar la red inmediatamente

# Especifica la interfaz a utilizar
interface = "eth0"  # Interfaz del sistema que conecta al OVS

# Número de paquetes a enviar
packet_count = 1000

print(f"Iniciando envío de {packet_count} paquetes...")
flood_packets(interface, packet_count)
print("Envió completo.")
