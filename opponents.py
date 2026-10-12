"""
Root-level re-export for Opponents suite.
"""
from src.ai.opponents import (
    RandomAgent,
    WinStayLoseShiftOpponent,
    CyclicOpponent,
    CopierOpponent,
    BiasedOpponent,
    FixedMoveOpponent,
)

__all__ = [
    "RandomAgent",
    "WinStayLoseShiftOpponent",
    "CyclicOpponent",
    "CopierOpponent",
    "BiasedOpponent",
    "FixedMoveOpponent",
]
