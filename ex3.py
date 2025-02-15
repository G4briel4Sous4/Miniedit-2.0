from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch, Host
from mininet.cli import CLI
from mininet.log import setLogLevel

def create_topology(net):
    """Cria uma topologia de rede com 1 controladora, 4 hosts e 2 switches."""
    # Adiciona a controladora
    c0 = net.addController('c0')

    # Adiciona os switches
    s1 = net.addSwitch('s1', cls=OVSSwitch)
    s2 = net.addSwitch('s2', cls=OVSSwitch)

    # Adiciona os hosts
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1/24')
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2/24')
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3/24')
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4/24')

    # Conecta os hosts aos switches
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s2)
    net.addLink(h4, s2)

    # Conecta os switches entre si
    net.addLink(s1, s2)

    # Inicia a rede
    net.build()
    c0.start()
    s1.start([c0])
    s2.start([c0])

    # Inicia a CLI do Mininet
    CLI(net)


if __name__ == '__main__':
    setLogLevel('info')  # Define o nível de log para "info"
    net = Mininet(controller=Controller, switch=OVSSwitch, host=Host)  # Inicializa o Mininet
    create_topology(net)  # Cria a topologia