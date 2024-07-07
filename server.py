import socket
import threading

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.uniquename = []

    def broadcast_message(self, message, sender_client):
        for client in self.clients:
            if client != sender_client:
                try:
                    client.send(message.encode('ascii'))
                except:
                    client.close()
                    self.remove_client(client)

    def remove_client(self, client):
        index = self.clients.index(client)
        uniquename = self.uniquename[index]
        self.clients.remove(client)
        self.uniquename.remove(uniquename)
        self.broadcast_message(f'{uniquename} left the chat', client)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024).decode('ascii')
                if message:
                    self.broadcast_message(message, client)
            except ConnectionResetError:
                self.remove_client(client)
                break

    def receive_clients(self):
        while True:
            client, address = self.server.accept()
            print(f'Connected with {str(address)}')

            client.send('NICK'.encode('ascii'))
            uniquename = client.recv(1024).decode('ascii')
            self.uniquename.append(uniquename)
            self.clients.append(client)

            print(f'The name of the client is {uniquename}!')
            self.broadcast_message(f'{uniquename} joined the chat', client)
            client.send('Connected to the server!'.encode('ascii'))

            thread = threading.Thread(target=self.handle, args=(client,), name=f'ClientThread-{uniquename}')
            thread.start()

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        print('Server is listening...')
        self.receive_clients()

if __name__ == "__main__":
    server = ChatServer('127.0.0.1', 5505)
    server.start()
