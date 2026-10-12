"""
Knowledge & Reasoning Layer: Strategy Detection Rules
=====================================================

AI Concept:
Human decision-making in zero-sum sequential games often exhibits cognitive biases,
bounded rationality, and heuristic habit loops rather than true mixed-strategy Nash equilibrium.
This module encodes explicit symbolic knowledge rules over sliding history windows:
1. Win-Stay / Lose-Shift (WSLS): Classic reinforcement learning heuristic (Thorndike's law of effect).
2. Cycling: Predictable circular move sequences (R -> P -> S or R -> S -> P).
3. Copying & Counter-Copying: Social imitation and anticipatory counter-play against opponent's prior action.
4. Frequency Bias: Over-reliance on a single preferred gesture (e.g., Rock bias).

Each rule outputs a normalized confidence score [0.0, 1.0] and an interpretable natural language explanation.
"""

from __future__ import annotations
from dataclasses import dataclass, field
import random
from typing import List, Dict, Optional, Tuple, Any

ALL_MOVES: List[str] = ["rock", "paper", "scissors"]

def get_beating_move(move: str) -> str:
    """Returns the move that defeats the input move."""
    mapping = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
    return mapping.get(move.lower(), "paper")

def get_losing_move(move: str) -> str:
    """Returns the move that loses to the input move."""
    mapping = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
    return mapping.get(move.lower(), "scissors")

def resolve_outcome(player_move: str, bot_move: str) -> str:
    """
    Resolves outcome from the player's perspective:
    - 'win': player defeats bot
    - 'lose': bot defeats player
    - 'tie': equal moves
    """
    p, b = player_move.lower(), bot_move.lower()
    if p == b:
        return "tie"
    if (p == "rock" and b == "scissors") or (p == "paper" and b == "rock") or (p == "scissors" and b == "paper"):
        return "win"
    return "lose"


@dataclass
class RuleDetection:
    """Detection result for an individual strategy rule."""
    rule_name: str
    detected: bool
    confidence: float
    predicted_next_move: Optional[str]
    explanation: str
    metrics: Dict[str, Any] = field(default_factory=dict)


class StrategyRule:
    """Abstract base class for a symbolic human strategy detection rule."""
    name: str = "base_rule"

    def evaluate(
        self,
        opponent_history: List[str],
        my_history: Optional[List[str]] = None,
        window_size: int = 15,
    ) -> RuleDetection:
        raise NotImplementedError


class WinStayLoseShiftRule(StrategyRule):
    """
    Detects Win-Stay / Lose-Shift behavior:
    - After an opponent win, do they repeat their winning move?
    - After an opponent loss, do they shift to another move?
    """
    name = "win_stay_lose_shift"

    def evaluate(
        self,
        opponent_history: List[str],
        my_history: Optional[List[str]] = None,
        window_size: int = 15,
    ) -> RuleDetection:
        if len(opponent_history) < 3 or not my_history or len(my_history) != len(opponent_history):
            return RuleDetection(
                rule_name=self.name,
                detected=False,
                confidence=0.0,
                predicted_next_move=None,
                explanation="Insufficient history or missing simultaneous match logs for WSLS detection.",
            )

        start = max(1, len(opponent_history) - window_size)
        win_stay_count, total_wins = 0, 0
        lose_shift_count, total_losses = 0, 0

        # Evaluate transitions from t-1 to t
        for t in range(start, len(opponent_history)):
            prev_opp = opponent_history[t - 1]
            prev_my = my_history[t - 1]
            curr_opp = opponent_history[t]

            # Outcome for opponent
            opp_outcome = resolve_outcome(prev_opp, prev_my)

            if opp_outcome == "win":
                total_wins += 1
                if curr_opp == prev_opp:
                    win_stay_count += 1
            elif opp_outcome == "lose":
                total_losses += 1
                if curr_opp != prev_opp:
                    lose_shift_count += 1

        total_tested = total_wins + total_losses
        if total_tested < 3:
            return RuleDetection(
                rule_name=self.name,
                detected=False,
                confidence=0.0,
                predicted_next_move=None,
                explanation="Too few decisive win/loss outcomes to evaluate WSLS pattern.",
            )

        stay_rate = win_stay_count / total_wins if total_wins > 0 else 0.5
        shift_rate = lose_shift_count / total_losses if total_losses > 0 else 0.5

        # Weighted consistency
        wsls_score = (win_stay_count + lose_shift_count) / total_tested
        # Random chance baseline is 1/3 stay, 2/3 shift -> mean expectation ~ (1/3 + 2/3)/2 ~ 0.5
        confidence = max(0.0, min(1.0, (wsls_score - 0.40) / 0.50))

        # Predict next move based on outcome of most recent completed round
        last_opp = opponent_history[-1]
        last_my = my_history[-1]
        last_outcome = resolve_outcome(last_opp, last_my)

        predicted: Optional[str] = None
        if last_outcome == "win":
            predicted = last_opp  # Win-Stay
        elif last_outcome == "lose":
            # Shifts to move that would have defeated my previous move
            predicted = get_beating_move(last_my)
        else:
            predicted = get_beating_move(last_opp)

        detected = confidence >= 0.45
        explanation = (
            f"Opponent stayed after {win_stay_count}/{total_wins} wins ({stay_rate*100:.0f}%) "
            f"and shifted after {lose_shift_count}/{total_losses} losses ({shift_rate*100:.0f}%). "
            f"Overall WSLS consistency: {wsls_score*100:.1f}%."
        )

        return RuleDetection(
            rule_name=self.name,
            detected=detected,
            confidence=round(confidence, 3),
            predicted_next_move=predicted if detected else None,
            explanation=explanation,
            metrics={
                "total_tested": total_tested,
                "win_stay_rate": round(stay_rate, 3),
                "lose_shift_rate": round(shift_rate, 3),
                "wsls_score": round(wsls_score, 3),
            },
        )


