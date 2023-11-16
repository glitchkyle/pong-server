"""
Contributing Authors:	  Nishan Budathoki, James Chen, Kyle Lastimos
Email Addresses:          nishan.budhathoki@uky.edu, James.Chen@uky.edu, klastimosa001@uky.edu
Date:                     Nov 11,2023
Purpose:                  Game logic for managing Pong game state, including ball, paddles, and player actions.
"""
from uuid import uuid1
from pygame import Rect

from config.constants import (
    DEFAULT_SCREEN_WIDTH,
    DEFAULT_SCREEN_HEIGHT,
    BALL_SIZE,
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
    MAX_SCORE
)
from pong.ball import Ball
from pong.paddle import Paddle

from pong_app.models import User

TupleRect = tuple[int, int, int, int]

class GameState(object):
    """
    Author:       Kyle Lastimosa, James Chen
    Purpose:      To hold the player information, scores, and the status of the game such as paddles and ball. 
    Pre:          GameState is instantiated when a new game is created or when an existing game's state needs to be captured.
    Post:         An object with a snapshot of the game's current state is created.
    """ 
    def __init__(self):
        """
        Author:       Kyle Lastimosa
        Purpose:      To initialize the game state with default settings for a new or reset game. 
        Pre:          Called when a new game session is started.
        Post:         A GameState instance is created with default values for game settings and state.
        """ 
        # Read Only
        self.game_id: str
        self.player_id: int
        self.player_name: str
        self.screen_size: tuple[int, int] = (
            DEFAULT_SCREEN_WIDTH,
            DEFAULT_SCREEN_HEIGHT,
        )

        # Read and Write
        self.sync = 0
        self.start: bool = False
        self.scores: tuple[int, int] = (0, 0)
        self.paddle_rect: list[TupleRect | None] = [None, None]
        self.ball: TupleRect = None
        self.ball_velocity: tuple[int, int] = (0, 0)
        self.again: list[bool] = [False, False]

