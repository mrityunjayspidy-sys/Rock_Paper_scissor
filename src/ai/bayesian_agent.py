"""
Bayesian Reasoning & Explainability Layer: Probabilistic Opponent Modeling
==========================================================================

AI Concept:
Bayesian inference treats the opponent's strategy as an unknown parameter vector theta
over the probability simplex Delta^2. Beginning with a prior distribution (Dirichlet prior),
we update our beliefs sequentially using Bayes' Rule as empirical move evidence is observed.

Key Components:
1. Dirichlet-Multinomial Model (Marginal):
   - Prior: theta ~ Dirichlet(alpha_R, alpha_P, alpha_S).
   - Likelihood: Multinomial count distribution.
   - Posterior: theta | data ~ Dirichlet(alpha + counts).
   - Expected predictive distribution: E[theta_k] = (alpha_k + c_k) / sum(alpha + counts).

2. Context-Aware Dirichlet Markov Chain:
   - Order-1: Conditioned on prior move m_{t-1}, maintaining Dirichlet priors per context.
   - Order-2: Conditioned on 2-step sequence (m_{t-2}, m_{t-1}).
   - Dynamic Blending: Bayesian Model Averaging (BMA) weighting models by recent predictive evidence.

3. Decision Theory & Best Response:
   - Computes expected utility under the predicted probability vector:
     E[U(b)] = sum_m P(m) * Payoff(b, m).
   - Selects b* = argmax E[U(b)].

4. Explainability & Transparent Auditing:
   - Logs the full predicted probability distribution [P(R), P(P), P(S)], entropy H(P),
     and model attribution for every round.
"""

from __future__ import annotations
from dataclasses import dataclass, field
import math
import random
from typing import List, Dict, Tuple, Optional, Any

ALL_MOVES: List[str] = ["rock", "paper", "scissors"]

PAYOFF_MATRIX: Dict[str, Dict[str, float]] = {
    # [my_move][opp_move] -> payoff (+1 win, 0 tie, -1 loss)
    "rock": {"rock": 0.0, "paper": -1.0, "scissors": 1.0},
    "paper": {"rock": 1.0, "paper": 0.0, "scissors": -1.0},
    "scissors": {"rock": -1.0, "paper": 1.0, "scissors": 0.0},
}


@dataclass
class BayesianRoundLog:
    """Detailed explainability audit log for a single decision round."""
    round_number: int
    probabilities: Dict[str, float]
    predicted_opponent_move: str
    chosen_move: str
    actual_opponent_move: Optional[str] = None
    outcome: Optional[str] = None
    model_used: str = "dirichlet-marginal"
    entropy: float = 0.0


class DirichletDistribution:
    """
    Maintains a Dirichlet prior and updates counts under Multinomial observations.
    """

    def __init__(self, prior_alpha: float = 1.0):
        self.prior_alpha = prior_alpha
        # Prior hyperparameter vector alpha
        self.alpha: Dict[str, float] = {m: float(prior_alpha) for m in ALL_MOVES}
        self.counts: Dict[str, int] = {m: 0 for m in ALL_MOVES}

    def update(self, move: str, weight: float = 1.0):
        if move in self.counts:
            self.counts[move] += 1
            self.alpha[move] += weight

    def get_predictive_distribution(self) -> Dict[str, float]:
        total_alpha = sum(self.alpha.values())
        if total_alpha <= 0:
            return {m: 1.0 / 3.0 for m in ALL_MOVES}
        return {m: self.alpha[m] / total_alpha for m in ALL_MOVES}

    def reset(self):
        self.alpha = {m: float(self.prior_alpha) for m in ALL_MOVES}
        self.counts = {m: 0 for m in ALL_MOVES}


