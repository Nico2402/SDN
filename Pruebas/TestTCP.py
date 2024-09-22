from scapy.all import *

ip = IP(src="10.0.0.2", dst="10.0.0.1")
tcp = TCP(sport=RandShort(), dport=80, flags="S")
pkt = ip/tcp
sendp(pkt,verbose=False)
