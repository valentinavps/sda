import time
import numpy as np
from opcua import Client
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

# Declaração global para sim ser usado dentro da função move_joint_smoothly
sim = None

########################################################################
# Função para interpolação linear entre a posição atual e a posição alvo
########################################################################
def move_joint_smoothly(handle, target_position):
    move_time = 1.0
    steps = 50
    delta_time = move_time / steps
    current_position = sim.getJointPosition(handle)
    step_size = (target_position - current_position) / steps

    for step in range(steps):
        new_position = current_position + step_size * (step + 1)
        sim.setJointTargetPosition(handle, new_position)
        time.sleep(delta_time)

########################################################################
# Inicia conexão com servidor OPC UA
########################################################################
def initOPC():
    client = Client("opc.tcp://DESKTOP-N9PU6HL:53530/OPCUA/SimulationServer")
    client.connect()
    servers = client.find_servers()

    for server in servers:
        print("-----------------------------")
        print("Server URI:", server.ApplicationUri)
        print("Server ProductURI:", server.ProductUri)
        print("Discovery URLs:", server.DiscoveryUrls)
        print("-----------------------------")
        
    root = client.get_objects_node()
    robo = root.get_child(["3:Franka"])
    var = robo.get_children()
    juntas = var[:7]
    garra = var[-3:]

    print("Descobrindo juntas do robo:")
    for j in juntas:
        name = j.get_browse_name().Name
        value = j.get_value()
        print(f"{name} = {value}")
        
    print("Descobrindo coordenadas da garra:")
    for p in garra:
        name = p.get_browse_name().Name
        value = p.get_value()
        print(f"{name} = {value}")
        
    return juntas, garra

########################################################################
# Inicializa CoppeliaSim
########################################################################
def initCoppelia():
    client = RemoteAPIClient()
    sim_local = client.getObject('sim')
    sim_local.startSimulation()
    time.sleep(1)
    joint_names = [f'link{i+2}_resp' for i in range(6)]
    joint_handles = [sim_local.getObject('/Franka/' + name + '/joint') for name in joint_names]
    return sim_local, joint_handles

########################################################################
# Espera até que todas as juntas estejam com valor válido
########################################################################
def esperar_juntas_validas(juntas):
    print("Aguardando valores válidos das juntas...")
    while True:
        valores = [j.get_value() for j in juntas]
        if all(v is not None for v in valores):
            return valores
        time.sleep(0.1)

########################################################################
# Main
########################################################################
# Inicializa cliente OPC e simulador
juntas, garra = initOPC()
sim, joint_handles = initCoppelia()

# Loop principal
for _ in range(2000):
    valores_juntas = esperar_juntas_validas(juntas)

    # Converte para radianos com fallback seguro
    target_positions = []
    for v in valores_juntas:
        if v is None:
            target_positions.append(0.0)
        else:
            rad = np.deg2rad(v)
            rad = np.clip(rad, -np.pi, np.pi)
            target_positions.append(rad)

    # Move as juntas
    for h, pos in zip(joint_handles, target_positions):
        move_joint_smoothly(h, pos)

    # Lê e envia a posição da garra
    position = sim.getObjectPosition(joint_handles[-1], -1)
    for i, p in enumerate(garra):
        p.set_value(position[i])

    time.sleep(0.1)

# Finaliza simulação
sim.stopSimulation()
