# Rock-Paper-Scissors Adaptive AI — Simulation Benchmark Report

Generated at: 2026-08-27 14:15:12 UTC

## Summary of Results (N=1000 Rounds Each)

| Strategy | Total Rounds | Bot Win Rate | Human Win Rate | Tie Rate | Prediction Accuracy | Order-1 Rolling Acc | Order-2 Rolling Acc | Avg Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **uniform_random** | 1000 | **32.6%** | 33.7% | 33.7% | **33.8%** | 40.0% | 35.0% | 0.0037 ms |
| **fixed_rock** | 1000 | **94.6%** | 2.7% | 2.7% | **100.0%** | 100.0% | 100.0% | 0.0033 ms |
| **cyclic** | 1000 | **94.9%** | 3.0% | 2.1% | **99.7%** | 100.0% | 100.0% | 0.0030 ms |
| **win_stay_lose_shift** | 1000 | **86.8%** | 7.9% | 5.3% | **91.5%** | 95.0% | 95.0% | 0.0031 ms |

## Key Findings & Verification

1. **Uniformly Random Opponent:**
   - Bot win rate converges precisely to **~33.3%** within binomial statistical bounds over 1000 rounds.
   - Prediction accuracy reflects theoretical baseline (~33.3%).

2. **Fixed Strategy (Always Rock):**
   - After initial cold-start exploration, Bot quickly achieves **> 90% Win Rate** by systematically playing Paper.
   - Prediction accuracy approaches ~100% (minus 8% exploration epsilon).

3. **Cyclic Strategy (Rock -> Paper -> Scissors):**
   - Order-1 Markov table $P(m_t \mid m_{t-1})$ rapidly learns the cyclic transitions.
   - Bot win rate achieves **> 85%**, significantly dominating the 33.3% random baseline.

4. **Reactive Strategy (Win-Stay, Lose-Shift):**
   - Order-2 Markov table and rolling adaptation track state transitions across multiple rounds.
   - Bot win rate achieves **> 70%**.

5. **Decision Latency:**
   - Pure functional matrix operations average **< 0.05 ms** per round, ensuring instant real-time response on both web and mobile client devices.
