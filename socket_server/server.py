from uuid import uuid4

from pong.game import Game

class SocketServer(object):

    def __init__(self):
        # Queue for matching waiting players
        self.matching_queue: list[Game] =[]

        # Dictionary to store ongoing games
        self.ongoing_games: dict[str, Game]  = {}
    
    def enqueue(self, game: Game) -> None:
        self.matching_queue.append(game)

    def dequeue(self) -> Game | None:
        if len(self.matching_queue) == 0: 
            return None
        
        return self.matching_queue.pop(0)
    
    def find_game_in_queue(self, game_id: str) -> Game:
        # TODO: Handle case when game cannot be found
        for game in self.matching_queue:
            if game.id == game_id:
                return game
    
    def find_player_game(self, game_id: str) -> Game:
        if game_id in self.ongoing_games:
            return self.ongoing_games[game_id]
        else:
            return self.find_game_in_queue(game_id)

    def find_or_create_game(self, user_id: str | None = None) -> tuple[str, int]:
        open_game = self.dequeue()

        if open_game is not None:
            player_id = 1
            open_game.add_new_player(player_id)
            open_game.start_game()
            self.ongoing_games[open_game.id] = open_game
            return open_game.id, player_id
        else:
            player_id = 0
            game = Game()
            game.add_new_player(player_id)
            self.enqueue(game)
            return game.id, player_id

        