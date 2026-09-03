"""
Rock-Paper-Scissors Adaptive Markov AI Engine (Python Implementation)
Opponent-Modeling Adaptive Markov AI with Exponential Decay and Dynamic Model Selection.
"""

import time
import random
from typing import List, Dict, Tuple, Optional

ALL_MOVES = ["rock", "paper", "scissors"]

def get_beating_move(move: str) -> str:
    if move == "rock":
        return "paper"
    elif move == "paper":
        return "scissors"
    elif move == "scissors":
        return "rock"
    raise ValueError(f"Invalid move: {move}")

def get_losing_move(move: str) -> str:
    if move == "rock":
        return "scissors"
    elif move == "paper":
        return "rock"
    elif move == "scissors":
        return "paper"
    raise ValueError(f"Invalid move: {move}")

def resolve_outcome(player_move: str, bot_move: str) -> str:
    if player_move == bot_move:
        return "tie"
    if (
        (player_move == "rock" and bot_move == "scissors") or
        (player_move == "paper" and bot_move == "rock") or
        (player_move == "scissors" and bot_move == "paper")
    ):
        return "win"
    return "lose"

def move_to_index(move: str) -> int:
    return ALL_MOVES.index(move)

def index_to_move(idx: int) -> str:
    return ALL_MOVES[idx % len(ALL_MOVES)]

class AdaptiveMarkovAI:
    def __init__(
        self,
        gamma: float = 0.94,
        epsilon: float = 0.08,
        cold_start_rounds: int = 10,
        window_size: int = 20,
        smoothing: float = 0.05,
        blunder_rate: float = 0.0
    ):
        self.gamma = gamma
        self.epsilon = epsilon
        self.cold_start_rounds = cold_start_rounds
        self.window_size = window_size
        self.smoothing = smoothing
        self.blunder_rate = blunder_rate
        self.round_count = 0

        # Order-1 Table: [last_move][next_move]
        self.order1_table: Dict[str, Dict[str, float]] = {
            m: {m2: 0.0 for m2 in ALL_MOVES} for m in ALL_MOVES
        }

        # Order-2 Table: [f"{m1},{m2}"][next_move]
        self.order2_table: Dict[str, Dict[str, float]] = {
            f"{m1},{m2}": {m3: 0.0 for m3 in ALL_MOVES}
            for m1 in ALL_MOVES for m2 in ALL_MOVES
        }

        self.order1_history: List[int] = []
        self.order2_history: List[int] = []
        self.order1_total = 0
        self.order1_correct = 0
        self.order2_total = 0
        self.order2_correct = 0

    def get_rolling_accuracy(self, hist: List[int]) -> float:
        if not hist:
            return 1.0 / 3.0
        return sum(hist) / len(hist)

    def predict_from_dist(self, dist: Dict[str, float]) -> Tuple[str, float]:
        smoothed = {m: dist.get(m, 0.0) + self.smoothing for m in ALL_MOVES}
        total = sum(smoothed.values())
        best_move = max(ALL_MOVES, key=lambda m: smoothed[m])
        max_prob = smoothed[best_move] / total
        return best_move, max_prob

    def predict_next_move(self, history: List[str]) -> Tuple[str, str, float]:
        if not history:
            return random.choice(ALL_MOVES), "random", 1.0 / 3.0

        last_move = history[-1]
        o1_pred_move, o1_conf = self.predict_from_dist(self.order1_table[last_move])

        o2_pred_move = None
        o2_conf = 0.0
        if len(history) >= 2:
            key = f"{history[-2]},{history[-1]}"
            dist = self.order2_table.get(key, {m: 0.0 for m in ALL_MOVES})
            if sum(dist.values()) > 0.05:
                o2_pred_move, o2_conf = self.predict_from_dist(dist)

        o1_acc = self.get_rolling_accuracy(self.order1_history)
        o2_acc = self.get_rolling_accuracy(self.order2_history)

        selected_model = "order-1"
        predicted_move = o1_pred_move
        confidence = o1_conf

        if o2_pred_move is not None:
            if o2_acc > o1_acc:
                selected_model = "order-2"
                predicted_move = o2_pred_move
                confidence = o2_conf
            elif abs(o2_acc - o1_acc) < 0.08 and o2_conf >= o1_conf:
                selected_model = "order-2"
                predicted_move = o2_pred_move
                confidence = o2_conf

        return predicted_move, selected_model, confidence

    def choose_move(self, history: List[str]) -> Tuple[str, str, str, float, float]:
        start = time.perf_counter()
        pred_move, model_used, confidence = self.predict_next_move(history)

        is_cold_start = len(history) < self.cold_start_rounds
        is_explore = random.random() < self.epsilon

        if is_cold_start:
            bot_move = random.choice(ALL_MOVES)
            final_model = "cold-start"
        elif is_explore:
            bot_move = random.choice(ALL_MOVES)
            final_model = "random"
        else:
            bot_move = get_beating_move(pred_move)
            if self.blunder_rate > 0 and random.random() < self.blunder_rate:
                bot_move = get_losing_move(pred_move)
            final_model = model_used

        latency_ms = (time.perf_counter() - start) * 1000.0
        return bot_move, pred_move, final_model, confidence, latency_ms

    def update(self, actual_move: str, history: List[str]):
        # Apply exponential decay
        for m1 in ALL_MOVES:
            for m2 in ALL_MOVES:
                self.order1_table[m1][m2] *= self.gamma

        for key in self.order2_table:
            for m3 in ALL_MOVES:
                self.order2_table[key][m3] *= self.gamma

        # Accuracy tracking
        if len(history) >= 1:
            last = history[-1]
            o1_pred, _ = self.predict_from_dist(self.order1_table[last])
            hit = 1 if o1_pred == actual_move else 0
            self.order1_history.append(hit)
            if len(self.order1_history) > self.window_size:
                self.order1_history.pop(0)
            self.order1_total += 1
            if hit:
                self.order1_correct += 1

        if len(history) >= 2:
            key = f"{history[-2]},{history[-1]}"
            o2_pred, _ = self.predict_from_dist(self.order2_table[key])
            hit = 1 if o2_pred == actual_move else 0
            self.order2_history.append(hit)
            if len(self.order2_history) > self.window_size:
                self.order2_history.pop(0)
            self.order2_total += 1
            if hit:
                self.order2_correct += 1

        # Increment counts
        if len(history) >= 1:
            last = history[-1]
            self.order1_table[last][actual_move] += 1.0

        if len(history) >= 2:
            key = f"{history[-2]},{history[-1]}"
            self.order2_table[key][actual_move] += 1.0

        self.round_count += 1
