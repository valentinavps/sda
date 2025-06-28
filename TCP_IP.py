import socket

def main():
    host = "localhost"
    port = 9000

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            print("Conectado ao CLP.\n")

            while True:
                try:
                    joint = input("Digite o número da junta (0-6, ou 'q' para sair): ").strip()
                    if joint.lower() == 'q':
                        print("Encerrando cliente.")
                        break

                    angle = input("Digite o ângulo desejado (-180 a 180): ").strip()
                    if angle.lower() == 'q':
                        print("Encerrando cliente.")
                        break

                    # Validação básica
                    joint_num = int(joint)
                    angle_val = float(angle)

                    if not (0 <= joint_num <= 6):
                        print("Número de junta inválido. Digite entre 0 e 6.")
                        continue
                    if not (-180 <= angle_val <= 180):
                        print("Ângulo fora do intervalo. Digite entre -180 e 180.")
                        continue

                    # Envia dados
                    s.send(f"{joint},{angle}".encode())

                    # Recebe resposta
                    data = s.recv(1024).decode().strip()

                    # Verifica se há erro ou posição inválida
                    if "None" in data or "Erro" in data:
                        print("Resposta do CLP: Erro na leitura da posição.")
                    else:
                        print(f"Resposta do CLP: {data}")

                except ValueError:
                    print("Entrada inválida. Certifique-se de digitar números válidos.")

    except ConnectionRefusedError:
        print("Erro: Não foi possível conectar ao CLP. Verifique se o servidor está ativo.")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()
