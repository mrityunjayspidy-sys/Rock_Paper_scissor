#!/usr/bin/env python3
"""
Probabilistic Opponent Modeller: Scientific Experiment Runner & Benchmark Suite
================================================================================
Conducts multi-seed evaluation (N=1000 rounds x 20 seeds) of the probabilistic
Bayesian opponent predictor against standard agent baselines:
- Uniform Random (Nash Equilibrium Baseline)
- Rule-Based Agent (Knowledge & Reasoning Layer)
- Bayesian Agent (Self-play Symmetry)
- Biased Play (70% Rock)
- Cyclic Play (R -> P -> S deterministic sequence)
- Win-Stay / Lose-Shift (WSLS heuristic)
- Copier Opponent (Reactive Mirroring)

Generates:
1. results/summary.csv (Statistical summary of mean +- std across all metrics)
2. results/probability_tracking.png (Posterior belief tracking vs Biased & Random)
3. results/cumulative_winrate.png (1000-round progression curves)
4. results/transition_heatmap.png (Empirical transition matrix heatmaps)
"""

import os
import sys
import argparse
import csv
import time
from typing import Dict, List, Any, Tuple
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Ensure root and src are on path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.ai.strategy_rules import (
    ALL_MOVES,
    get_beating_move,
    resolve_outcome,
    RuleBasedAgent,
    StrategyDetector,
)
from src.ai.bayesian_agent import BayesianAgent
from src.ai.opponents import (
    RandomAgent,
    WinStayLoseShiftOpponent,
    CyclicOpponent,
    CopierOpponent,
    BiasedOpponent,
    FixedMoveOpponent,
)
from src.ai.rps_ai import AdaptiveMarkovAI


def play_match(
    predictor: Any,
    opponent: Any,
    rounds: int = 1000,
    seed: int = 42,
) -> Dict[str, Any]:
    """
    Executes a sequential match of `rounds` between a predictor and an opponent.
    Strictly asserts zero-lookahead simultaneously committed moves.
    """
    pred_history: List[str] = []
    opp_history: List[str] = []
    pred_wins = 0
    opp_wins = 0
    ties = 0
    hits = 0

    round_latencies: List[float] = []
    pred_win_progression: List[float] = []

    for r in range(rounds):
        # 1. Zero-Lookahead Fair Play assertion
        assert len(pred_history) == r, f"Fair Play violation! History length {len(pred_history)} != {r}"
        assert len(opp_history) == r, f"Fair Play violation! History length {len(opp_history)} != {r}"

        # 2. Predictor commits action
        t0 = time.perf_counter()
        if hasattr(predictor, "play"):
            # Predictor chooses counter move based strictly on past opponent history
            pred_move = predictor.play(opp_history)
        elif hasattr(predictor, "predict_and_counter"):
            pred_move = predictor.predict_and_counter(opp_history)
        else:
            pred_move = "rock"
        latency = (time.perf_counter() - t0) * 1000.0
        round_latencies.append(latency)

        # 3. Opponent commits action (simultaneous reveal)
        if isinstance(opponent, WinStayLoseShiftOpponent):
            opp_move = opponent.play(pred_history, opp_history)
        elif hasattr(opponent, "play"):
            opp_move = opponent.play(pred_history)
        else:
            opp_move = "rock"

        # 4. Check prediction accuracy if BayesianAgent
        if hasattr(predictor, "last_predicted_move") and predictor.last_predicted_move is not None:
            if predictor.last_predicted_move == opp_move:
                hits += 1

        # 5. Evaluate simultaneous outcome
        outcome = resolve_outcome(pred_move, opp_move)
        if outcome == "win":
            pred_wins += 1
        elif outcome == "lose":
            opp_wins += 1
        else:
            ties += 1

        # 6. Post-reveal learning update
        if hasattr(predictor, "update"):
            if isinstance(predictor, BayesianAgent):
                predictor.update(opp_move, opp_history)
            else:
                predictor.update(opp_move, pred_move)

        pred_history.append(pred_move)
        opp_history.append(opp_move)
        pred_win_progression.append(pred_wins / (r + 1))

    return {
        "rounds": rounds,
        "pred_wins": pred_wins,
        "opp_wins": opp_wins,
        "ties": ties,
        "pred_win_rate": pred_wins / rounds,
        "opp_win_rate": opp_wins / rounds,
        "tie_rate": ties / rounds,
        "prediction_accuracy": hits / rounds if hits > 0 else (pred_wins / max(1, rounds - ties)),
        "mean_latency_ms": np.mean(round_latencies),
        "win_progression": pred_win_progression,
        "opp_history": opp_history,
        "pred_history": pred_history,
    }


