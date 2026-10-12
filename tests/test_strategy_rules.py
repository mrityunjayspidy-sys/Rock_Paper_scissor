"""
Unit Tests: Strategy Detection Rules and RuleBasedAgent
=======================================================
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ai.strategy_rules import (
    ALL_MOVES,
    WinStayLoseShiftRule,
    CyclingRule,
    CopyingRule,
    BiasedPlayRule,
    StrategyDetector,
    RuleBasedAgent,
)


def test_cycling_rule_forward_cycle():
    rule = CyclingRule()
    cycle = ["rock", "paper", "scissors"] * 6
    det = rule.evaluate(cycle)

    assert det.detected is True
    assert det.confidence > 0.80
    assert "Forward" in det.explanation
    assert det.predicted_next_move == "rock"


def test_wsls_rule_detection():
    rule = WinStayLoseShiftRule()

    # Construct trace where opponent strictly does Win-Stay and Lose-Shift
    # Opponent plays rock, Me plays scissors -> Opponent wins -> Opponent stays with rock
    opp_history = ["rock", "rock", "rock", "paper", "scissors"]
    my_history  = ["scissors", "scissors", "paper", "scissors", "paper"]

    det = rule.evaluate(opp_history, my_history)
    assert det.metrics["total_tested"] > 0
    assert det.confidence >= 0.0
    assert "Opponent stayed" in det.explanation


def test_biased_play_rule():
    rule = BiasedPlayRule()
    # 80% Rock
    biased_history = ["rock"] * 12 + ["paper"] * 2 + ["scissors"] * 1
    det = rule.evaluate(biased_history)

    assert det.detected is True
    assert det.confidence > 0.70
    assert det.predicted_next_move == "rock"
    assert "rock" in det.explanation.lower()


def test_copying_rule():
    rule = CopyingRule()
    # Opponent plays what I played on the previous round
    my_history =  ["rock", "paper", "scissors", "rock", "paper", "scissors"]
    opp_history = ["rock", "rock", "paper", "scissors", "rock", "paper"]

    det = rule.evaluate(opp_history, my_history)
    assert det.detected is True
    assert det.confidence > 0.70
    assert "Direct Mirror" in det.explanation


def test_strategy_detector_ranking():
    detector = StrategyDetector(window_size=15)
    cycle = ["rock", "paper", "scissors"] * 5
    dominant, ranked = detector.get_dominant_strategy(cycle)

    assert dominant is not None
    assert dominant.rule_name == "cycling"
    assert len(ranked) >= 4
    # Ensure ranked is sorted descending
    for i in range(len(ranked) - 1):
        assert ranked[i].confidence >= ranked[i + 1].confidence


def test_rule_based_agent():
    agent = RuleBasedAgent(confidence_threshold=0.45, seed=42)
    cycle = ["rock", "paper", "scissors"] * 5

    move = agent.play(cycle)
    assert move in ALL_MOVES
    explanation = agent.get_last_explanation()
    assert len(explanation) > 0
