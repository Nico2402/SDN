from mininet.net import Mininet 

from mininet.topo import LinearTopo 


Linear = LinearTopo(k=4) 

net = Mininet(topo=Linear) 

c0 = RemoteController (name='C0',controller=RemoteController, port=6653,  ip= contip) 

net.start() 
net.pingAll() 
net.stop() 