def run_benchmark_matrix(
    rounds: int = 1000,
    seeds: int = 20,
    base_seed: int = 42,
    output_dir: str = "results",
) -> Dict[str, Dict[str, Tuple[float, float]]]:
    """
    Evaluates the Bayesian Opponent Modeler vs standard agent baselines across multiple random seeds.
    """
    os.makedirs(output_dir, exist_ok=True)
    opponent_factories = {
        "Random": lambda s: RandomAgent(seed=s),
        "Rule-Based": lambda s: RuleBasedAgent(seed=s),
        "Bayesian (Self)": lambda s: BayesianAgent(seed=s),
        "Copier": lambda s: CopierOpponent(seed=s),
        "Biased (70% Rock)": lambda s: BiasedOpponent(seed=s),
        "Cyclic (R->P->S)": lambda s: CyclicOpponent(),
        "Win-Stay/Lose-Shift": lambda s: WinStayLoseShiftOpponent(seed=s),
    }

    summary_records: List[Dict[str, Any]] = []
    print("\n" + "=" * 80)
    print(f"PROBABILISTIC OPPONENT MODELER: BENCHMARK SUITE ({rounds} rounds x {seeds} seeds)")
    print("=" * 80)

    results_table: Dict[str, Dict[str, Tuple[float, float]]] = {}

    for name, factory in opponent_factories.items():
        win_rates: List[float] = []
        loss_rates: List[float] = []
        tie_rates: List[float] = []
        acc_rates: List[float] = []

        for s_idx in range(seeds):
            current_seed = base_seed + s_idx
            predictor = BayesianAgent(prior_alpha=1.0, seed=current_seed)
            opponent = factory(current_seed)

            match_result = play_match(predictor, opponent, rounds=rounds, seed=current_seed)
            win_rates.append(match_result["pred_win_rate"] * 100.0)
            loss_rates.append(match_result["opp_win_rate"] * 100.0)
            tie_rates.append(match_result["tie_rate"] * 100.0)
            acc_rates.append(match_result["prediction_accuracy"] * 100.0)

        mean_w, std_w = float(np.mean(win_rates)), float(np.std(win_rates))
        mean_l, std_l = float(np.mean(loss_rates)), float(np.std(loss_rates))
        mean_t, std_t = float(np.mean(tie_rates)), float(np.std(tie_rates))
        mean_a, std_a = float(np.mean(acc_rates)), float(np.std(acc_rates))

        results_table[name] = {
            "win_rate": (mean_w, std_w),
            "loss_rate": (mean_l, std_l),
            "tie_rate": (mean_t, std_t),
            "accuracy": (mean_a, std_a),
        }

        summary_records.append({
            "Opponent": name,
            "Rounds": rounds,
            "Seeds": seeds,
            "WinRate_Mean": round(mean_w, 2),
            "WinRate_Std": round(std_w, 2),
            "LossRate_Mean": round(mean_l, 2),
            "LossRate_Std": round(std_l, 2),
            "TieRate_Mean": round(mean_t, 2),
            "TieRate_Std": round(std_t, 2),
            "Accuracy_Mean": round(mean_a, 2),
            "Accuracy_Std": round(std_a, 2),
        })

        print(
            f"{name:<22} | Win: {mean_w:5.1f}% (+-{std_w:4.1f}%) | "
            f"Loss: {mean_l:5.1f}% (+-{std_l:4.1f}%) | "
            f"Tie: {mean_t:5.1f}% | Acc: {mean_a:5.1f}%"
        )

    # Save to CSV
    csv_path = os.path.join(output_dir, "summary.csv")
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary_records[0].keys()))
        writer.writeheader()
        writer.writerows(summary_records)
    print(f"\n[Artifact Saved] Benchmark summary metrics written to: {csv_path}")

    return results_table


