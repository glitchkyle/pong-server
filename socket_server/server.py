from queue import Queue
from uuid import uuid4

from pong.game import Game

class SocketServer(object):

    def __init__(self):
        # Queue for matching waiting players
        self.matching_queue = Queue()

        # Dictionary to store ongoing games
        self.ongoing_games: [str, Game]  = {}
    
    def enqueue(self, player_user_id: str) -> None:
        """
        Add a player to the matching queue
        """
        self.matching_queue.put(player_user_id)

    def dequeue_player(self) -> str | None:
        """
        Remove a player from the matching queue
        """
        if not self.matching_queue.empty():
            return self.matching_queue.get()
        else:
            return None
        
    def create_game(self, player1, player2):
        """
        Create a new game and add it to the ongoing games dictionary
        """
        game_id = str(uuid4())
        self.ongoing_games[game_id] = Game()
        return game_id
    
    def get_game_players(self, game_id: str):
        """
        Get the players of a specific game
        """
        if game_id in self.ongoing_games:
            return self.ongoing_games[game_id]
        else:
            return None
    
    def remove_game(self, game_id):
        """
        Remove a game from ongoing games
        """
        if game_id in self.ongoing_games:
            del self.ongoing_games[game_id]


        