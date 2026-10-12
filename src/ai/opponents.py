"""
Opponents Benchmark Suite: Standard Agents and Scripted Behavioral Opponents
=============================================================================

AI Concept:
Standardized baseline suite implementing the uniform interface:
    `play(history: List[str], my_history: Optional[List[str]] = None) -> str`

Includes:
1. RandomAgent: Uniform i.i.d. random baseline (Nash equilibrium).
2. WinStayLoseShiftOpponent: Heuristic psychology learner.
3. CyclicOpponent: Periodic rotating sequence generator.
4. CopierOpponent: Imitation / tit-for-tat opponent.
5. BiasedOpponent: Skewed categorical distribution opponent.
6. FixedMoveOpponent: Constant single-gesture agent.
"""

from __future__ import annotations
import random
from typing import List, Optional
from src.ai.strategy_rules import ALL_MOVES, get_beating_move, resolve_outcome


class RandomAgent:
    """Plays uniformly random moves i.i.d. (Mixed Strategy Nash Equilibrium)."""

    def __init__(self, seed: Optional[int] = None):
        self.rng = random.Random(seed)

    def play(self, history: Optional[List[str]] = None, my_history: Optional[List[str]] = None) -> str:
        return self.rng.choice(ALL_MOVES)

    def reset(self):
        pass


class WinStayLoseShiftOpponent:
    """
    Scripted opponent implementing Thorndike's Win-Stay / Lose-Shift heuristic.
    Repeats previous move on a win; shifts to beating move on a loss.
    """

    def __init__(self, shift_mode: str = "beat_loss", seed: Optional[int] = None):
        self.shift_mode = shift_mode
        self.rng = random.Random(seed)
        self.my_history: List[str] = []

    def play(self, history: Optional[List[str]] = None, my_history: Optional[List[str]] = None) -> str:
        hist = my_history if my_history is not None else self.my_history
        if not history or not hist or len(history) != len(hist):
            move = self.rng.choice(ALL_MOVES)
            self.my_history.append(move)
            return move

        last_opp = hist[-1]      # What this agent played
        last_bot = history[-1]   # What the predictor played
        outcome = resolve_outcome(last_opp, last_bot)

        if outcome == "win":
            chosen = last_opp  # Win-Stay
        elif outcome == "lose":
            if self.shift_mode == "beat_loss":
                # Shift to move that would beat what just beat them
                chosen = get_beating_move(last_bot)
            else:
                # Cycle forward
                fwd = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
                chosen = fwd[last_opp]
        else:
            # On tie, random shift
            candidates = [m for m in ALL_MOVES if m != last_opp]
            chosen = self.rng.choice(candidates)

        self.my_history.append(chosen)
        return chosen

    def reset(self):
        self.my_history.clear()


class CyclicOpponent:
    """
    Scripted opponent playing deterministic cycles (e.g. Rock -> Paper -> Scissors).
    """

    def __init__(self, cycle: Optional[List[str]] = None, offset: int = 0):
        self.cycle = cycle or ["rock", "paper", "scissors"]
        self.offset = offset
        self.step = 0

    def play(self, history: Optional[List[str]] = None, my_history: Optional[List[str]] = None) -> str:
        move = self.cycle[(self.step + self.offset) % len(self.cycle)]
        self.step += 1
        return move

    def reset(self):
        self.step = 0


class CopierOpponent:
    """
    Scripted opponent that mirrors the other player's previous move (Tit-for-Tat).
    """

    def __init__(self, mode: str = "mirror", seed: Optional[int] = None):
        self.mode = mode  # 'mirror' or 'counter'
        self.rng = random.Random(seed)

    def play(self, history: Optional[List[str]] = None, my_history: Optional[List[str]] = None) -> str:
        if not history:
            return self.rng.choice(ALL_MOVES)
        last_move = history[-1]
        if self.mode == "counter":
            return get_beating_move(last_move)
        return last_move  # Mirror

    def reset(self):
        pass


class BiasedOpponent:
    """
    Scripted opponent with fixed non-uniform probabilities, e.g. 70% Rock, 15% Paper, 15% Scissors.
    """

    def __init__(
        self,
        probabilities: Optional[Dict[str, float]] = None,
        seed: Optional[int] = None,
    ):
        self.probs = probabilities or {"rock": 0.70, "paper": 0.15, "scissors": 0.15}
        self.rng = random.Random(seed)
        self.moves = list(self.probs.keys())
        self.weights = [self.probs[m] for m in self.moves]

    def play(self, history: Optional[List[str]] = None, my_history: Optional[List[str]] = None) -> str:
        return self.rng.choices(self.moves, weights=self.weights, k=1)[0]

    def reset(self):
        pass


class FixedMoveOpponent:
    """Always plays a single static gesture."""

    def __init__(self, move: str = "rock"):
        self.move = move

    def play(self, history: Optional[List[str]] = None, my_history: Optional[List[str]] = None) -> str:
        return self.move

    def reset(self):
        pass