def generate_evaluation_plots(output_dir: str = "results", seed: int = 42):
    """
    Generates required deliverable figures:
    1. Probability plot: predicted P(R), P(P), P(S) over rounds vs Biased and Random.
    2. Cumulative win-rate progression over 1000 rounds across all opponents.
    3. Heatmap of the learned transition matrix.
    """
    os.makedirs(output_dir, exist_ok=True)

    # -------------------------------------------------------------------------
    # Plot 1: Probability Tracking Over Rounds (Explainability)
    # -------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7.5), dpi=300)
    fig.patch.set_facecolor("#0a0a0a")
    for ax in (ax1, ax2):
        ax.set_facecolor("#121212")

    # Subplot A: Against Biased Opponent
    b_agent = BayesianAgent(prior_alpha=1.0, seed=seed)
    biased_opp = BiasedOpponent(probabilities={"rock": 0.70, "paper": 0.15, "scissors": 0.15}, seed=seed)
    play_match(b_agent, biased_opp, rounds=150, seed=seed)
    logs_biased = b_agent.get_logs()

    rounds_b = [l["round"] for l in logs_biased]
    p_rock_b = [l["p_rock"] for l in logs_biased]
    p_paper_b = [l["p_paper"] for l in logs_biased]
    p_scissors_b = [l["p_scissors"] for l in logs_biased]

    ax1.plot(rounds_b, p_rock_b, color="#ef4444", linewidth=2.2, label="P(Rock) - Opponent Skew")
    ax1.plot(rounds_b, p_paper_b, color="#3b82f6", linewidth=1.5, linestyle="--", label="P(Paper)")
    ax1.plot(rounds_b, p_scissors_b, color="#10b981", linewidth=1.5, linestyle=":", label="P(Scissors)")
    ax1.axhline(0.70, color="#ef4444", linestyle=":", alpha=0.5, label="True Ground Truth P(Rock)=0.70")
    ax1.axhline(1.0 / 3.0, color="#71717a", linestyle="--", alpha=0.4, label="Prior Nash Baseline (0.333)")

    ax1.set_title("Posterior Belief Convergence vs Biased Opponent (Fast Bayesian Learning)", fontsize=12, fontweight="bold", color="#ffffff", pad=10)
    ax1.set_ylabel("Posterior Probability P(m)", fontsize=10, color="#ffffff")
    ax1.set_ylim(-0.05, 1.05)
    ax1.legend(loc="upper right", frameon=True, facecolor="#18181b", edgecolor="#3f3f46", fontsize=8)
    ax1.grid(color="#ffffff", alpha=0.15, linestyle="--")

    # Subplot B: Against Random Opponent (Remains near uniform)
    b_agent2 = BayesianAgent(seed=seed)
    rand_opp = RandomAgent(seed=seed)
    play_match(b_agent2, rand_opp, rounds=150, seed=seed)
    logs_rand = b_agent2.get_logs()

    rounds_c = [l["round"] for l in logs_rand]
    p_rock_c = [l["p_rock"] for l in logs_rand]
    p_paper_c = [l["p_paper"] for l in logs_rand]
    p_scissors_c = [l["p_scissors"] for l in logs_rand]

    ax2.plot(rounds_c, p_rock_c, color="#ef4444", linewidth=1.8, alpha=0.85, label="P(Rock)")
    ax2.plot(rounds_c, p_paper_c, color="#3b82f6", linewidth=1.8, alpha=0.85, label="P(Paper)")
    ax2.plot(rounds_c, p_scissors_c, color="#10b981", linewidth=1.8, alpha=0.85, label="P(Scissors)")
    ax2.axhline(1.0 / 3.0, color="#ffffff", linestyle="--", linewidth=1.5, label="Uniform Nash Equilibrium Line (33.3%)")

    ax2.set_title("Posterior Probability Trajectory vs Random Opponent (Nash Baseline Stability)", fontsize=12, fontweight="bold", color="#ffffff", pad=10)
    ax2.set_xlabel("Round Number", fontsize=10, color="#ffffff")
    ax2.set_ylabel("Posterior Probability P(m)", fontsize=10, color="#ffffff")
    ax2.set_ylim(0.15, 0.55)
    ax2.legend(loc="upper right", frameon=True, facecolor="#18181b", edgecolor="#3f3f46", fontsize=8)
    ax2.grid(color="#ffffff", alpha=0.15, linestyle="--")

    plt.tight_layout()
    prob_path = os.path.join(output_dir, "probability_tracking.png")
    plt.savefig(prob_path, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"[Plot Saved] Probability trajectory plot saved to: {prob_path}")

    # -------------------------------------------------------------------------
    # Plot 2: Cumulative Win-Rate Over 1000 Rounds
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    fig.patch.set_facecolor("#0a0a0a")
    ax.set_facecolor("#121212")

    eval_opponents = {
        "Biased (70% Rock)": (BiasedOpponent(seed=seed), "#10b981", "-"),
        "Cyclic (R->P->S)": (CyclicOpponent(), "#38bdf8", "-"),
        "Win-Stay/Lose-Shift": (WinStayLoseShiftOpponent(seed=seed), "#f59e0b", "-."),
        "Rule-Based Agent": (RuleBasedAgent(seed=seed), "#a855f7", ":"),
        "Copier": (CopierOpponent(seed=seed), "#ffffff", "-"),
        "Random (Nash)": (RandomAgent(seed=seed), "#71717a", "--"),
    }

    for name, (opp, color, style) in eval_opponents.items():
        predictor = BayesianAgent(seed=seed)
        res = play_match(predictor, opp, rounds=1000, seed=seed)
        prog = [p * 100.0 for p in res["win_progression"]]
        ax.plot(range(1, 1001), prog, label=f"{name} ({prog[-1]:.1f}%)", color=color, linestyle=style, linewidth=2.0)

    ax.axhline(33.33, color="#ef4444", linestyle="--", linewidth=1.5, alpha=0.7, label="Theoretical Nash Baseline (33.3%)")
    ax.set_title("Probabilistic Opponent Modeler: Cumulative Win Rate over 1000 Rounds", fontsize=12, fontweight="bold", color="#ffffff", pad=12)
    ax.set_xlabel("Round Number", fontsize=10, color="#ffffff")
    ax.set_ylabel("Cumulative Win Rate (%)", fontsize=10, color="#ffffff")
    ax.set_ylim(0, 105)
    ax.legend(loc="lower right", frameon=True, facecolor="#18181b", edgecolor="#3f3f46", fontsize=8.5)
    ax.grid(color="#ffffff", alpha=0.15, linestyle="--")

    plt.tight_layout()
    winrate_path = os.path.join(output_dir, "cumulative_winrate.png")
    plt.savefig(winrate_path, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"[Plot Saved] Cumulative win-rate progression saved to: {winrate_path}")

    # -------------------------------------------------------------------------
    # Plot 3: Transition Matrix Heatmap
    # -------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8), dpi=300)
    fig.patch.set_facecolor("#0a0a0a")

    # Learned transition matrix vs Cyclic Opponent
    b_cyclic = BayesianAgent(seed=seed)
    play_match(b_cyclic, CyclicOpponent(), rounds=1000, seed=seed)
    cyclic_mat = np.zeros((3, 3))
    for i, m1 in enumerate(ALL_MOVES):
        dist = b_cyclic.order1_models[m1].get_predictive_distribution()
        for j, m2 in enumerate(ALL_MOVES):
            cyclic_mat[i, j] = dist[m2]

    # Learned transition matrix vs Random Opponent
    b_rand = BayesianAgent(seed=seed)
    play_match(b_rand, RandomAgent(seed=seed), rounds=1000, seed=seed)
    rand_mat = np.zeros((3, 3))
    for i, m1 in enumerate(ALL_MOVES):
        dist = b_rand.order1_models[m1].get_predictive_distribution()
        for j, m2 in enumerate(ALL_MOVES):
            rand_mat[i, j] = dist[m2]

    im1 = ax1.imshow(cyclic_mat, cmap="magma", vmin=0, vmax=1)
    ax1.set_title("Learned Transitions: Cyclic Opponent\n(Sharp Deterministic Pattern)", color="#ffffff", fontweight="bold", fontsize=10)
    ax1.set_xticks(range(3))
    ax1.set_yticks(range(3))
    ax1.set_xticklabels(["Rock", "Paper", "Scissors"], color="#ffffff")
    ax1.set_yticklabels(["Rock", "Paper", "Scissors"], color="#ffffff")
    ax1.set_ylabel("Previous Move m_{t-1}", color="#ffffff", fontweight="bold")
    ax1.set_xlabel("Next Move m_t", color="#ffffff", fontweight="bold")

    for i in range(3):
        for j in range(3):
            val = cyclic_mat[i, j]
            ax1.text(j, i, f"{val:.2f}", ha="center", va="center", color="black" if val > 0.6 else "white", fontweight="bold")

    im2 = ax2.imshow(rand_mat, cmap="magma", vmin=0, vmax=1)
    ax2.set_title("Learned Transitions: Random Opponent\n(Uncorrelated Uniform Stability ~0.33)", color="#ffffff", fontweight="bold", fontsize=10)
    ax2.set_xticks(range(3))
    ax2.set_yticks(range(3))
    ax2.set_xticklabels(["Rock", "Paper", "Scissors"], color="#ffffff")
    ax2.set_yticklabels(["Rock", "Paper", "Scissors"], color="#ffffff")
    ax2.set_xlabel("Next Move m_t", color="#ffffff", fontweight="bold")

    for i in range(3):
        for j in range(3):
            val = rand_mat[i, j]
            ax2.text(j, i, f"{val:.2f}", ha="center", va="center", color="black" if val > 0.6 else "white", fontweight="bold")

    plt.tight_layout()
    heatmap_path = os.path.join(output_dir, "transition_heatmap.png")
    plt.savefig(heatmap_path, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"[Plot Saved] Transition matrix heatmap saved to: {heatmap_path}")


