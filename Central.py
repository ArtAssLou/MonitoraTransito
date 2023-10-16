import socket
import json

# Cria um objeto socket
def servidor():
    # Configurações do servidor e porta
    #hosta = '164.41.98.29'  # ip da placa 7
    hosta = '164.41.98.28' # ip placa 6
    host = hosta
    port = 10770  # Insira a porta à qual deseja se conectar
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    servidor_socket.bind((host, port))
    servidor_socket.listen(5)
    print(f"Servidor funcionando {host}")
    while True:
        client_socket, client_address = servidor_socket.accept()
        print(f"Conexão estabelecida com {client_address}")
        recebe_dados(client_socket)
        client_socket.close()

def recebe_dados(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            return

        data_recebida = json.loads(data.decode('utf-8'))

        if data_recebida['type'] == 'controlar_velocidade':
            dados = json.loads(data_recebida['data'])

            print("Os carros a cima da velocidade são:")
            for carro in dados['CarroVA']:
                print(carro)
            print("A velocidade dos carros nas vias são:")
            for carro in dados['CarroVN']:
                print(carro)
            print("Os carros que passaram o sinal vermelho são:")
            for carro in dados['SinalVermelho']:
                print(carro)

        response_data = json.dumps({"type": "ok"}).encode('utf-8')
        client_socket.send(response_data)

if __name__ == "__main__":
    servidor()
