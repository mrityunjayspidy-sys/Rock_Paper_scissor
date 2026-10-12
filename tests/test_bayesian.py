"""
Unit Tests: Bayesian Inference and Probabilistic Opponent Modeling
===================================================================
"""

import pytest
import math
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ai.bayesian_agent import (
    ALL_MOVES,
    DirichletDistribution,
    BayesianAgent,
)


def test_dirichlet_prior_and_posterior_update():
    dirichlet = DirichletDistribution(prior_alpha=1.0)
    prior_dist = dirichlet.get_predictive_distribution()

    # Uniform prior
    for m in ALL_MOVES:
        assert pytest.approx(prior_dist[m], abs=1e-4) == 1.0 / 3.0

    # Observe 10 Rock moves
    for _ in range(10):
        dirichlet.update("rock")

    post_dist = dirichlet.get_predictive_distribution()
    assert sum(post_dist.values()) == pytest.approx(1.0, abs=1e-5)
    # Expected: alpha = (11, 1, 1), total = 13 -> P(rock) = 11/13 ~ 0.846
    assert post_dist["rock"] > 0.80
    assert post_dist["paper"] < 0.10
    assert post_dist["scissors"] < 0.10


def test_bayesian_agent_best_response():
    agent = BayesianAgent(prior_alpha=1.0, seed=42)

    # If opponent always plays rock, agent must quickly adapt to play paper
    history = []
    for _ in range(30):
        move = agent.play(history)
        agent.update("rock", history)
        history.append("rock")

    # Final decision should be paper to counter rock
    assert agent.play(history) == "paper"


def test_bayesian_entropy_computation():
    agent = BayesianAgent()
    # Uniform
    uniform = {m: 1.0 / 3.0 for m in ALL_MOVES}
    h_uniform = agent.compute_entropy(uniform)
    assert pytest.approx(h_uniform, abs=0.01) == math.log2(3.0)

    # Skewed
    skewed = {"rock": 0.90, "paper": 0.05, "scissors": 0.05}
    h_skewed = agent.compute_entropy(skewed)
    assert h_skewed < h_uniform
    assert h_skewed > 0.0


def test_bayesian_audit_logging():
    agent = BayesianAgent(seed=42)
    history = []

    for r in range(5):
        move = agent.play(history)
        opp_move = ALL_MOVES[r % 3]
        agent.update(opp_move, history)
        history.append(opp_move)

    logs = agent.get_logs()
    assert len(logs) == 5
    for l in logs:
        assert "p_rock" in l
        assert "p_paper" in l
        assert "p_scissors" in l
        total_p = l["p_rock"] + l["p_paper"] + l["p_scissors"]
        assert pytest.approx(total_p, abs=0.02) == 1.0
        assert l["actual_opponent"] in ALL_MOVES
        assert l["outcome"] in ("win", "lose", "tie")