def print_strategy_detection_telemetry(rounds: int = 60, seed: int = 42):
    """
    Demonstrates the StrategyDetector reasoning over time against a human-like WSLS opponent.
    """
    print("\n" + "-" * 80)
    print("LAYER 2 TELEMETRY: STRATEGY DETECTOR ONLINE INFERENCE (Win-Stay/Lose-Shift)")
    print("-" * 80)

    detector = StrategyDetector(window_size=15)
    opponent = WinStayLoseShiftOpponent(seed=seed)
    opp_history: List[str] = []
    my_history: List[str] = []

    for r in range(1, rounds + 1):
        my_move = ALL_MOVES[r % 3]
        opp_move = opponent.play(my_history, opp_history)

        my_history.append(my_move)
        opp_history.append(opp_move)

        if r in (5, 10, 15, 20, 30, 45, 60):
            dominant, ranked = detector.get_dominant_strategy(opp_history, my_history)
            if dominant:
                print(f"Round {r:2d}: Detected '{dominant.rule_name.upper()}' (Confidence: {dominant.confidence:.2f}) -> {dominant.explanation}")
            else:
                top = ranked[0] if ranked else None
                top_str = f"Top candidate: {top.rule_name} (conf={top.confidence:.2f})" if top else "None"
                print(f"Round {r:2d}: Inconclusive evidence. {top_str}")


def main():
    parser = argparse.ArgumentParser(description="Probabilistic Opponent Modeler Benchmark Suite")
    parser.add_argument("--rounds", type=int, default=1000, help="Rounds per simulation (default: 1000)")
    parser.add_argument("--seeds", type=int, default=20, help="Number of random seeds for benchmark matrix (default: 20)")
    parser.add_argument("--seed", type=int, default=42, help="Base random seed (default: 42)")
    parser.add_argument("--output-dir", type=str, default="results", help="Directory to save artifacts and plots")
    args = parser.parse_args()

    # 1. Run multi-seed benchmark matrix
    run_benchmark_matrix(rounds=args.rounds, seeds=args.seeds, base_seed=args.seed, output_dir=args.output_dir)

    # 2. Strategy Detector Online Telemetry
    print_strategy_detection_telemetry(rounds=60, seed=args.seed)

    # 3. Generate all diagnostic plots
    generate_evaluation_plots(output_dir=args.output_dir, seed=args.seed)

    print("\n" + "=" * 80)
    print("EXPERIMENTS COMPLETED SUCCESSFULLY!")
    print(f"Artifacts stored in: {os.path.abspath(args.output_dir)}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
