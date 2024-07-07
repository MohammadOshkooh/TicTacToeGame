import socket
import threading


class Peer:
    def __init__(self, port, host='127.0.0.1'):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []
        self.is_listening = False

    def connect(self, peer_port, peer_host='127.0.0.1'):
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((peer_host, peer_port))
            self.connections.append(peer_socket)
            print(f'Connected to {peer_host}:{peer_port}')
        except socket.error as error:
            print(f'Connection failed for {peer_host}:{peer_port}: {error}')

    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f'Listening on {self.host}:{self.port}')
        self.is_listening = True

        while self.is_listening:
            connection, address = self.socket.accept()
            self.connections.append(connection)
            thread = threading.Thread(target=self.handle, args=(connection, address))
            thread.start()

    def send(self, data):
        for connection in self.connections:
            try:
                connection.send(data.encode())
            except socket.error as error:
                print(f'Send failed: {error}')

    def start(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()

    def handle(self, connection, address):
        """ Handles incoming data from a connected peer."""

        while True:
            try:
                data = connection.recv(1024).decode()
                if not data:
                    break
                print(f"Received from {address}: {data}")
                self.on_receive(data)
            except socket.error as error:
                print(f'Connection error: {error}')
                break
        connection.close()

    def on_receive(self, data):
        """Processes received data. To be overridden by subclasses."""
        pass
