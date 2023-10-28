import unittest
import numpy as np

from src.chinese_checkers.game.Position import Position
from src.chinese_checkers.game.Move import Move
from src.chinese_checkers.geometry.Hexagram import Hexagram
from src.chinese_checkers.game.Player import Player
from src.chinese_checkers.game.ChineseCheckersGame import ChineseCheckersGame
from src.chinese_checkers.simulation.GameSimulationData import GamePositions, GameMetadata, GameSimulationData


class TestGameMetadata(unittest.TestCase):

    def test_init(self):
        metadata = GameMetadata(player_count=2, board_size=4, max_game_length=10,
                                winning_player="Player1", name="TestGame", version="1.0")
        self.assertEqual(metadata.player_count, 2)
        self.assertEqual(metadata.board_size, 4)
        self.assertEqual(metadata.max_game_length, 10)
        self.assertEqual(metadata.winning_player, "Player1")
        self.assertEqual(metadata.name, "TestGame")
        self.assertEqual(metadata.version, "1.0")


class TestGamePositions(unittest.TestCase):

    def setUp(self):
        self.game_positions = GamePositions(
            player_ids=["P1", "P2"],
            player_start_positions=[[(0, 1), (0, 2)], [(2, 3), (2, 4)]],
            player_target_positions=[[(1, 2), (1, 3)], [(3, 4), (3, 5)]],
            historical_moves=[((0, 1), (1, 2)), ((2, 3), (3, 4))]
        )

    def test_to_storable(self):
        storable = GamePositions.to_storable(self.game_positions)
        self.assertTrue(isinstance(storable["player_ids"], np.ndarray))
        self.assertTrue(isinstance(storable["player_start_positions"], np.ndarray))
        self.assertTrue(isinstance(storable["player_target_positions"], np.ndarray))
        self.assertTrue(isinstance(storable["historical_moves"], np.ndarray))

    def test_from_storable(self):
        storable = GamePositions.to_storable(self.game_positions)
        restored = GamePositions.from_storable(storable)
        self.assertEqual(restored, self.game_positions)


class TestGameSimulationData(unittest.TestCase):

    def setUp(self):
        self.metadata = GameMetadata(player_count=2, board_size=4, max_game_length=10,
                                     winning_player="Player1", name="TestGame", version="1.0")
        self.game_positions = GamePositions(
            player_ids=["P1", "P2"],
            player_start_positions=[[Position(0, 1), Position(0, 2)], [Position(2, 3), Position(2, 4)]],
            player_target_positions=[[Position(1, 2), Position(1, 3)], [Position(3, 4), Position(3, 5)]],
            historical_moves=[Move(0, 1, Position(1, 2)), Move(2, 3, Position(3, 4))]
        )
        self.simulation_data = GameSimulationData(metadata=self.metadata, positions=self.game_positions)

    def test_init(self):
        self.assertEqual(self.simulation_data.metadata, self.metadata)
        self.assertEqual(self.simulation_data.positions, self.game_positions)

    def test_to_game_sequence(self):
        game_sequence = GameSimulationData.to_game_sequence(self.simulation_data)

        self.assertEqual(len(game_sequence), len(self.game_positions.historical_moves) + 1)
        expected_players = [
            Player(start_positions, target_positions, player_id)
            for player_id, start_positions, target_positions
            in zip(self.simulation_data.positions.player_ids,
                   self.simulation_data.positions.player_start_positions,
                   self.simulation_data.positions.player_target_positions)
        ]

        initial_game = ChineseCheckersGame(
            expected_players, board=Hexagram(self.simulation_data.metadata.board_size))

        self.assertEqual(game_sequence[0], initial_game)

        current_game = initial_game
        for idx, move in enumerate(self.game_positions.historical_moves):
            current_game = current_game.apply_move(move)
            self.assertEqual(game_sequence[idx + 1], current_game)
