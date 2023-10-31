from django.core.management.commands.runserver import Command as BaseCommand

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from config.constants import SOCKET_IP, SOCKET_PORT, BUFFER_SIZE
from threading import Thread
from pickle import loads, dumps

from socket_server.server import SocketServer
from pong.game import GameState
from pong_app.models import User

def handle_client(socket_server: SocketServer, client_socket: socket, game_id: str, player_id: int, player_name:str) -> None:
    try:

        # Find the client's game
        my_game = socket_server.find_player_game(game_id)

        # Send initial game state to set up player screen and board
        initial_game_state = my_game.transform_game_state(player_id, player_name)
        serialized_initial_game_state = dumps(initial_game_state)
        client_socket.sendall(serialized_initial_game_state)

        while True:
            try:
                # Receive updates from client
                received_data = client_socket.recv(BUFFER_SIZE)
                receive_game_state: GameState | None = loads(received_data)

                if not receive_game_state:
                    print("Game state not received")
                    break
                
                # Update game based on new information
                my_game.update_game(receive_game_state)

                # Send updated information back to client
                send_game_state = my_game.transform_game_state(player_id, player_name)
                serialized_game_state = dumps(send_game_state)
                client_socket.sendall(serialized_game_state)
            except Exception as e:
                print(f"Error when updating game state: {e}")
                break

    except Exception as e:
        print(f"Error when handling client: {e}")
    finally:
        client_socket.close()


def run_socket_server(socket_server_instance: SocketServer):
    try:
        server = socket(AF_INET, SOCK_STREAM)
        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server.bind((SOCKET_IP, SOCKET_PORT))
        server.listen()

        print(f"Socket server listening on {SOCKET_IP}:{SOCKET_PORT}")

        while True:
            # TODO: Authentication
            client_socket, addr = server.accept()
            player_name = client_socket.recv(BUFFER_SIZE).decode()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")

            game_id, player_id = socket_server_instance.find_or_create_game(player_name)
            thread = Thread(
                target=handle_client,
                args=(
                    socket_server_instance,
                    client_socket,
                    game_id,
                    player_id,
                    player_name
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
