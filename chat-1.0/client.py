import socket
import threading

# Configuração dos clientes
HOST = '127.0.0.1' # endereço IP do servidor
PORT = 65432 # porta do servidor

def send_message(client_socket):
    while True:
        # Lê a mensagem do usuário
        message = input("Digite sua mensagem: ")

        # Envia a mensagem para o servidor
        client_socket.send(message.encode())

def receive_message(client_socket,client_id):
    while True:
        # Recebe a resposta do servidor
        response = client_socket.recv(1024).decode()
        #split the response to get the sender's id
        sender_id = response.split(" ")[0]
        if sender_id != client_id:
            # Imprime a resposta do servidor
            print(response)

# Criação dos sockets
client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ligação dos sockets ao endereço e porta especificados
client_socket1.connect((HOST, PORT))
client_socket2.connect((HOST, PORT))

# Cria threads para lidar com as mensagens de cada cliente
send_thread1 = threading.Thread(target=send_message, args=(client_socket1,))
receive_thread1 = threading.Thread(target=receive_message, args=(client_socket1,"client1",))
send_thread2 = threading.Thread(target=send_message, args=(client_socket2,))
receive_thread2 = threading.Thread(target=receive_message, args=(client_socket2,"client2",))

# Inicia as threads
send_thread1.start()
receive_thread1.start()
send_thread2.start()
receive_thread2.start()
