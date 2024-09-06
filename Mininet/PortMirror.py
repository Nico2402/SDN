from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.log import setLogLevel, info

def topology():
    # Crear la red
    net = Mininet(controller=RemoteController, switch=OVSSwitch)

    # Agregar controlador
    c0 = net.addController(name='c0',
                      controller=RemoteController,
                      ip='172.17.0.2',
                      protocol='tcp',
                      port=6633)

    # Agregar switch
    s1 = net.addSwitch('s1')

    # Agregar hosts
    hosts = []
    for i in range(1, 11):
        host = net.addHost(f'h{i}')
        net.addLink(host, s1)
        hosts.append(host)

    # Iniciar la red
    net.start()

    # Configurar el puerto espejo en el switch
    mirror_port = 11  # Suponiendo que el puerto 11 no está ocupado
    s1.cmd(f'ovs-vsctl -- set Bridge s1 mirrors=@m -- --id=@s1 get Bridge s1 '
           f'-- --id=@p1 get Port s1-eth1 '
           f'-- --id=@p11 get Port s1-eth{mirror_port} '
           f'-- --id=@m create Mirror name=m0 select-all=true output-port=@p11')

    print("Puerto espejo configurado en el switch s1 en el puerto", mirror_port)

    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([c0])
    # Iniciar la CLI para interacción

    info( '*** Post configure switches and hosts\n')
    CLI(net)

    # Detener la red
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
