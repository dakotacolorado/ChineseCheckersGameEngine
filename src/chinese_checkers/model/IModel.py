from typing import List

from ..game import Player
from ..game.ChineseCheckersGame import ChineseCheckersGame
from ..game.Move import Move


class IModel:
    """
    Interface for a model that can be used to play Chinese Checkers.
    """

    def _chose_next_move(self, current_player: Player, other_players: List[Player], moves: List[Move]) -> Move:
        """
        Chooses the next move to make.
        Args:
            current_player: current player
            other_players: other players in the game
            moves: list of possible moves for current player

        Returns:
            Next move to make.
        """
        pass

    def make_move(self, game: ChineseCheckersGame) -> ChineseCheckersGame:
        moves = game.get_next_moves()
        current_player = game.get_current_player()
        other_players = game.get_other_players()
        move = self._chose_next_move(current_player, other_players, moves)
        return game.apply_move(move)
