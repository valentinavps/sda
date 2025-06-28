from opcua import Client
import time

client = Client("opc.tcp://Valentina:53530/OPCUA/SimulationServer")
client.connect()

robo = client.get_objects_node().get_child(["3:Franka"])
garra = robo.get_children()[-3:]

def safe_format(value):
    return f"{value:.2f}" if value is not None else "NaN"
with open("mes.txt", "a") as f:

    while True:
        pos = [g.get_value() for g in garra]
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"{timestamp},{safe_format(pos[0])},{safe_format(pos[1])},{safe_format(pos[2])}\n")
        f.flush()
        print(f"[MES] {timestamp} -> {pos}")
        time.sleep(2)
