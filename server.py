import socket
import threading
import json
from db_manager import DBManager


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.user_manager = DBManager()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []
        self.is_listening = False

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f'Server is listening on {self.host}:{self.port}')
        self.is_listening = True

        while self.is_listening:
            connection, address = self.socket.accept()
            self.connections.append({'connection': connection, 'address': address})
            thread = threading.Thread(target=self.handle_client, args=(connection, address))
            thread.start()

    def handle_client(self, client_socket, address):
        while True:
            # try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(f"Received data from {address}: {data}")

            parts = data.split()
            if parts[0] == '1':  # register
                username = parts[1]
                password = parts[2]
                if self.user_manager.register(username, password):
                    client_socket.send('REGISTER SUCCESS'.encode())
                    self.user_manager.add_connection(address, username)
                else:
                    client_socket.send('REGISTER FAIL. TRY AGAIN'.encode())
            elif parts[0] == '2':  # login
                username = parts[1]
                password = parts[2]
                if self.user_manager.login(username, password):
                    client_socket.send('LOGIN SUCCESS'.encode())
                    self.user_manager.add_connection(address, username)
                else:
                    client_socket.send('LOGIN FAIL. TRY AGAIN'.encode())
            elif parts[0] == '3':  # get connections
                connections = json.dumps(self.user_manager.get_online_users())
                client_socket.send(connections.encode())
            elif parts[0] == '4':  # request connection
                print(parts)
                from_user = parts[1]
                to_user = parts[2]
                self.handle_connection_request(client_socket, from_user, to_user)
            elif parts[0] == '5':  # response to connection request
                response = parts[1]
                from_user = parts[2]
                to_user = parts[3]
                self.handle_connection_response(response, from_user, to_user)
            elif parts[0] == '6':
                username = parts[1]
                client_socket.send(str(self.user_manager.get_user_port(username)).encode())
            else:
                client_socket.send('INVALID COMMAND'.encode())

        # except Exception as e:
        #     print(f"Exception: {e}")
        #     break

        client_socket.close()

    def handle_connection_request(self, client_socket, from_user, to_user):
        """Handles a connection request from one user to another."""

        found = False
        for obj in self.connections:
            if obj["address"] == self.get_user_address(to_user):
                obj["connection"].send(f"REQUEST {from_user} wants to connect with you".encode())
                found = True
                break

        if not found:
            client_socket.send(f"User {to_user} not found or offline".encode())

    def handle_connection_response(self, response, from_user, to_user):
        """Handles the response to a connection request."""
        print(response)
        found = False
        for obj in self.connections:
            if obj["address"] == self.get_user_address(to_user):
                obj["connection"].send(f"{response} {from_user} {to_user}".encode())
                found = True
                break

        if not found:
            print(f"User {to_user} not found or offline")

    def get_user_address(self, username):
        for conn in self.user_manager.get_online_users():
            if conn["username"] == username:
                return conn["address"]
        return None

    def stop(self):
        self.is_listening = False
        self.socket.close()


if __name__ == "__main__":
    server = Server('127.0.0.1', 12345)

    server_thread = threading.Thread(target=server.start)
    server_thread.start()
