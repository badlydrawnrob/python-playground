from contract.client import Client
import socket

HOST = '192.168.1.36'
PORT = 43210


class BerkeleySocketClient(Client):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.server.connect((HOST, PORT))

    def write(self, message):
        self.server.sendall(message)

    def read(self):
        data = self.server.recv(1024)
        return data

    def disconnect(self):
        self.server.close()


if __name__ == '__main__':
    client = BerkeleySocketClient()
    client.connect()
    client.write('Hey, this is Rob'.encode())
    print(client.read().decode())
