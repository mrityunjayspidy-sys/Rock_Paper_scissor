import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ai.rps_ai import resolve_outcome, get_beating_move, get_losing_move, move_to_index, index_to_move

def test_resolve_outcome():
    # Ties
    assert resolve_outcome("rock", "rock") == "tie"
    assert resolve_outcome("paper", "paper") == "tie"
    assert resolve_outcome("scissors", "scissors") == "tie"

    # Wins
    assert resolve_outcome("rock", "scissors") == "win"
    assert resolve_outcome("paper", "rock") == "win"
    assert resolve_outcome("scissors", "paper") == "win"

    # Losses
    assert resolve_outcome("rock", "paper") == "lose"
    assert resolve_outcome("paper", "scissors") == "lose"
    assert resolve_outcome("scissors", "rock") == "lose"

def test_counter_moves():
    assert get_beating_move("rock") == "paper"
    assert get_beating_move("paper") == "scissors"
    assert get_beating_move("scissors") == "rock"

    assert get_losing_move("rock") == "scissors"
    assert get_losing_move("paper") == "rock"
    assert get_losing_move("scissors") == "paper"

def test_move_indexing():
    assert move_to_index("rock") == 0
    assert move_to_index("paper") == 1
    assert move_to_index("scissors") == 2

    assert index_to_move(0) == "rock"
    assert index_to_move(1) == "paper"
    assert index_to_move(2) == "scissors"
    assert index_to_move(3) == "rock"
