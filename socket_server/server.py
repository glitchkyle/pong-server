"""
Contributing Authors:	  Nishan Budathoki, James Chen, Kyle Lastimos
Email Addresses:          nishan.budhathoki@uky.edu, James.Chen@uky.edu, klastimosa001@uky.edu
Date:                     Nov 11,2023
Purpose:                  Manages the queue and active games for a socket-based multiplayer game server.
ChatGPT generated some of these comments for the function 
"""
from pong.game import Game

class SocketServer(object):
    """
    Author:       Kyle Lastimosa, James Chen
    Purpose:      Handles game session management over sockets for a multiplayer game.
    Pre:          None
    Post:         SocketServer instance is created with initialized structures for game management.
    """ 

    def __init__(self):
        """
        Author:       Kyle Lastimosa
        Purpose:      Initializes the server with structures to manage game matching and ongoing games.
        Pre:          None
        Post:         Matching queue and ongoing games dictionary are initialized.
        """ 
        # Queue for matching waiting players
        self.matching_queue: list[Game] =[]

        # Dictionary to store ongoing games
        self.ongoing_games: dict[str, Game]  = {}
    
    def enqueue(self, game: Game) -> None:
        """
        Author:       Kyle Lastimosa
        Purpose:      Adds a game to the matching queue.
        Pre:          'game' instance created and ready to be matched.
        Post:         Game is added to the queue.
        """ 
        self.matching_queue.append(game)

    def dequeue(self, player_name:str) :
        """
        Author:       Kyle Lastimosa
        Purpose:      Removes and returns a game from the queue not involving the given player.
        Pre:          Matching queue may contain games.
        Post:         If found, a game without the player is removed from the queue and returned.
        """ 
        if len(self.matching_queue) == 0: 
            return None
        
        for index, game in enumerate(self.matching_queue):
            if game.player_names[0] != player_name:
                return self.matching_queue.pop(index)
        return None
    
    def find_game_in_queue(self, game_id: str) -> Game:
        """
        Author:       Kyle Lastimosa, James Chen
        Purpose:      Finds a game in the queue by ID.
        Pre:          'game_id' must correspond to a game in the queue.
        Post:         Game object with the matching ID is returned or None if not found.
        """ 
        # TODO: Handle case when game cannot be found
        for game in self.matching_queue:
            if game.id == game_id:
                return game
    
    def find_player_game(self, game_id: str) -> Game:
        """
        Author:       Kyle Lastimosa, James Chen
        Purpose:      Retrieves an ongoing game by ID, falling back to queue search if not found.
        Pre:          'game_id' must correspond to a game in progress or in the queue.
        Post:         Game object with the matching ID is returned or None if not found.
        """ 
        if game_id in self.ongoing_games:
            return self.ongoing_games[game_id]
        else:
            return self.find_game_in_queue(game_id)

    def find_or_create_game(self, player_name: str) -> tuple[str, int]:
        """
        Author:       Kyle Lastimosa, James Chen
        Purpose:      Matches a player with an open game or creates a new game if none are open.
        Pre:          'player_name' given to match or start a new game.
        Post:         Player is either added to an existing game or a new game is created and enqueued.
        """ 
        open_game = self.dequeue(player_name)

        if open_game is not None:
            player_id = 1
            open_game.add_new_player(player_id, player_name)
            open_game.start_game()
            self.ongoing_games[open_game.id] = open_game
            return open_game.id, player_id
        else:
            player_id = 0
            game = Game()
            game.add_new_player(player_id, player_name)
            self.enqueue(game)
            return game.id, player_id

        