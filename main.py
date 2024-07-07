import hashlib
import socket
from time import sleep

from game import TicTacToe

if __name__ == "__main__":

    port = int(input("Enter your port: "))
    is_login = False

    username = None
    password = None
    client_socket = None

    while not is_login:
        command = input("Select one 1.REGISTER 2.LOGIN 3.EXIT: ")

        if command == '1' or command == '2':
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                client_socket.connect(('127.0.0.1', 12345))
            except:
                print('Connection to server failed.')

            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            message = f"{command} {username} {hashed_password}"

            client_socket.send(message.encode())

            response = client_socket.recv(1024).decode()
            print(f"Server response: {response}")

            if response in ['REGISTER SUCCESS', 'LOGIN SUCCESS']:
                is_login = True

    client_socket.send("3".encode())
    connections = client_socket.recv(1024).decode()
    print(f"Online Users: {connections}")

    # to_user = input("Enter the username you want to connect to: or enter 1.WAIT 2.Exit: ")
    to_user = input("Enter the username you want to connect to: ")
    while is_login:
        # if to_user == '1':
        #     pass
        # elif to_user == '2':
        #     is_login = False
        # else:
        request_message = f"4 {username} {to_user}"
        client_socket.send(request_message.encode())

        response = client_socket.recv(1024).decode()
        print(response)
        if response.startswith("REQUEST"):
            print(response)
            accept = input("Do you accept the connection? (yes/no): ")
            if accept.lower() == "yes":
                response_message = f"5 ACCEPT {username} {to_user}"
            else:
                response_message = f"5 REJECT {username} {to_user}"
            client_socket.send(response_message.encode())

        response = client_socket.recv(1024).decode()
        if response.startswith("ACCEPT"):
            print(f"Connection accepted by {to_user}")
            # Start the game
            game = TicTacToe(port)
            game.start()
            client_socket.send("3".encode())

            peer_port = int(input("Enter peer port to connect: "))
            game.connect(peer_port)
            game.start_game()

            sleep(1)

            client_socket.send("3".encode())
            connections = client_socket.recv(1024).decode()
            print(f"Online Users: {connections}")
            to_user = input("Enter the username you want to connect to: ")

        elif response.startswith("REJECT"):
            print(f"Connection rejected by {to_user}")

    client_socket.close()
