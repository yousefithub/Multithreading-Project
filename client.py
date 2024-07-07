import socket
import threading

class ChatClient:
    def __init__(self, host, port):
        self.uniquename = input("Enter your UniqueName: ")
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('ascii')
                if not message:
                    print("Server closed the connection.")
                    self.client.close()
                    break
                elif message == 'NICK':
                    self.client.send(self.uniquename.encode('ascii'))
                else:
                    print(message)
            except ConnectionResetError:
                print("Connection with the server was reset.")
                self.client.close()
                break

    def write(self):
        while True:
            try:
                message = f'{self.uniquename}: {input("")}'
                self.client.send(message.encode('ascii'))
            except (ConnectionResetError, BrokenPipeError):
                print("Connection with the server was reset.")
                self.client.close()
                break

    def start(self):
        try:
            self.client.connect((self.host, self.port))
            receive_thread = threading.Thread(target=self.receive, name='ReceiveThread')
            receive_thread.start()

            write_thread = threading.Thread(target=self.write, name='WriteThread')
            write_thread.start()
        except ConnectionRefusedError:
            print("Connection refused. Make sure the server is running.")

if __name__ == "__main__":
    client = ChatClient('127.0.0.1', 5505)
    client.start()
