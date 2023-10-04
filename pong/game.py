from uuid import uuid1
from pygame import Rect

from config.constants import DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, BALL_SIZE, PADDLE_WIDTH, PADDLE_HEIGHT
from pong.ball import Ball
from pong.paddle import Paddle

class GameState(object):
    # Read Only
    game_id: str
    player_id: str
    screen_size: tuple[int, int] = (DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)

    # Read and Write
    ball: Rect = None
    ball_velocity: tuple[int, int] = (0, 0)
    player_one_paddle_rect: Rect = None
    player_two_paddle_rect: Rect = None
    scores: tuple[int, int] = (0, 0)

class Game(object):
    def __init__(self, screen_size: tuple[int, int] = (DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)):
        self.id = str(uuid1())
        self.scores = (0, 0)

        self.screen_size: tuple[int, int] = screen_size
        screen_width, screen_height = screen_size

        self.ball = Ball(Rect(screen_width/2, screen_height/2, BALL_SIZE, BALL_SIZE))
        self.player_one_paddle = Paddle(Rect(10,(screen_height-PADDLE_HEIGHT)/2, PADDLE_WIDTH, PADDLE_HEIGHT))
        self.player_two_paddle = None
    
    def __str__(self):
        return f"{self.id}"
    
    def add_new_player(self):
        if self.player_two_paddle is not None:
            raise ValueError("Game already has two players")

        screen_width, screen_height = self.screen_size
        self.player_two_paddle = Paddle(Rect(screen_width-20,(screen_height-PADDLE_HEIGHT)/2, PADDLE_WIDTH, PADDLE_HEIGHT))
    
    def transform_game_state(self, player_id: int) -> GameState:
        game_state = GameState()

        game_state.game_id = self.id
        game_state.player_id = player_id
        game_state.scores = self.scores
        game_state.screen_size = self.screen_size

        game_state.ball = self.ball.rect
        game_state.ball_velocity = self.ball.velocity
        
        game_state.player_one_paddle_rect = self.player_one_paddle.rect

        if self.player_two_paddle is not None:
            game_state.player_two_paddle_rect = self.player_two_paddle.rect
        else:
            game_state.player_two_paddle_rect = None

        return game_state

    def update_game_state(self, game_state: GameState) -> GameState:
        if game_state.game_id != self.id:
            raise ValueError("Invalid game being updated")

        # Boolean indicating that the game started
        start = self.player_two_paddle is not None

        if start:
            # If game started, update overall game logic
            if game_state.player_id == 0:
                self.player_one_paddle.update(game_state.player_one_paddle_rect)
            else:
                self.player_two_paddle.update(game_state.player_two_paddle_rect)
        else:
            # If no opponent yet, only update first player position
            self.player_one_paddle.update(game_state.player_one_paddle_rect)