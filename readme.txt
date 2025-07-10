Trabalho Prático Final de SDA
Controle de um Manipulador Robótico via Integração com Servidor OPC UA
Alunos: Pedro Ribeiro Rodrigues Lourenço e Valentina Perpetuo dos Santos


1 - Pré requisitos:

- Dependências:
    - numpy
    - opcua
    - coppeliasim_zmqremoteapi_client

- Servidor OPC UA com as variáveis:
    - Junta1
    - Junta2
    - Junta3
    - Junta4
    - Junta5
    - Junta6
    - Junta7
    - Px
    - Py
    - Pz

- Software coppeliaSim e o arquivo fornecido "robo.ttt"

2 - Instruções para execução:

    - Abra o arquivo "robo.ttt" e inicie a simulação
    - Inicie o servidor OPC UA
    - Copie a URL fornecida pelo servidor e a insira nos locais indicados nos arquivos "MES.py", "brigde.py" e "CLP.py"
    - Abra 4 terminais diferentes
    - Execute "brigde.py"
    - Execute "CLP.py"
    - Execute "TCP_IP.py"
    - Execute "MES.py"
    - No terminal referente ao arquivo "TCP_IP.py" siga as instruções exibidas no terminal para inserir valores válidos das juntas e dos ângulos
    - Observe a movimentação do robo pelo programa coppeliaSim
    - Ao encerrar a execução observe os registros nos arquivos "historiador.txt" e "mes.txt"
