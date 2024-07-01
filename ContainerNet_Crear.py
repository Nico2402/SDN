from containernet.net import Containernet
from containernet.node import Controller, RemoteController, Docker
from containernet.link import TCLink
from containernet.cli import CLI
from mininet.log import setLogLevel, info

def myNetwork():

    net = Containernet(topo=None,
                       build=False,
                       link=TCLink,  # Usar TCLink para soporte de control de tráfico
                       ipBase='10.0.0.0/8')
    
    info('*** Adding controller\n')

    c0 = net.addController(name='c0',
                           controller=RemoteController,
                           ip='172.17.0.2',
                           protocol='tcp',
                           port=6633)
    
    info('*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, protocols=["OpenFlow13"])
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, protocols=["OpenFlow13"])

    info('*** Add Docker containers as hosts\n')
    h1 = net.addDocker('h1', ip='10.0.0.1', dimage="ubuntu:latest")
    h2 = net.addDocker('h2', ip='10.0.0.2', dimage="ubuntu:latest")
    h3 = net.addDocker('h3', ip='10.0.0.3', dimage="ubuntu:latest")
    h4 = net.addDocker('h4', ip='10.0.0.4', dimage="ubuntu:latest")
    h5 = net.addDocker('h5', ip='10.0.0.5', dimage="ubuntu:latest")
    h6 = net.addDocker('h6', ip='10.0.0.6', dimage="ubuntu:latest")
    h7 = net.addDocker('h7', ip='10.0.0.7', dimage="ubuntu:latest")
    h8 = net.addDocker('h8', ip='10.0.0.8', dimage="ubuntu:latest")
    h9 = net.addDocker('h9', ip='10.0.0.9', dimage="ubuntu:latest")
    h10 = net.addDocker('h10', ip='10.0.0.10', dimage="ubuntu:latest")

    info('*** Add links\n')

    net.addLink(s1, s2)
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s2)
    net.addLink(h4, s2)
    net.addLink(h5, s1)
    net.addLink(h6, s2)
    net.addLink(h7, s1)
    net.addLink(h8, s2)
    net.addLink(h9, s1)
    net.addLink(h10, s2)
     
    info('*** Starting network\n')
    net.build()

    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    net.get('s1').start([c0])
    net.get('s2').start([c0])

    info('*** Post configure switches and Docker containers\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()