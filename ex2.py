from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch, RemoteController
from mininet.log import setLogLevel
from mininet.cli import CLI

def create_topology(net):
    """Cria uma topologia com 4 hosts, 2 switches e uma controladora."""
    
    print("*** Adicionando controladora")
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)
    
    print("*** Adicionando switches")
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    
    print("*** Adicionando hosts")
    h1 = net.addHost('h1', ip='10.0.0.1/24')  # Configura o IP com a máscara de rede
    h2 = net.addHost('h2', ip='10.0.0.2/24')
    h3 = net.addHost('h3', ip='10.0.0.3/24')
    h4 = net.addHost('h4', ip='10.0.0.4/24')
    
    print("*** Criando links")
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s2)
    net.addLink(h4, s2)
    net.addLink(s1, s2)

def myNetwork():
    net = Mininet(controller=Controller, switch=OVSSwitch)
    create_topology(net)
    
    print("\n*** Construindo a rede...")
    net.build()
    
    print("*** Iniciando controladora...")
    net.controllers[0].start()
    
    print("*** Iniciando switches...")
    for switch in net.switches:
        switch.start([net.controllers[0]])
    
    # Configura as interfaces de rede dos hosts
    print("\n*** Configurando interfaces de rede dos hosts...")
    for host in net.hosts:
        host.cmd(f"ifconfig {host.defaultIntf()} {host.IP()} up")
        print(f"{host.name}: Interface {host.defaultIntf()} configurada com IP {host.IP()}")

    # Debug: Verifica os endereços IP dos hosts
    print("\n*** Verificando endereços IP dos hosts:")
    for host in net.hosts:
        print(f"{host.name}: {host.IP()}")

    # Debug: Verifica a conectividade entre os hosts
    print("\n*** Testando conectividade entre os hosts:")
    for src in net.hosts:
        for dst in net.hosts:
            if src != dst:
                print(f"{src.name} -> {dst.name}: {src.cmd(f'ping -c 1 {dst.IP()}')}")

    # Inicia o CLI do Mininet
    print("\n*** Iniciando CLI do Mininet...")
    CLI(net)

    # Finaliza a rede ao sair do CLI
    print("\n*** Finalizando a rede...")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')  # Define o nível de log para exibir informações
    myNetwork()