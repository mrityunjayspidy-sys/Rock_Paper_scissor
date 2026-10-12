# Responsible AI in Adversarial Games: Fair Play, Data Consent, and Model Limits

> **Probabilistic Opponent Modeler — Applied & Responsible AI Framework**

---

## 1. Fair Play: Architectural Integrity & Zero Lookahead

In adversarial games such as Rock-Paper-Scissors (RPS), algorithm design must ensure **strict procedural fairness**. If an AI agent were permitted to observe the opponent's move before committing its own action (lookahead or move-peeking), the problem reduces to trivial reactive cheating rather than true sequential machine learning.

### 1.1 Formal Information Asymmetry Boundary
In our system, the game loop adheres to a simultaneous reveal protocol. At round $t$:
1. The AI agent's decision function $\pi(H_{t-1})$ takes as input **only** the historical interaction trace up to round $t-1$:
   $$H_{t-1} = \{(m_1, b_1), (m_2, b_2), \dots, (m_{t-1}, b_{t-1})\}$$
2. The agent commits its choice $b_t = \pi(H_{t-1})$ to an immutable registry **before** the opponent's move $m_t$ is sampled or dispatched.
3. The outcome $R(m_t, b_t)$ is evaluated simultaneously.

### 1.2 Programmatic Assertion Enforcement
To enforce fair play programmatically, the game loop asserts that the length of the historical action record passed to the agent never exceeds $t-1$:
```python
# Game loop fair play assertion
assert len(history) == current_round - 1, (
    f"Fair play violation! History length {len(history)} does not match round {current_round - 1}."
)
ai_move = agent.play(history)
# Opponent move is generated strictly after AI move commitment
opponent_move = opponent.play(ai_history)
```
This architectural design guarantees that the Bayesian model's predictive advantage stems solely from genuine probabilistic pattern recognition, not information leakage.

---

## 2. Human Data Consent & Privacy-by-Design

When Rock-Paper-Scissors agents are evaluated against human players (e.g., via webcam hand-gesture recognition or keyboard logging), user interaction telemetry must be protected under ethical standards and data privacy principles (e.g., GDPR, CCPA).

### 2.1 Explicit Opt-In Protocol
- **No Invisible Recording**: Telemetry tracking is disabled by default until the user explicitly consents.
- **Informed Choice**: Users are presented with a clear consent dialog disclosing:
  - What is recorded: categorical move choices (`rock`, `paper`, `scissors`), timestamps, and algorithmic prediction hit rates.
  - Why it is stored: to benchmark adaptation latency and provide personalized session analytics.
  - Where it lives: **100% Client-Side Local Storage** (`localStorage` in the browser or local CSVs). Zero server-side video uploads or third-party telemetry transmission.

```
+-------------------------------------------------------------+
|               DATA COLLECTION CONSENT PROMPT                |
|                                                             |
| Would you like to save your match telemetry to local memory?|
| [X] Save anonymized move records locally                    |
| [ ] No, play in private incognito mode                      |
|                                                             |
| Data remains 100% on your device. Never transmitted.        |
+-------------------------------------------------------------+
```

### 2.2 Right to Erasure & Zero PII
- **Right to Be Forgotten**: The web application and CLI include one-click **Reset / Erase** functionality that purges all stored logs and clears internal model parameters.
- **Zero Personally Identifiable Information (PII)**: Computer vision processing (MediaPipe 21-point hand landmarking) occurs entirely in GPU memory within the client browser; raw video frames are immediately discarded without ever persisting to disk or remote servers.

---

## 3. Epistemic Limits, Generalization, and Algorithmic Bias

### 3.1 Overfitting to Individual Playstyles
A Bayesian Dirichlet-Markov model or heuristic rule detector trained on a specific player's habits captures idiosyncratic psychological heuristics (e.g., a specific player's propensity to throw Rock after losing). 

**Risks of Transferring Model Weights**:
- **Distribution Shift**: If a trained model is transferred to a new human player, the learned priors may produce worse-than-random performance until sufficient decay or Bayesian re-weighting occurs.
- **Adversarial Exploitation**: If a human recognizes that the model has learned their prior habits, they can intentionally employ reverse psychology (e.g., switching from Win-Stay to Win-Shift), temporarily causing the AI's win rate to plummet.

### 3.2 Probabilistic Uncertainty vs. Deterministic Certainty
- Predictions in zero-sum games are inherently stochastic. Even with an Order-2 Markov model reporting $P(\text{Rock}) = 0.65$, there remains a 35% probability that the opponent selects Paper or Scissors.
- The model must convey **epistemic uncertainty** through entropy metrics $H(P)$ and confidence intervals rather than presenting decisions as guaranteed outcomes.
- Under high entropy ($H(P) \approx 1.585$ bits), the agent recognizes that the opponent is effectively playing near the Nash equilibrium and gracefully falls back to uniform randomization to avoid being exploited.