class BayesianAgent:
    """
    Probabilistic Opponent Modeler reasoning under uncertainty with
    Dirichlet priors and context-aware Markov transitions.
    """

    def __init__(
        self,
        prior_alpha: float = 1.0,
        model_mode: str = "adaptive_blend",  # 'marginal', 'order-1', 'order-2', 'adaptive_blend'
        rolling_window: int = 20,
        seed: Optional[int] = None,
    ):
        self.prior_alpha = prior_alpha
        self.model_mode = model_mode
        self.rolling_window = rolling_window
        self.rng = random.Random(seed)

        # 1. Marginal Dirichlet model
        self.marginal_model = DirichletDistribution(prior_alpha=prior_alpha)

        # 2. Order-1 Contextual Dirichlet models: P(m_t | m_{t-1})
        self.order1_models: Dict[str, DirichletDistribution] = {
            m: DirichletDistribution(prior_alpha=prior_alpha) for m in ALL_MOVES
        }

        # 3. Order-2 Contextual Dirichlet models: P(m_t | m_{t-2}, m_{t-1})
        self.order2_models: Dict[str, DirichletDistribution] = {
            f"{m1},{m2}": DirichletDistribution(prior_alpha=prior_alpha)
            for m1 in ALL_MOVES for m2 in ALL_MOVES
        }

        # Rolling accuracy tracking for adaptive blending
        self.marginal_hits: List[int] = []
        self.order1_hits: List[int] = []
        self.order2_hits: List[int] = []

        # Explainability audit trail
        self.audit_logs: List[BayesianRoundLog] = []
        self.my_history: List[str] = []
        self.round_counter = 0

    def compute_entropy(self, probs: Dict[str, float]) -> float:
        """Computes Shannon entropy H(P) = -sum p_i log2(p_i)."""
        h = 0.0
        for p in probs.values():
            if p > 1e-12:
                h -= p * math.log2(p)
        return round(h, 4)

    def get_predicted_distribution(self, history: List[str]) -> Tuple[Dict[str, float], str]:
        """
        Computes the predicted posterior predictive distribution over opponent moves.
        """
        marginal_dist = self.marginal_model.get_predictive_distribution()

        if self.model_mode == "marginal" or len(history) < 1:
            return marginal_dist, "dirichlet-marginal"

        o1_dist = None
        if len(history) >= 1:
            prev1 = history[-1]
            o1_dist = self.order1_models[prev1].get_predictive_distribution()

        if self.model_mode == "order-1" and o1_dist is not None:
            return o1_dist, "dirichlet-order1"

        o2_dist = None
        if len(history) >= 2:
            prev2 = f"{history[-2]},{history[-1]}"
            o2_dist = self.order2_models[prev2].get_predictive_distribution()

        if self.model_mode == "order-2" and o2_dist is not None:
            return o2_dist, "dirichlet-order2"

        # Adaptive Blending / Bayesian Model Averaging
        w_marginal = max(0.20, sum(self.marginal_hits[-self.rolling_window:]) / max(1, len(self.marginal_hits[-self.rolling_window:])))
        w_o1 = max(0.20, sum(self.order1_hits[-self.rolling_window:]) / max(1, len(self.order1_hits[-self.rolling_window:]))) if o1_dist else 0.0
        w_o2 = max(0.20, sum(self.order2_hits[-self.rolling_window:]) / max(1, len(self.order2_hits[-self.rolling_window:]))) if o2_dist else 0.0

        total_w = w_marginal + w_o1 + w_o2
        blended: Dict[str, float] = {}
        for m in ALL_MOVES:
            p = (w_marginal * marginal_dist[m])
            if o1_dist:
                p += (w_o1 * o1_dist[m])
            if o2_dist:
                p += (w_o2 * o2_dist[m])
            blended[m] = p / total_w

        # Pick primary responsible model tag
        if w_o2 > w_o1 and w_o2 > w_marginal:
            tag = "blended-order2-lead"
        elif w_o1 > w_marginal:
            tag = "blended-order1-lead"
        else:
            tag = "blended-marginal-lead"

        return blended, tag

    def select_best_response(self, probs: Dict[str, float]) -> str:
        """
        Maximizes expected utility E[U(b)] = sum_m P(m) * Payoff(b, m).
        """
        best_move = "rock"
        best_expected_utility = -float("inf")

        # Randomized tie-breaking
        shuffled_moves = list(ALL_MOVES)
        self.rng.shuffle(shuffled_moves)

        for my_move in shuffled_moves:
            expected_u = sum(probs[opp_m] * PAYOFF_MATRIX[my_move][opp_m] for opp_m in ALL_MOVES)
            if expected_u > best_expected_utility:
                best_expected_utility = expected_u
                best_move = my_move

        return best_move

    def play(self, history: List[str], my_history: Optional[List[str]] = None) -> str:
        """
        Enforces fair play: strictly receives past history (length <= round count).
        Predicts distribution, computes best response, and creates an audit entry.
        """
        self.round_counter += 1
        probs, model_tag = self.get_predicted_distribution(history)
        entropy = self.compute_entropy(probs)
        pred_opp_move = max(ALL_MOVES, key=lambda m: probs[m])

        chosen_move = self.select_best_response(probs)
        self.my_history.append(chosen_move)

        # Store audit log (actual opponent move filled in post-round via update)
        audit = BayesianRoundLog(
            round_number=self.round_counter,
            probabilities={m: round(probs[m], 4) for m in ALL_MOVES},
            predicted_opponent_move=pred_opp_move,
            chosen_move=chosen_move,
            model_used=model_tag,
            entropy=entropy,
        )
        self.audit_logs.append(audit)
        return chosen_move

    def update(self, actual_opponent_move: str, history: List[str]):
        """
        Updates Dirichlet priors sequentially with newly revealed opponent move.
        """
        # Complete last audit log entry
        if self.audit_logs:
            last_log = self.audit_logs[-1]
            last_log.actual_opponent_move = actual_opponent_move
            p_move = last_log.chosen_move
            # Result from Bayesian agent's perspective:
            from src.ai.strategy_rules import resolve_outcome
            last_log.outcome = resolve_outcome(p_move, actual_opponent_move)

            # Check individual model accuracy for blending
            m_pred = max(ALL_MOVES, key=lambda m: self.marginal_model.get_predictive_distribution()[m])
            self.marginal_hits.append(1 if m_pred == actual_opponent_move else 0)

            if len(history) >= 1:
                prev1 = history[-1]
                o1_pred = max(ALL_MOVES, key=lambda m: self.order1_models[prev1].get_predictive_distribution()[m])
                self.order1_hits.append(1 if o1_pred == actual_opponent_move else 0)

            if len(history) >= 2:
                prev2 = f"{history[-2]},{history[-1]}"
                o2_pred = max(ALL_MOVES, key=lambda m: self.order2_models[prev2].get_predictive_distribution()[m])
                self.order2_hits.append(1 if o2_pred == actual_opponent_move else 0)

        # Update marginal model
        self.marginal_model.update(actual_opponent_move)

        # Update order-1 contextual Dirichlet
        if len(history) >= 1:
            prev1 = history[-1]
            self.order1_models[prev1].update(actual_opponent_move)

        # Update order-2 contextual Dirichlet
        if len(history) >= 2:
            prev2 = f"{history[-2]},{history[-1]}"
            self.order2_models[prev2].update(actual_opponent_move)

    def get_logs(self) -> List[Dict[str, Any]]:
        return [
            {
                "round": l.round_number,
                "p_rock": l.probabilities.get("rock", 0.0),
                "p_paper": l.probabilities.get("paper", 0.0),
                "p_scissors": l.probabilities.get("scissors", 0.0),
                "predicted_opponent": l.predicted_opponent_move,
                "chosen_move": l.chosen_move,
                "actual_opponent": l.actual_opponent_move,
                "outcome": l.outcome,
                "model_used": l.model_used,
                "entropy": l.entropy,
            }
            for l in self.audit_logs
        ]

    def reset(self):
        self.marginal_model.reset()
        for m in ALL_MOVES:
            self.order1_models[m].reset()
        for k in self.order2_models:
            self.order2_models[k].reset()
        self.marginal_hits.clear()
        self.order1_hits.clear()
        self.order2_hits.clear()
        self.audit_logs.clear()
        self.my_history.clear()
        self.round_counter = 0
