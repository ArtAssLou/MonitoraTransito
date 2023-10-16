import socket
import json


# Configurações do servidor e porta
hosta = '164.41.98.29'  # ip da placa 7
#hosta = ''
host = hosta
port = 10761  # Insira a porta à qual deseja se conectar



# Cria um objeto socket
def servidor():
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    servidor_socket.connect((host, port))
    servidor_socket.listen(5)
    print(f"Servidor funcionando {host}")
    while True:
        client_socket, client_address = servidor_socket.accept()
        print(f"Conexeão estabelecida com {client_address}")
        recebe_dados(client_socket)




def recebe_dados(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        data_recebida = json.loads(data.decode('utf-8'))

        if data_recebida['type'] == 'controlar_velocidade':

            global carro
            print ("Os carros a cima da velocidade são:")
            for carro in data_recebida['data']['CarroVA']:
                print (carro)
            print ("A velocidade dos carros nas vias são:")
            for carro in data_recebida['data']['CarroVN']:
                print (carro)
            print ("Os carros que passaram o sinal vermelho são:")
            for carro in data_recebida['data']['SinalVermelho']:
                print (carro)

        client_socket.close()
 
            
