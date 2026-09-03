import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from ai.rps_ai import AdaptiveMarkovAI, ALL_MOVES, get_beating_move, resolve_outcome

def test_ai_initialization():
    ai = AdaptiveMarkovAI(gamma=0.94, epsilon=0.08, cold_start_rounds=10)
    assert ai.gamma == 0.94
    assert ai.epsilon == 0.08
    assert ai.cold_start_rounds == 10
    assert ai.round_count == 0

def test_cold_start_behavior():
    ai = AdaptiveMarkovAI(cold_start_rounds=5, epsilon=0)
    history = []
    for _ in range(5):
        bot_move, pred_move, model, conf, lat = ai.choose_move(history)
        assert model == "cold-start"
        assert bot_move in ALL_MOVES
        ai.update("rock", history)
        history.append("rock")

    # Post cold start
    bot_move, pred_move, model, conf, lat = ai.choose_move(history)
    assert model != "cold-start"

def test_cyclic_opponent_learning():
    ai = AdaptiveMarkovAI(gamma=0.96, epsilon=0.01, cold_start_rounds=3)
    history = []
    cycle = ["rock", "paper", "scissors"]
    bot_wins = 0
    total = 300

    for r in range(total):
        opp_move = cycle[r % len(cycle)]
        bot_move, pred_move, model, conf, lat = ai.choose_move(history)
        outcome = resolve_outcome(opp_move, bot_move)
        if outcome == "lose": # bot won
            bot_wins += 1
        ai.update(opp_move, history)
        history.append(opp_move)

    win_rate = bot_wins / total
    assert win_rate > 0.90, f"Expected >90% win rate against cyclic strategy, got {win_rate*100}%"