class CyclingRule(StrategyRule):
    """
    Detects deterministic periodic cycling:
    - Forward cycling: Rock -> Paper -> Scissors -> Rock (+1 step)
    - Backward cycling: Rock -> Scissors -> Paper -> Rock (-1 step)
    - Period-2 oscillations: alternating between two specific moves.
    """
    name = "cycling"

    def evaluate(
        self,
        opponent_history: List[str],
        my_history: Optional[List[str]] = None,
        window_size: int = 15,
    ) -> RuleDetection:
        if len(opponent_history) < 4:
            return RuleDetection(
                rule_name=self.name,
                detected=False,
                confidence=0.0,
                predicted_next_move=None,
                explanation="Need at least 4 moves to detect cyclic periodicity.",
            )

        window = opponent_history[-window_size:]
        n = len(window)

        # Check Forward Cycle: m_t beats m_{t-1}
        forward_hits = 0
        backward_hits = 0

        forward_map = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
        backward_map = {"rock": "scissors", "paper": "rock", "scissors": "paper"}

        for i in range(1, n):
            prev_m = window[i - 1]
            curr_m = window[i]
            if curr_m == forward_map[prev_m]:
                forward_hits += 1
            if curr_m == backward_map[prev_m]:
                backward_hits += 1

        total_transitions = n - 1
        fwd_rate = forward_hits / total_transitions
        bwd_rate = backward_hits / total_transitions

        best_rate = max(fwd_rate, bwd_rate)
        # Expected baseline random rate is 1/3 (0.333)
        confidence = max(0.0, min(1.0, (best_rate - 0.33) / 0.55))

        last_move = window[-1]
        predicted: Optional[str] = None
        cycle_type = "none"

        if fwd_rate >= bwd_rate:
            cycle_type = "Forward (R->P->S)"
            predicted = forward_map[last_move]
        else:
            cycle_type = "Backward (R->S->P)"
            predicted = backward_map[last_move]

        detected = confidence >= 0.50
        explanation = (
            f"Detected {cycle_type} cycling in {max(forward_hits, backward_hits)} of "
            f"{total_transitions} transitions ({best_rate*100:.1f}% accuracy)."
        )

        return RuleDetection(
            rule_name=self.name,
            detected=detected,
            confidence=round(confidence, 3),
            predicted_next_move=predicted if detected else None,
            explanation=explanation,
            metrics={
                "cycle_type": cycle_type,
                "forward_rate": round(fwd_rate, 3),
                "backward_rate": round(bwd_rate, 3),
                "best_rate": round(best_rate, 3),
            },
        )


class CopyingRule(StrategyRule):
    """
    Detects mirroring (copying) or counter-copying:
    - Direct Mirror: Opponent plays what I played on the previous round.
    - Counter-Copying: Opponent plays what beats my previous move.
    """
    name = "copying"

    def evaluate(
        self,
        opponent_history: List[str],
        my_history: Optional[List[str]] = None,
        window_size: int = 15,
    ) -> RuleDetection:
        if len(opponent_history) < 3 or not my_history or len(my_history) != len(opponent_history):
            return RuleDetection(
                rule_name=self.name,
                detected=False,
                confidence=0.0,
                predicted_next_move=None,
                explanation="Mirroring detection requires simultaneous opponent and player action history.",
            )

        start = max(1, len(opponent_history) - window_size)
        mirror_hits = 0
        counter_hits = 0
        total_steps = 0

        for t in range(start, len(opponent_history)):
            prev_my = my_history[t - 1]
            curr_opp = opponent_history[t]
            total_steps += 1

            if curr_opp == prev_my:
                mirror_hits += 1
            if curr_opp == get_beating_move(prev_my):
                counter_hits += 1

        if total_steps < 3:
            return RuleDetection(
                rule_name=self.name,
                detected=False,
                confidence=0.0,
                predicted_next_move=None,
                explanation="Insufficient window steps to test copying behavior.",
            )

        mirror_rate = mirror_hits / total_steps
        counter_rate = counter_hits / total_steps
        best_rate = max(mirror_rate, counter_rate)

        confidence = max(0.0, min(1.0, (best_rate - 0.33) / 0.55))
        last_my = my_history[-1]

        predicted: Optional[str] = None
        if mirror_rate >= counter_rate:
            copy_type = "Direct Mirror"
            predicted = last_my
        else:
            copy_type = "Counter-Copy"
            predicted = get_beating_move(last_my)

        detected = confidence >= 0.48
        explanation = (
            f"Detected {copy_type} behavior in {max(mirror_hits, counter_hits)}/{total_steps} "
            f"rounds ({best_rate*100:.1f}% matching)."
        )

        return RuleDetection(
            rule_name=self.name,
            detected=detected,
            confidence=round(confidence, 3),
            predicted_next_move=predicted if detected else None,
            explanation=explanation,
            metrics={
                "copy_type": copy_type,
                "mirror_rate": round(mirror_rate, 3),
                "counter_rate": round(counter_rate, 3),
            },
        )


