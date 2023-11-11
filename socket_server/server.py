from pong.game import Game

class SocketServer(object):

    def __init__(self):
        # Queue for matching waiting players
        self.matching_queue: list[Game] =[]

        # Dictionary to store ongoing games
        self.ongoing_games: dict[str, Game]  = {}
    
    def enqueue(self, game: Game) -> None:
        self.matching_queue.append(game)

    def dequeue(self, player_name:str) :
        if len(self.matching_queue) == 0: 
            return None
        
        for index, game in enumerate(self.matching_queue):
            if game.player_names[0] != player_name:
                return self.matching_queue.pop(index)
        return None
    
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

    def find_or_create_game(self, player_name: str) -> tuple[str, int]:
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

        