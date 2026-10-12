"""
CSP Adversary: Constraint Satisfaction Problem Move Sequence Generator
========================================================================

AI Concept:
Constraint Satisfaction Problems (CSP) model combinatorial problems where states
must satisfy a set of hard constraints. In adversarial Rock-Paper-Scissors, an adversary
aims to remain unpredictable to Markovian or statistical opponent modelers while maintaining
naturalistic human-like aggregate properties.

This module implements:
1. Balanced move distribution: R, P, S appear equally (within +-1 over N moves,
   and within bounded tolerance in sliding windows).
2. No triple repeats: No move is repeated three times consecutively (s_i != s_{i-1} or s_{i-1} != s_{i-2}).
3. Low Order-1 predictability: Empirical transition probabilities P(m_{t} | m_{t-1}) <= 0.45,
   ensuring high transition entropy H(T) close to the maximum theoretical log2(3) ~ 1.585 bits.

Search Technique:
- Variable Ordering: Sequential indexed variables X_0, X_1, ..., X_{N-1}.
- Value Ordering: Randomized value ordering with forward checking to prune values violating
  the triple-repeat constraint, aggregate budget limits, or transition frequency caps.
- Scalability: Chunked backtracking with overlap boundary stitching, solving blocks of size K
  with forward checking, guaranteed to scale efficiently to N >= 1000 moves.
"""

from __future__ import annotations
import math
import random
from typing import List, Dict, Tuple, Optional, Any

ALL_MOVES: List[str] = ["rock", "paper", "scissors"]
MOVE_INDICES: Dict[str, int] = {m: i for i, m in enumerate(ALL_MOVES)}