class BiasedPlayRule(StrategyRule):
    """
    Detects heavy frequency skew toward a specific move (e.g. >50% Rock).
    """
    name = "biased_play"

    def evaluate(
        self,
        opponent_history: List[str],
        my_history: Optional[List[str]] = None,
        window_size: int = 15,
    ) -> RuleDetection:
        if len(opponent_history) < 5:
            return RuleDetection(
                rule_name=self.name,
                detected=False,
                confidence=0.0,
                predicted_next_move=None,
                explanation="Need at least 5 rounds to evaluate frequency bias.",
            )

        window = opponent_history[-window_size:]
        n = len(window)
        counts = {m: window.count(m) for m in ALL_MOVES}
        top_move = max(ALL_MOVES, key=lambda m: counts[m])
        top_freq = counts[top_move] / n

        # Expected baseline is 33.3%. Capped confidence scaled from 0.45 to 0.85
        confidence = max(0.0, min(1.0, (top_freq - 0.38) / 0.45))
        detected = confidence >= 0.45

        explanation = (
            f"Heavy preference for '{top_move}': chosen {counts[top_move]}/{n} times "
            f"({top_freq*100:.1f}% frequency) in recent history."
        )

        return RuleDetection(
            rule_name=self.name,
            detected=detected,
            confidence=round(confidence, 3),
            predicted_next_move=top_move if detected else None,
            explanation=explanation,
            metrics={
                "top_move": top_move,
                "frequency": round(top_freq, 3),
                "counts": counts,
            },
        )


class StrategyDetector:
    """
    Orchestrates multiple heuristic rules, scoring and ranking detected opponent strategies.
    """

    def __init__(self, window_size: int = 15):
        self.window_size = window_size
        self.rules: List[StrategyRule] = [
            CyclingRule(),
            WinStayLoseShiftRule(),
            CopyingRule(),
            BiasedPlayRule(),
        ]

    def detect_all(
        self,
        opponent_history: List[str],
        my_history: Optional[List[str]] = None,
    ) -> List[RuleDetection]:
        detections: List[RuleDetection] = []
        for rule in self.rules:
            det = rule.evaluate(opponent_history, my_history, self.window_size)
            detections.append(det)
        # Sort descending by confidence
        detections.sort(key=lambda d: -d.confidence)
        return detections

    def get_dominant_strategy(
        self,
        opponent_history: List[str],
        my_history: Optional[List[str]] = None,
    ) -> Tuple[Optional[RuleDetection], List[RuleDetection]]:
        ranked = self.detect_all(opponent_history, my_history)
        dominant = ranked[0] if (ranked and ranked[0].detected and ranked[0].confidence > 0.40) else None
        return dominant, ranked


class RuleBasedAgent:
    """
    An opponent-modeling agent that uses rule-based strategy detection to anticipate
    and counter the opponent's next move, with stochastic fallback under uncertainty.
    """

    def __init__(
        self,
        confidence_threshold: float = 0.45,
        window_size: int = 15,
        seed: Optional[int] = None,
    ):
        self.confidence_threshold = confidence_threshold
        self.detector = StrategyDetector(window_size=window_size)
        self.rng = random.Random(seed)
        self.last_detection: Optional[RuleDetection] = None
        self.my_history: List[str] = []

    def play(self, opponent_history: List[str], my_history: Optional[List[str]] = None) -> str:
        """
        Decides next move based on dominant detected opponent strategy.
        """
        history_to_use = my_history if my_history is not None else self.my_history
        dominant, _ = self.detector.get_dominant_strategy(opponent_history, history_to_use)
        self.last_detection = dominant

        if dominant and dominant.predicted_next_move and dominant.confidence >= self.confidence_threshold:
            # Play the move that beats the predicted opponent move
            chosen = get_beating_move(dominant.predicted_next_move)
        else:
            chosen = self.rng.choice(ALL_MOVES)

        self.my_history.append(chosen)
        return chosen

    def get_last_explanation(self) -> str:
        if self.last_detection:
            return f"[{self.last_detection.rule_name.upper()} conf={self.last_detection.confidence:.2f}] {self.last_detection.explanation}"
        return "No dominant rule detected; playing uniformly random move."
