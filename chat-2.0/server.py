import socket
import threading

clients = {}
nicknames = []

def broadcast(message):
    for client in clients:
        clients[client].send(message)
        
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('utf-8'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients[nickname] = client
        print(f'Nickname of client is {nickname}!')
        client.send(f'Welcome {nickname}!'.encode('utf-8'))
        broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
        client_thread = threading.Thread(target=handle, args=(client,))
        client_thread.start()


def direct_message(nickname, message):
    for client in clients:
        if nickname in clients:
            clients[nickname].send(message)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 55555))
server.listen(1)
print("Server is listening...")

receive_thread = threading.Thread(target=receive)
receive_thread.start()

while True:
    message = input('Enter message: ')
    if '@' in message:
        message = message.split(' ')
        nickname = message[0][1:]
        message = ' '.join(message[1:])
        direct_message(nickname, message)
    else:
        broadcast(message.encode('utf-8'))