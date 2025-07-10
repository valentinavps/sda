import threading
import socket
import time
from opcua import Client, ua

class CLP:
    def __init__(self):
        self.opc_client = Client("opc.tcp://DESKTOP-N9PU6HL:53530/OPCUA/SimulationServer")   # Insira a URL do servidor aqui
        self.tcp_host = "localhost"
        self.tcp_port = 9000
        self.juntas = []
        self.garra = []

    def conectar_opcua(self):
        self.opc_client.connect()
        root = self.opc_client.get_objects_node()
        robo = root.get_child(["3:Franka"])
        var = robo.get_children()
        self.juntas = var[:7]
        self.garra = var[-3:]

    def opcua_loop(self):
        while True:
            pos = [g.get_value() for g in self.garra]
            print(f"[OPCUA] Posição da garra: {pos}")
            time.sleep(1)

    def tcp_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.tcp_host, self.tcp_port))
            s.listen()
            print("[TCP] Servidor aguardando conexão...")

            conn, addr = s.accept()
            with conn:
                print(f"[TCP] Conectado por {addr}")
                while True:
                    data = conn.recv(1024).decode()
                    if not data:
                        break
                    try:
                        joint_index, angle = map(float, data.split(","))
                        joint_index = int(joint_index)
                        if 0 <= joint_index < 7:
                            print(f"[TCP] Comando recebido: Junta {joint_index}, Ângulo {angle}")
                            self.juntas[joint_index].set_value(angle)
                        pos = [g.get_value() for g in self.garra]
                        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                        resposta = f"{pos[0]:.2f},{pos[1]:.2f},{pos[2]:.2f},{timestamp}\n"
                        conn.send(resposta.encode())

                        with open("historiador.txt", "a") as f:
                            f.write(f"{timestamp},Junta {joint_index},{angle},{resposta.strip()}\n")
                    except Exception as e:
                        conn.send(f"Erro: {str(e)}\n".encode())

    def iniciar(self):
        self.conectar_opcua()
        t1 = threading.Thread(target=self.opcua_loop)
        t2 = threading.Thread(target=self.tcp_server)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

if __name__ == "__main__":
    clp = CLP()
    clp.iniciar()