class Game(object):
    """
    Author:       Kyle Lastimosa
    Purpose:      Managing the game's players, ball, scores, and the state of the game.
    Pre:          Game is initiated when players are ready to start a new pong match.
    Post:         A new game instance is created with initialized players, ball, and scorekeeping.
    """ 
    def __init__(
        self,
        ball_size: int = BALL_SIZE,
        screen_size: tuple[int, int] = (DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT),
    ):
        """
        Author:       Kyle Lastimosa, James Chen
        Purpose:      Initializes the game with settings for ball and screen size.
        Pre:          Instantiation of a new game.
        Post:         Game instance created with unique ID and initial settings.
        """ 
        self.id = str(uuid1())
        self.player_names: list[str | None] = [None, None]
        self.sync = 0
        self.start = False
        self.scores = (0, 0)

        self.screen_size: tuple[int, int] = screen_size

        screen_width, screen_height = screen_size
        ball_rect = Rect(screen_width / 2, screen_height / 2, ball_size, ball_size)
        self.ball = Ball(ball_rect)
        self.paddle: list[Paddle | None] = [None, None]
        self.again: list[bool] = [False, False]

    def __str__(self):
        """
        Author:       Kyle Lastimosa, James Chen
        Purpose:      Provides a string summary of the game's state.
        Pre:          Game object exists.
        Post:         String with game ID, start status, and scores returned.
        """ 
        return f"Game {self.id} [Start: {self.start}] - {self.scores}"
    
    def start_game(self):
        """
        Author:       Kyle Lastimosa
        Purpose:      To begin the game, resetting scores and positions to their starting state.
        Pre:          Game instance must be created and players should be ready to start.
        Post:         The game starts with the ball reset to the center and scores set to zero.
        """ 
        if self.start:
            return
        self.start = True
        self.scores = (0, 0)
        self.ball.reset()

        # Helps prompt users if they want to play again
        self.again = [False, False]

    def end_game(self):
        """
        Author:       Kyle Lastimosa, James Chen
        Purpose:      To end the current game, record the final scores, and determine the winner and loser.
        Pre:          The game must have started and a win condition must be met.
        Post:         The game is ended, the winner's and loser's records are updated.
        """ 
        if not self.start:
            return
        self.start = False

        # Record points
        winner_username, loser_username = self.get_winner_and_loser_username()

        winner = User.objects.get(username=winner_username)
        loser = User.objects.get(username=loser_username)

        winner.wins += 1

        winner.games += 1
        loser.games += 1

        winner.save()
        loser.save()

    def add_new_player(self, player_id: int, player_name: str):
        """
        Author:       Kyle Lastimosa, James Chen, Nishan Budhathoki
        Purpose:      To add a new player to the game with a specified player ID and name.
        Pre:          There must be an available slot in the game.
        Post:         A new player is added to the game.
        """ 
        if self.paddle[0] is not None and self.paddle[1] is not None:
            raise ValueError(f"Game already has reached maximum of 2 players")

        screen_width, screen_height = self.screen_size
        if player_id == 0:
            rect = Rect(
                10, (screen_height - PADDLE_HEIGHT) / 2, PADDLE_WIDTH, PADDLE_HEIGHT
            )
            self.paddle[0] = Paddle(rect)
            self.player_names[0] = player_name
        elif player_id == 1:
            rect = Rect(
                screen_width - 20,
                (screen_height - PADDLE_HEIGHT) / 2,
                PADDLE_WIDTH,
                PADDLE_HEIGHT,
            )
            self.paddle[1] = Paddle(rect)
            self.player_names[1] = player_name
        else:
            raise ValueError(f"Invalid player id {player_id}")

    def transform_game_state(self, player_id: int, player_name) -> GameState:
        """
        Author:       Kyle Lastimosa, James Chen
        Purpose:      To create a GameState object representing the current state of the game from the perspective of a given player.
        Pre:          The game must be initialized and contain the current states of game.
        Post:         A GameState object is returned with information about the specified player.
        """ 
        game_state = GameState()

        game_state.player_id = player_id
        game_state.player_name = player_name
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
        game_state.again = self.again

        return game_state

    def is_game_finished(self) -> bool:
        """
        Author:       Kyle Lastimosa
        Purpose:      To check if the game has reached a win condition based on scores.
        Pre:          The game must be in progress with scores being tracked.
        Post:         Returns True if a win condition is met, otherwise false.
        """ 
        return self.scores[0] == MAX_SCORE or self.scores[1] == MAX_SCORE
    
    def get_winner_and_loser_username(self) -> str:
        """
        Author:       Kyle Lastimosa
        Purpose:      To determine the winner and loser of the game based on the current scores.
        Pre:          The game should have ended with a clear win condition.
        Post:         Returns the usernames of the winner and loser.
        """ 
        if self.scores[0] > self.scores[1]:
            return self.player_names[0], self.player_names[1]
        elif self.scores[0] < self.scores[1]:
            return self.player_names[1], self.player_names[0]
    
    def are_players_playing_again(self) -> bool:
        """
        Author:       Kyle Lastimosa
        Purpose:      To check if both players have indicated to play another game.
        Pre:          The game has ended and players are prompted to play again.
        Post:         Returns True if both players want to play again, otherwise false.
        """ 
        return self.again == [True, True]
    
    def update_game(self, game_state: GameState) -> None:
        """
        Author:       Kyle Lastimosa
        Purpose:      To update the game state with a new GameState object, reflecting any changes made by the players.
        Pre:          The game must be initialized and a valid GameState object must be provided.
        Post:         The game's state is updated to reflect the changes provided by the GameState object, including scores and positions of game.
        """ 
        if game_state.game_id != self.id:
            raise ValueError("Invalid game being updated")

        id = game_state.player_id

        # Update paddles regardless of game state
        if self.paddle[id] is not None and game_state.paddle_rect[id] is not None:
            x, y, w, h = game_state.paddle_rect[id]
            paddle_rect = Rect(x, y, w, h)
            self.paddle[id].update(paddle_rect)

        # Check game state
        if game_state.start:
            # Game has started with two players ready to play
            if game_state.sync > self.sync:
                self.sync = game_state.sync
                self.scores = game_state.scores

                # Update Ball
                x, y, w, h = game_state.ball
                ball_rect = Rect(x, y, w, h)
                self.ball.update(ball_rect, game_state.ball_velocity)

            if self.is_game_finished():
                self.end_game()
        else:
            # Update player who wants to play again
            self.again[id] = game_state.again[id]

            # If game is awaiting opponent or game has ended
            if self.are_players_playing_again():
                self.start_game()