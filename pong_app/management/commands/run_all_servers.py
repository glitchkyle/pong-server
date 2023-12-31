"""
Contributing Authors:	  Nishan Budathoki, James Chen, Kyle Lastimos
Email Addresses:          nishan.budhathoki@uky.edu, James.Chen@uky.edu, klastimosa001@uky.edu
Date:                     Nov 11,2023
Purpose:                  initialize and manage a secure socket server for a multiplayer pong game 
ChatGPT generated some of these comments for the function
"""
from django.core.management.commands.runserver import Command as BaseCommand

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from config.constants import SOCKET_IP, SOCKET_PORT, BUFFER_SIZE
from threading import Thread
from pickle import loads, dumps

from socket_server.server import SocketServer
from pong.game import GameState
import ssl
from pong_app.views import authenticationUser,register_user

def handle_client(socket_server: SocketServer, client_socket: ssl.SSLSocket, game_id: str, player_id: int, player_name: str) -> None:
    try:
        # Find the client's game
        my_game = socket_server.find_player_game(game_id)

        # Send initial game state to set up player screen and board
        initial_game_state = my_game.transform_game_state(player_id, player_name)
        serialized_initial_game_state = dumps(initial_game_state)
        client_socket.sendall(serialized_initial_game_state)

        while True:
            # Receive updates from client
            received_data = client_socket.recv(BUFFER_SIZE)
            receive_game_state: GameState | None = loads(received_data)

            if not receive_game_state:
                raise ValueError("Game state not received")
            
            # Update game based on new information
            my_game.update_game(receive_game_state)

            # Send updated information back to client
            send_game_state = my_game.transform_game_state(player_id, player_name)
            serialized_game_state = dumps(send_game_state)
            client_socket.sendall(serialized_game_state)

    except Exception as e:
        # TODO: Remove player from queue or game stack
        print(f"Error when handling client: {e}")
    finally:
        client_socket.close()


def run_socket_server(socket_server_instance: SocketServer):
    server = socket(AF_INET, SOCK_STREAM)
    try:
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

        # Load the server's certificate and private key signed by the CA
        context.load_cert_chain(certfile="./server.crt", keyfile="./server.key")

        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server.bind((SOCKET_IP, SOCKET_PORT))
        server.listen()

        print(f"Socket server listening on {SOCKET_IP}:{SOCKET_PORT}")

        while True:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")

            ssock = context.wrap_socket(client_socket, server_side=True)
            player_credentials = ssock.recv(BUFFER_SIZE)
            player = loads(player_credentials)

            # TODO: Fix pls
            if ('confirm_password' in player and register_user(player)) or authenticationUser(player):
                ssock.sendall(b"Success")
            else:
                ssock.sendall(b"Authentication failed")
                ssock.close()
                continue

            game_id, player_id = socket_server_instance.find_or_create_game(player['username'])

            thread = Thread(
                target=handle_client,
                args=(
                    socket_server_instance,
                    ssock,
                    game_id,
                    player_id,
                    player['username']
                ),
            )
            thread.start()
    except Exception as e:
        print(f"Server Error: {e}")
    finally:
        server.close()


class Command(BaseCommand):
    help = 'Initializes Django server and Pong socket server'

    def handle(self, *args, **options):
        print("Initializing socket server")
        socket_server = SocketServer()
        socket_thread = Thread(target=run_socket_server, args=(socket_server,))
        socket_thread.start()

        print("Initializing Django server")
        super().handle(*args, **options)
