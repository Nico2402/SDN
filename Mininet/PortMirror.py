from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import OVSLink

def myNetwork():
    net = Mininet(topo=None,
                   build=False,
                   link=OVSLink,
                   ipBase='10.0.0.0/8')

    info('*** Adding controller\n')
    c0 = net.addController(name='c0',
                           controller=RemoteController,
                           ip='172.17.0.2',
                           protocol='tcp',
                           port=6633)

    info('*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, protocols=["OpenFlow13"]) # OF13

    info('*** Add hosts\n')
    h1 = net.addHost('h1', ip='10.0.0.1', defaultRoute=None)
    h2 = net.addHost('h2', ip='10.0.0.2', defaultRoute=None)
    h3 = net.addHost('h3', ip='10.0.0.3', defaultRoute=None)
    h4 = net.addHost('h4', ip='10.0.0.4', defaultRoute=None)
    h5 = net.addHost('h5', ip='10.0.0.5', defaultRoute=None)
    h6 = net.addHost('h6', ip='10.0.0.6', defaultRoute=None)
    h7 = net.addHost('h7', ip='10.0.0.7', defaultRoute=None)
    h8 = net.addHost('h8', ip='10.0.0.8', defaultRoute=None)
    h9 = net.addHost('h9', ip='10.0.0.9', defaultRoute=None)
    h10 = net.addHost('h10', ip='10.0.0.10', defaultRoute=None)
    # Agregar host adicional para el puerto espejo
    h11 = net.addHost('h11', ip='10.0.0.11', defaultRoute=None)

    info('*** Add links\n')
    for h in [h1, h2, h3, h4, h5, h6, h7, h8, h9, h10]:
        net.addLink(h, s1)
    # Conectar el host adicional al puerto que quieres usar como mirror
    net.addLink(h11, s1)
    
    info('*** Starting network\n')
    net.build()

    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    net.get('s1').start([c0])

    info('*** Configuring mirror port on switch s1\n')
    # Configuración del mirror para replicar todo el tráfico a s1-eth11
    s1.cmd('ovs-vsctl -- set Bridge s1 mirrors=@m -- --id=@p1 get port s1-eth11 -- --id=@m create Mirror name=m0 select_all=1 output_port=@p1')

    info('*** Post configure switches and hosts\n')
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()
