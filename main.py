# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
from pickle import loads, dumps

from config.constants import SERVER_IP, SERVER_PORT, BUFFER_SIZE

from pong.game import Game, GameState

# Queue for available games
open_games: list[Game] = []

# Current ongoing games with two players
ongoing_games: dict[str, Game] = {}

def handle_client(client_socket: socket, addr, game_id: str, player_id: int) -> None:
    try:

        # Find the client's game
        if game_id in ongoing_games:
            # Opponent found
            my_game = ongoing_games[game_id]
        else:
            # Waiting for opponent
            my_game = find_game(game_id)

        # Send initial game state to set up player screen and board
        initial_game_state = my_game.transform_game_state(player_id)

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

                my_game.update_game_state(receive_game_state)

                # Send updated information back to client
                send_game_state = my_game.transform_game_state(player_id)
                serialized_game_state = dumps(send_game_state)
                client_socket.sendall(serialized_game_state)
            except Exception as e:
                print(f"Error when updating game state: {e}")
                break

    except Exception as e:
        print(f"Error when handling client: {e}")
    finally:
        client_socket.close()

def find_game(game_id: str) -> Game:
    for game in open_games:
        if game.id == game_id:
            return game
    
def find_or_create_game() -> tuple[str, str]:
    if len(open_games) > 0:
        # If there are active games, find a game that can be joined
        open_game = open_games.pop(0)
        open_game.add_new_player(1)

        open_game.start_game()
        ongoing_games[open_game.id] = open_game
        return open_game.id, 1
    
    # Need to create a game since cannot join a game or no games available
    game = Game()
    game.add_new_player(0)
    open_games.append(game)
    return game.id, 0

def main():
    try:

        # Initialize socket server
        server = socket(AF_INET, SOCK_STREAM)
        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server.bind((SERVER_IP, SERVER_PORT))
        server.listen()
        
        print(f"Socket server listening on {SERVER_IP}:{SERVER_PORT}")

        while True:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")

            game_id, player_id = find_or_create_game()
            thread = Thread(target=handle_client, args=(client_socket, addr, game_id, player_id,))
            thread.start()

    except Exception as e:
        print(f"Server Error: {e}")
    finally:
        server.close()

if __name__ == "__main__":
    main()