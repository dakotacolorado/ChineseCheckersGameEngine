from typing import List

from ..game.ChineseCheckersGame import ChineseCheckersGame
from ..model.IModel import IModel


class GameSimulation:

    def __init__(self, models: List[IModel], board_size: int = 4, print_period: bool = 0, print_coordinates: bool = False):
        """
        Simulates a game between the given models.

        Args:
            models: models to play the game
            board_size: size of the board
            print_period: period to print the game
        """
        self.game = ChineseCheckersGame.start_game(
            number_of_players=len(models), board_size=board_size)

        self.print_period = print_period
        self.game.update_printer_settings(print_coordinates=print_coordinates)
        self._print_game()
        self.models = models
        self.games = []

    def simulate_game(self) -> ChineseCheckersGame:
        while not self.game.is_game_won():
            self.games.append(self.game)
            self.game = self.models[self.game.turn % len(self.models)].make_move(self.game)
            self._print_game()

        self.games.append(self.game)
        return self.game

    def _print_game(self):
        if self.print_period and self.game.turn % self.print_period == 0:
            self.game.print()