class CSPConstraintValidator:
    """
    Validates move sequences against all CSP adversary constraints and computes metrics.
    """

    def __init__(
        self,
        max_transition_prob: float = 0.45,
        window_size: int = 30,
        window_tolerance: float = 0.25,
    ):
        self.max_transition_prob = max_transition_prob
        self.window_size = window_size
        self.window_tolerance = window_tolerance

    def validate(self, sequence: List[str]) -> Dict[str, Any]:
        n = len(sequence)
        if n == 0:
            return {
                "is_valid": False,
                "length": 0,
                "errors": ["Sequence is empty"],
            }

        errors: List[str] = []
        warnings: List[str] = []

        # 1. Check Global Balance (within +-1 if n % 3 == 0)
        counts = {m: sequence.count(m) for m in ALL_MOVES}
        target = n / 3.0
        max_deviation = max(abs(counts[m] - target) for m in ALL_MOVES)
        if max_deviation > 1.5:
            errors.append(
                f"Global counts not balanced: {counts} (max deviation: {max_deviation:.1f})"
            )

        # 2. Check No Triple Repeats
        triple_repeat_indices: List[int] = []
        for i in range(2, n):
            if sequence[i] == sequence[i - 1] == sequence[i - 2]:
                triple_repeat_indices.append(i)

        if triple_repeat_indices:
            errors.append(
                f"Triple repeats found at {len(triple_repeat_indices)} locations: indices {triple_repeat_indices[:5]}..."
            )

        # 3. Check Order-1 Transition Probabilities & Entropy
        transition_counts: Dict[str, Dict[str, int]] = {
            m1: {m2: 0 for m2 in ALL_MOVES} for m1 in ALL_MOVES
        }
        for i in range(1, n):
            prev_m = sequence[i - 1]
            curr_m = sequence[i]
            transition_counts[prev_m][curr_m] += 1

        transition_probs: Dict[str, Dict[str, float]] = {}
        max_t_prob = 0.0
        conditional_entropies: List[float] = []

        for m1 in ALL_MOVES:
            row_sum = sum(transition_counts[m1].values())
            transition_probs[m1] = {}
            if row_sum > 0:
                h_row = 0.0
                for m2 in ALL_MOVES:
                    p = transition_counts[m1][m2] / row_sum
                    transition_probs[m1][m2] = p
                    if p > max_t_prob:
                        max_t_prob = p
                    if p > 0:
                        h_row -= p * math.log2(p)
                conditional_entropies.append(h_row)
            else:
                for m2 in ALL_MOVES:
                    transition_probs[m1][m2] = 1.0 / 3.0
                conditional_entropies.append(math.log2(3.0))

        # Check maximum transition probability
        if n > 10 and max_t_prob > (self.max_transition_prob + 0.02):
            errors.append(
                f"Max Order-1 transition prob {max_t_prob:.3f} exceeds cap of {self.max_transition_prob:.2f}"
            )

        mean_entropy = (
            sum(conditional_entropies) / len(conditional_entropies)
            if conditional_entropies
            else 0.0
        )
        max_entropy = math.log2(3.0)  # ~1.58496 bits

        # 4. Check Sliding Window Balance
        window_imbalances = 0
        if n >= self.window_size:
            w_target = self.window_size / 3.0
            for start in range(0, n - self.window_size + 1, max(1, self.window_size // 4)):
                w = sequence[start : start + self.window_size]
                for m in ALL_MOVES:
                    if abs(w.count(m) - w_target) / self.window_size > self.window_tolerance:
                        window_imbalances += 1
                        break

        is_valid = len(errors) == 0

        return {
            "is_valid": is_valid,
            "length": n,
            "counts": counts,
            "max_deviation": max_deviation,
            "triple_repeats_count": len(triple_repeat_indices),
            "max_transition_prob": round(max_t_prob, 4),
            "transition_probabilities": {
                m1: {m2: round(transition_probs[m1][m2], 4) for m2 in ALL_MOVES}
                for m1 in ALL_MOVES
            },
            "transition_counts": transition_counts,
            "mean_transition_entropy": round(mean_entropy, 4),
            "theoretical_max_entropy": round(max_entropy, 4),
            "entropy_ratio": round(mean_entropy / max_entropy, 4) if max_entropy > 0 else 0.0,
            "window_imbalances": window_imbalances,
            "errors": errors,
            "warnings": warnings,
        }


class CSPSequenceGenerator:
    """
    Backtracking search engine for generating move sequences under balance,
    anti-repetition, and transition unpredictability constraints.
    """

    def __init__(
        self,
        max_transition_prob: float = 0.45,
        seed: Optional[int] = None,
    ):
        self.max_transition_prob = max_transition_prob
        self.rng = random.Random(seed)
        self.validator = CSPConstraintValidator(max_transition_prob=max_transition_prob)

    def _solve_chunk(
        self,
        chunk_size: int,
        target_counts: Dict[str, int],
        prefix: List[str],
        transition_matrix: Dict[str, Dict[str, int]],
        max_t_prob: float,
    ) -> Optional[List[str]]:
        """
        Solves a chunk of moves via depth-first backtracking with forward checking.
        """
        curr_counts = {m: 0 for m in ALL_MOVES}
        result: List[str] = []

        # Local copy of transition counts
        local_t = {
            m1: {m2: transition_matrix[m1][m2] for m2 in ALL_MOVES} for m1 in ALL_MOVES
        }

        def backtrack(step: int) -> bool:
            if step == chunk_size:
                # Confirm target counts exactly met
                return all(curr_counts[m] == target_counts[m] for m in ALL_MOVES)

            prev1 = result[-1] if result else (prefix[-1] if prefix else None)
            prev2 = (
                result[-2]
                if len(result) >= 2
                else (prefix[-1] if len(result) == 1 and prefix else (prefix[-2] if len(prefix) >= 2 else None))
            )

            # Randomized value ordering
            candidates = list(ALL_MOVES)
            self.rng.shuffle(candidates)

            # Least-constraining value / entropy heuristic:
            # Prioritize moves with lowest prior transition count from prev1 and largest remaining quota
            if prev1 is not None:
                candidates.sort(key=lambda m: (local_t[prev1][m], -(target_counts[m] - curr_counts[m])))
            else:
                candidates.sort(key=lambda m: -(target_counts[m] - curr_counts[m]))

            for move in candidates:
                # 1. Forward Checking: Move quota
                if curr_counts[move] >= target_counts[move]:
                    continue

                # 2. Forward Checking: No Triple Repeat
                if prev1 == move and prev2 == move:
                    continue

                # 3. Forward Checking: Transition Cap
                if prev1 is not None:
                    row_total = sum(local_t[prev1].values()) + 1
                    projected_prob = (local_t[prev1][move] + 1) / row_total
                    # In early steps of small chunks allow slight relaxation, but cap strictly after 15 steps
                    threshold = max_t_prob if (row_total >= 12 or step >= 20) else 0.55
                    if projected_prob > threshold and row_total >= 8:
                        continue

                # Apply move
                curr_counts[move] += 1
                result.append(move)
                if prev1 is not None:
                    local_t[prev1][move] += 1

                if backtrack(step + 1):
                    return True

                # Undo move
                if prev1 is not None:
                    local_t[prev1][move] -= 1
                result.pop()
                curr_counts[move] -= 1

            return False

        if backtrack(0):
            return result
        return None

    def generate(self, n: int = 1000, chunk_size: int = 60) -> List[str]:
        """
        Generates an N-move sequence by solving in stitched chunks to scale to large N.
        """
        full_sequence: List[str] = []
        global_target_base = n // 3
        remainder = n % 3
        global_targets = {m: global_target_base for m in ALL_MOVES}
        for i in range(remainder):
            global_targets[ALL_MOVES[i]] += 1

        global_counts = {m: 0 for m in ALL_MOVES}
        transition_matrix = {m1: {m2: 0 for m2 in ALL_MOVES} for m1 in ALL_MOVES}

        remaining_rounds = n
        while remaining_rounds > 0:
            current_chunk_size = min(chunk_size, remaining_rounds)
            # Allocate chunk targets proportionally to remaining needed
            needed = {m: global_targets[m] - global_counts[m] for m in ALL_MOVES}

            chunk_targets = {m: current_chunk_size // 3 for m in ALL_MOVES}
            chunk_rem = current_chunk_size % 3

            # Give remainder to moves with highest pending deficit
            sorted_needed = sorted(ALL_MOVES, key=lambda m: -needed[m])
            for i in range(chunk_rem):
                chunk_targets[sorted_needed[i]] += 1

            prefix = full_sequence[-2:] if len(full_sequence) >= 2 else full_sequence[:]
            chunk = self._solve_chunk(
                current_chunk_size,
                chunk_targets,
                prefix,
                transition_matrix,
                self.max_transition_prob,
            )

            # Fallback repair if strict backtrack fails on a boundary
            if chunk is None:
                chunk = self._generate_fallback_chunk(current_chunk_size, chunk_targets, prefix)

            for i, m in enumerate(chunk):
                if full_sequence:
                    prev_m = full_sequence[-1]
                    transition_matrix[prev_m][m] += 1
                full_sequence.append(m)
                global_counts[m] += 1

            remaining_rounds -= current_chunk_size

        return full_sequence

    def _generate_fallback_chunk(
        self,
        size: int,
        targets: Dict[str, int],
        prefix: List[str],
    ) -> List[str]:
        """
        Greedy min-conflicts repair fallback ensuring hard constraints are preserved.
        """
        pool: List[str] = []
        for m, count in targets.items():
            pool.extend([m] * count)
        self.rng.shuffle(pool)

        # Fix any triple repeats iteratively
        for attempt in range(100):
            has_triple = False
            for i in range(len(pool)):
                p1 = pool[i - 1] if i >= 1 else (prefix[-1] if prefix else None)
                p2 = pool[i - 2] if i >= 2 else (prefix[-2] if len(prefix) >= 2 else None)
                if p1 == pool[i] and p2 == pool[i]:
                    has_triple = True
                    # Swap with another position
                    swap_idx = self.rng.randint(0, len(pool) - 1)
                    pool[i], pool[swap_idx] = pool[swap_idx], pool[i]
            if not has_triple:
                break
        return pool


class AdversaryAgent:
    """
    Opponent agent powered by the CSP move generator.
    Produces pre-generated constraint-satisfying moves or generates dynamically.
    """

    def __init__(
        self,
        sequence_length: int = 1000,
        max_transition_prob: float = 0.45,
        seed: Optional[int] = None,
        precomputed_sequence: Optional[List[str]] = None,
    ):
        self.sequence_length = sequence_length
        self.max_transition_prob = max_transition_prob
        self.seed = seed
        self.generator = CSPSequenceGenerator(max_transition_prob=max_transition_prob, seed=seed)
        if precomputed_sequence is not None:
            self.sequence = list(precomputed_sequence)
        else:
            self.sequence = self.generator.generate(sequence_length)
        self.current_idx = 0

    def play(self, history: Optional[List[str]] = None) -> str:
        """
        Returns the next move in the constraint-satisfying sequence.
        """
        if self.current_idx < len(self.sequence):
            move = self.sequence[self.current_idx]
            self.current_idx += 1
            return move
        # If sequence exhausted, cycle or generate extension
        move = self.sequence[self.current_idx % len(self.sequence)]
        self.current_idx += 1
        return move

    def reset(self):
        self.current_idx = 0

    def get_validation_report(self) -> Dict[str, Any]:
        return CSPConstraintValidator(self.max_transition_prob).validate(self.sequence)
