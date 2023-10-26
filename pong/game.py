from uuid import uuid1
from pygame import Rect

from config.constants import (
    DEFAULT_SCREEN_WIDTH,
    DEFAULT_SCREEN_HEIGHT,
    BALL_SIZE,
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
)
from pong.ball import Ball
from pong.paddle import Paddle

TupleRect = tuple[int, int, int, int]


class GameState(object):
    def __init__(self):
        # Read Only
        self.game_id: str
        self.player_id: int
        self.screen_size: tuple[int, int] = (
            DEFAULT_SCREEN_WIDTH,
            DEFAULT_SCREEN_HEIGHT,
        )

        # Read and Write
        self.sync = 0
        self.message: str
        self.start: bool = False
        self.scores: tuple[int, int] = (0, 0)
        self.paddle_rect: list[TupleRect | None] = [None, None]
        self.ball: TupleRect = None
        self.ball_velocity: tuple[int, int] = (0, 0)


class Game(object):
    def __init__(
        self,
        ball_size: int = BALL_SIZE,
        screen_size: tuple[int, int] = (DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT),
    ):
        self.id = str(uuid1())
        self.sync = 0
        self.start = False
        self.scores = (0, 0)

        self.screen_size: tuple[int, int] = screen_size

        screen_width, screen_height = screen_size
        rect = Rect(screen_width / 2, screen_height / 2, ball_size, ball_size)
        self.ball = Ball(rect)
        self.paddle: list[Paddle | None] = [None, None]

    def __str__(self):
        return f"Game {self.id} [Start: {self.start}] - {self.scores}"

    def start_game(self):
        if self.start:
            raise ValueError("Already started")

        self.start = True

    def add_new_player(self, player_id: int):
        if self.paddle[0] is not None and self.paddle[1] is not None:
            raise ValueError(f"Game already has reached maximum of 2 players")

        screen_width, screen_height = self.screen_size
        if player_id == 0:
            rect = Rect(
                10, (screen_height - PADDLE_HEIGHT) / 2, PADDLE_WIDTH, PADDLE_HEIGHT
            )
            self.paddle[0] = Paddle(rect)
        elif player_id == 1:
            rect = Rect(
                screen_width - 20,
                (screen_height - PADDLE_HEIGHT) / 2,
                PADDLE_WIDTH,
                PADDLE_HEIGHT,
            )
            self.paddle[1] = Paddle(rect)
        else:
            raise ValueError(f"Invalid player id {player_id}")

    def transform_game_state(self, player_id: int) -> GameState:
        game_state = GameState()

        game_state.player_id = player_id
        game_state.sync = self.sync
        game_state.game_id = self.id
        game_state.start = self.start
        game_state.scores = self.scores
        game_state.screen_size = self.screen_size

        game_state.ball = self.ball.to_tuple_rect()
        game_state.ball_velocity = self.ball.velocity

        game_state.paddle_rect = [None, None]
        game_state.paddle_rect[0] = (
            None if self.paddle[0] is None else self.paddle[0].to_tuple_rect()
        )
        game_state.paddle_rect[1] = (
            None if self.paddle[1] is None else self.paddle[1].to_tuple_rect()
        )

        return game_state

    def update_game_state(self, game_state: GameState) -> None:
        if game_state.game_id != self.id:
            raise ValueError("Invalid game being updated")

        id = game_state.player_id
        
        # Update Paddles
        if self.paddle[id] is not None and game_state.paddle_rect[id] is not None:
            x, y, w, h = game_state.paddle_rect[id]
            paddle_rect = Rect(x, y, w, h)
            self.paddle[id].update(paddle_rect)

        if game_state.start:
            # If game has started

            if game_state.sync > self.sync:
                self.sync = game_state.sync

                # Update Scores
                self.scores = game_state.scores

                # Update Ball
                x, y, w, h = game_state.ball
                ball_rect = Rect(x, y, w, h)
                self.ball.update(ball_rect, game_state.ball_velocity)