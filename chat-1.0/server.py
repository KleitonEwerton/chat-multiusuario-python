import socket
import threading

# Configuração do servidor
HOST = '127.0.0.1' # endereço IP do servidor
PORT = 65432 # porta que o servidor vai escutar

# Criação do socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ligação do socket ao endereço e porta especificados
server_socket.bind((HOST, PORT))

# Define o número máximo de conexões pendentes
server_socket.listen(5)

# Lista para armazenar os clientes conectados
clients = []

# Função para lidar com as mensagens de um cliente
def handle_client(client_socket,client_address):
    while True:
        # Recebe a mensagem do cliente
        message = client_socket.recv(1024).decode()

        # Verifica se o cliente enviou uma mensagem vazia
        if message == '':
            break
        
        # Envia a mensagem para todos os clientes conectados exceto o que enviou
        for client in clients:
            if client.getpeername()[1] != client_socket.getpeername()[1]:
                client.send(f"{client_address} diz: {message}".encode())
            # print('\nclient        : ', client.getpeername()[1], "\nclient_socket : ",client_socket.getpeername()[1])
            
    clients.remove(client_socket)
    client_socket.close()
                
# Loop principal do servidor
while True:
    # Aceita novas conexões
    client_socket, client_address = server_socket.accept()

    # Adiciona o cliente à lista de clientes conectados
    clients.append(client_socket)

    # Cria uma nova thread para lidar com as mensagens deste cliente
    client_thread = threading.Thread(target=handle_client, args=(client_socket,client_address))
    client_thread.start()

# Fecha o socket do servidor
server_socket.close()
