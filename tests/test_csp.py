"""
Unit Tests: CSP Adversary and Constraint Validation
===================================================
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ai.csp_adversary import (
    ALL_MOVES,
    CSPConstraintValidator,
    CSPSequenceGenerator,
    AdversaryAgent,
)


def test_csp_sequence_length_and_balance():
    generator = CSPSequenceGenerator(max_transition_prob=0.45, seed=123)
    n = 300
    seq = generator.generate(n)
    assert len(seq) == n

    counts = {m: seq.count(m) for m in ALL_MOVES}
    target = n // 3
    # Check that each move count is within +-1
    for m in ALL_MOVES:
        assert abs(counts[m] - target) <= 1, f"Move {m} count {counts[m]} deviates from target {target}"


def test_csp_no_triple_repeats():
    generator = CSPSequenceGenerator(max_transition_prob=0.45, seed=999)
    seq = generator.generate(600)

    for i in range(2, len(seq)):
        is_triple = (seq[i] == seq[i - 1] == seq[i - 2])
        assert not is_triple, f"Triple repeat found at index {i}: {seq[i-2:i+1]}"


def test_csp_order1_predictability_cap():
    generator = CSPSequenceGenerator(max_transition_prob=0.45, seed=42)
    seq = generator.generate(1000)

    validator = CSPConstraintValidator(max_transition_prob=0.45)
    report = validator.validate(seq)

    assert report["is_valid"] is True
    assert report["triple_repeats_count"] == 0
    assert report["max_transition_prob"] <= 0.46, f"Transition prob {report['max_transition_prob']} exceeds cap"
    assert report["mean_transition_entropy"] > 1.40, f"Entropy {report['mean_transition_entropy']} too low"


def test_csp_validator_detects_violations():
    validator = CSPConstraintValidator(max_transition_prob=0.45)

    # Sequence with triple repeats
    bad_seq = ["rock", "rock", "rock", "paper", "scissors", "rock"] * 10
    report = validator.validate(bad_seq)
    assert report["is_valid"] is False
    assert report["triple_repeats_count"] > 0


def test_adversary_agent_interface():
    agent = AdversaryAgent(sequence_length=100, seed=77)
    moves_played = []
    for _ in range(100):
        m = agent.play()
        assert m in ALL_MOVES
        moves_played.append(m)

    assert len(moves_played) == 100
    report = agent.get_validation_report()
    assert report["is_valid"] is True

    # Test reset
    agent.reset()
    assert agent.current_idx == 0
