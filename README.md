# Stone-Paper-Scissors AI: Adaptive Markov Engine & Probabilistic Opponent Modeller ✊✋✌️

> **Multi-Layer AI System: Real-Time Opponent Modeling, Constraint-Satisfaction Adversary, Symbolic Strategy Detection, & Bayesian Decision Theory**
> 
> *Developed by **Mrityunjay***

[![Tests](https://img.shields.io/badge/pytest-21%20passed-brightgreen.svg)](#-how-to-run)
[![TypeScript](https://img.shields.io/badge/vitest-14%20passed-blue.svg)](#-how-to-run)
[![License](https://img.shields.io/badge/license-MIT-purple.svg)](LICENSE)

---

## 🌟 1. What the Project Can Do

This project is a high-performance **Stone-Paper-Scissors artificial intelligence system** that operates both as an **interactive, real-time web application** and as a **rigorous scientific benchmark testbed** for non-cooperative game theory and probabilistic opponent modeling.

### Key Capabilities & Features:
1. **Interactive Real-Time Gameplay**:
   - Play Stone, Paper, or Scissors directly in a sleek, obsidian dark-mode interface.
   - Large tactile move cards with instant click triggers or global keyboard hotkeys (<kbd>R</kbd> for Rock/Stone, <kbd>P</kbd> for Paper, <kbd>S</kbd> for Scissors).
2. **Adaptive Opponent Modeling**:
   - The AI does **not** rely on static rules or hardcoded moves; it dynamically learns your subconscious behavioral tendencies, transition habits, and feints as you play.
3. **Three Distinct AI Difficulty Profiles**:
   - **Easy (Casual)**: Forgiving AI with higher stochastic exploration ($\varepsilon = 0.25$) and occasional blunders.
   - **Normal (Adaptive)**: Balanced Markov learning with adaptive decay ($\varepsilon = 0.10$).
   - **Hard (Mastermind)**: Aggressive pattern exploitation ($\varepsilon = 0.02$) with near-instant counterplay.
4. **Cinematic Showdown Arena**:
   - Dynamic showdown reveal displaying Player Move vs. Bot Move, winner banners, synthesized Web Audio sound effects, and celebratory confetti for victories.
   - Instant decision telemetry: Displays the AI's predicted move, the active model used (Order-1 vs. Order-2), and decision latency ($< 0.01$ ms).
   - Instant continuation via keyboard (<kbd>Space</kbd> / <kbd>Enter</kbd> to play next round, <kbd>Esc</kbd> to exit).
5. **Live Telemetry & Diagnostics Dashboard (`HomeStats`)**:
   - Real-time KPI metrics: Total rounds played, Player Win Rate, Bot Win Rate, Tie Rate, and AI Prediction Accuracy.
   - Dynamic win/loss streak badges (e.g. `🔥 4 Win Streak` or `⚡ AI Lead`).
   - Side-by-side rolling accuracy bars comparing Markov Order-1 vs. Markov Order-2 sequence models.
6. **Data Export & Privacy (1-Click CSV & JSON)**:
   - Full round-by-round match telemetry logs can be downloaded directly from the browser as standard CSV or JSON files for further analysis.
7. **In-App "About AI" Architecture Explorer**:
   - Built-in tabbed educational section detailing the game theory, Markov equations, CSP solver, symbolic rules, Bayesian mathematics, and ethics.
8. **Offline Monte Carlo Simulation & Stress Testing**:
   - Comprehensive Python experiment runner (`run_experiments.py`) that evaluates predictors across 1,000 rounds over 20 random seeds against diverse simulated opponents.

---

## 🧠 2. Algorithms & Mathematical Foundations

The system models Rock-Paper-Scissors as a **non-stationary decision process** where human decision-making consistently departs from uniform randomness due to cognitive heuristics. It applies four core algorithmic frameworks:

### 2.1 Real-Time Adaptive Markov Decision Engine (Web Client)
Implemented in [`src/ai/ai.ts`](file:///d:/FAI_Project/src/ai/ai.ts), this engine models the opponent's sequential transition patterns in real-time.

- **Order-1 Markov Transition Matrix**:  
  Calculates the conditional probability of the opponent playing move $m_t$ given their immediately preceding move $m_{t-1}$:
  $$P_1(m_t \mid m_{t-1}) = \frac{C(m_{t-1}, m_t) + \alpha}{\sum_{m'} C(m_{t-1}, m') + 3\alpha}$$
  where $\alpha = 0.05$ is Laplace smoothing parameter preventing division by zero.

- **Order-2 Markov Transition Matrix**:  
  Captures two-step historical dependencies conditioned on the previous move pair $(m_{t-2}, m_{t-1})$:
  $$P_2(m_t \mid m_{t-2}, m_{t-1}) = \frac{C(m_{t-2}, m_{t-1}, m_t) + \alpha}{\sum_{m'} C(m_{t-2}, m_{t-1}, m') + 3\alpha}$$

- **Exponential Memory Decay ($\gamma = 0.94$)**:  
  When players realize the bot is predicting them, they change their strategy. To rapidly discard stale habits, prior transition counts are exponentially discounted at every timestep:
  $$C_{t+1}(s, a) = \gamma \cdot C_t(s, a) + \mathbb{I}(s = s_t, a = a_t)$$
  With $\gamma = 0.94$, an action played 15 rounds ago retains only $39.5\%$ weight, allowing agile adaptation.

- **Dynamic Rolling Accuracy Model Selection**:  
  The engine tracks the rolling prediction accuracy of both Order-1 and Order-2 models over a sliding window ($W = 20$). If the Order-2 model demonstrates equal or superior rolling accuracy, it is automatically deployed to execute the counter-move.

- **Markov Agent Decision Hierarchy & Backoff Strategy**:  
  When resolving the predicted opponent move at round $t$, the agent evaluates historical evidence through a structured multi-tiered backoff hierarchy:
  - **Order-2 Transition Maximization**: Prioritizes localized patterns conditioned on the 2-step history $(m_{t-2}, m_{t-1})$. If the opponent previously played Paper followed by Scissors, the agent evaluates the empirical count $C((P, S) \to m)$ across $m \in \{R, P, S\}$ and selects the move with maximum frequency.
  - **Order-1 Fallback**: If the specific 2-step tuple has never been recorded, the model backs off to the 1-step condition $C(m_{t-1} \to m)$.
  - **Unigram Bias Fallback**: If the opponent's prior single move has never transitioned anywhere yet, the agent relies on the global aggregate frequency $C(m)$ (exploiting fixed human preferences, e.g., high Rock frequency).
  - **Stochastic Cold Start**: At $t=0$ where no percepts exist, it defaults to uniform random play ($1/3$ probability per action) to avoid ungrounded initial bias.

  ```
  [Round t Prediction]
           │
           ├── (m_{t-2}, m_{t-1}) observed?
           │        ├── YES ──► Argmax_m C((m_{t-2}, m_{t-1}) → m)
           │        └── NO  ──► m_{t-1} transition observed?
           │                         ├── YES ──► Argmax_m C(m_{t-1} → m)
           │                         └── NO  ──► Global counts C(m) exist?
           │                                          ├── YES ──► Argmax_m C(m)
           │                                          └── NO  ──► Uniform Random (1/3 Cold Start)
  ```

---

### 2.2 Layer 1: Constraint-Satisfaction (CSP) Adversary
Implemented in [`csp_adversary.py`](file:///d:/FAI_Project/csp_adversary.py), this module synthesizes synthetic move sequences of length $N = 1000$ to serve as an **unexploitable stress-test adversary**.

- **Search Technique**: Backtracking search with **Forward Checking**, chunk stitching (chunk size = 100), and min-conflicts fallback.
- **Three Mandatory Constraints**:
  1. **Balanced Move Distribution ($\pm 1$)**: Over 1,000 moves, each of Rock, Paper, and Scissors is used exactly 333 or 334 times, eliminating marginal frequency bias.
  2. **No Triple Repeats**: $s_i \ne s_{i-1} \lor s_{i-1} \ne s_{i-2}$. The same move never appears three times in a row.
  3. **Low Order-1 Predictability**: Transition probability ceiling $P(m_t \mid m_{t-1}) \le 0.45$.
- **Entropy-Maximizing Value Ordering**: Prioritizes assigning transitions with the lowest current occurrence count, achieving an empirical transition matrix entropy of **$H = 1.585$ bits** ($100\%$ of theoretical maximum $\log_2 3 = 1.585$).
- **Wrapped Agent**: Exposed via `AdversaryAgent(sequence)` with the standard `play(history)` interface.

---

### 2.3 Layer 2: Knowledge & Reasoning Layer (Symbolic Strategy Detection)
Implemented in [`strategy_rules.py`](file:///d:/FAI_Project/strategy_rules.py), this layer encodes formal human cognitive heuristics over a sliding history window ($W \in [10, 20]$).

- **Encoded Cognitive Rules**:
  - **Win-Stay / Lose-Shift (WSLS)**: Repeating winning choices and shifting away from losses (plus Win-Shift and Lose-Stay variants).
  - **Periodic Cycling**: Clockwise ($R \to P \to S$) or counter-clockwise cycling with detected period length.
  - **Copying & Counter-Copying**: Reactive imitation of the bot's prior actions.
  - **Biased / Constant Play**: Statistically significant deviations from uniform $1/3$ frequency.
- **Scoring & Explanation**: Each rule outputs a confidence score $[0.0, 1.0]$ and a natural language explanation (e.g., *"Opponent stayed after 4 of the last 5 wins"*).
- **`StrategyDetector` & `RuleBasedAgent`**: Combines rule outputs into ranked hypotheses. If top confidence exceeds $0.55$, it deterministically plays the optimal counter; otherwise, it falls back to a uniform random move.

---

### 2.4 Layer 3: Applied Bayesian Inference & Decision Theory
Implemented in [`bayesian_agent.py`](file:///d:/FAI_Project/bayesian_agent.py), this layer performs formal probabilistic reasoning under uncertainty.

- **Dirichlet-Multinomial Conjugate Updating**:  
  Models opponent move distributions as multinomial samples with conjugate Dirichlet priors:
  $$\boldsymbol{\alpha}_t = \boldsymbol{\alpha}_0 + \mathbf{c}_t, \quad \mathbb{E}[P(\text{move} = m)] = \frac{\alpha_{t, m}}{\sum_{k} \alpha_{t, k}}$$
  Prior parameters $\boldsymbol{\alpha}_0 = (1, 1, 1)$ represent uniform uncertainty, smoothly updating as empirical observations accumulate.

- **Contextual Markov Dirichlet Models**:  
  Maintains independent Dirichlet priors conditioned on previous moves:
  $$\text{Dirichlet}(\boldsymbol{\alpha} \mid m_{t-1} = \text{Rock}), \quad \text{Dirichlet}(\boldsymbol{\alpha} \mid m_{t-1} = \text{Paper}), \quad \text{Dirichlet}(\boldsymbol{\alpha} \mid m_{t-1} = \text{Scissors})$$

- **Adaptive Model Blending**:  
  Evaluates rolling log-loss (Brier score) between the global marginal model and the contextual Markov model, adaptively weighting the superior predictor.

- **Expected Utility Decision Theory**:  
  Instead of naively selecting the argmax move, the agent computes the expected utility across the payoff matrix ($U(\text{win}) = +1, U(\text{tie}) = 0, U(\text{loss}) = -1$):
  $$a^* = \arg\max_{a \in \{R, P, S\}} \sum_{s \in \{R, P, S\}} P(s) \cdot U(a, s)$$

- **Explainability Audit Trail (`BayesianRoundLog`)**:  
  Logs round number, predicted probabilities $(P(R), P(P), P(S))$, chosen action, opponent action, and decision latency for full transparency.

---

### 2.5 Applied & Responsible AI Framework
Documented in [`docs/responsible_ai.md`](file:///d:/FAI_Project/docs/responsible_ai.md):

- **Zero-Lookahead Fair Play**:  
  Architecturally guarantees strict simultaneous decision-making. Enforced via programmatic assertion in the game loop:
  ```python
  assert len(history) == current_round - 1, "Fair Play Violation: Lookahead detected!"
  ```
- **Data Privacy & Sovereignty**:  
  100% of telemetry data is stored in client-side `localStorage` or local CSVs; zero data is transmitted to external servers.
- **Right to Erasure (GDPR)**:  
  Includes a one-click Reset button that wipes all stored history and model parameters.
- **Epistemic Limits**:  
  Acknowledges that models fitted to one player do not generalize to others, avoiding demographic bias.

---

## 📊 3. Summary of Experimental Results (1,000 Rounds × 20 Seeds)

The primary predictor (`BayesianAgent`) was benchmarked across **20 distinct random seeds** for **1,000 rounds per match** using [`run_experiments.py`](file:///d:/FAI_Project/run_experiments.py). The full results are stored in [`results/summary.csv`](file:///d:/FAI_Project/results/summary.csv):

### Empirical Performance Table:

| Opponent Strategy | Theoretical Expectation | Bot Win Rate (Mean ± Std) | Loss Rate (Mean ± Std) | Tie Rate (Mean ± Std) | Prediction Accuracy |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Uniform Random** | Nash Equilibrium ($33.3\%$) | **33.36% ± 1.60%** | 33.53% ± 1.36% | 33.11% ± 1.36% | 33.04% ± 1.44% |
| **Rule-Based Agent** | Detectable Symbolic Patterns | **41.07% ± 2.00%** | 29.74% ± 1.50% | 29.19% ± 1.87% | 41.56% ± 1.79% |
| **Bayesian Agent (Self)**| Symmetric Bayesian Play | **33.53% ± 1.34%** | 33.25% ± 1.60% | 33.22% ± 1.53% | 33.51% ± 1.60% |
| **CSP Adversary** | High-Entropy Pseudo-Random | **46.94% ± 1.94%** | 15.29% ± 1.45% | 37.78% ± 2.62% | 48.75% ± 1.55% |
| **Biased (70% Rock)** | Skewed Marginal Distribution | **69.51% ± 1.25%** | 15.21% ± 1.00% | 15.28% ± 0.92% | 69.67% ± 1.19% |
| **Cyclic ($R \to P \to S$)** | Deterministic Periodic Pattern | **99.57% ± 0.06%** | 0.18% ± 0.06% | 0.26% ± 0.07% | 99.80% ± 0.00% |
| **Win-Stay / Lose-Shift**| Deterministic Reactive Pattern | **98.44% ± 0.55%** | 1.10% ± 0.39% | 0.46% ± 0.17% | 98.14% ± 0.53% |

---

### In-Depth Result Analysis:

1. **Nash Baseline Validation vs. Uniform Random**:
   - Against pure uncorrelated noise (`RandomAgent`), the Bayesian model records **$33.36\% \pm 1.60\%$ win rate** and **$33.04\%$ prediction accuracy**.
   - This validates that the predictor converges to the theoretical $1/3$ baseline and cannot be tricked into finding illusory patterns in truly random processes.

2. **CSP Adversary Stress-Testing**:
   - The CSP adversary successfully satisfies all constraints: transition entropy is maximized ($H = 1.585$ bits out of $\log_2 3 = 1.585$), and transition probabilities never exceed $0.336 \le 0.45$.
   - However, because the CSP strictly forbids triple repeats ($s_i \ne s_{i-1}$ when $s_{i-1} = s_{i-2}$), the Bayesian contextual model detects this **negative autocorrelation**.
   - As a result, the model pushes its win rate to **$46.94\%$** and suppresses its loss rate down to **$15.29\%$** (with $37.78\%$ ties). This demonstrates the model's remarkable sensitivity to subtle statistical structure even in highly uniform sequences.

3. **Mastery of Human Cognitive Heuristics**:
   - Against deterministic human strategies (`CyclicOpponent` and `WinStayLoseShiftOpponent`), the Bayesian agent achieves **$>98.4\%$ win rates** and near-zero losses ($<1.1\%$), mastering the opponent's strategy within fewer than 15 rounds.

4. **Generated Visual Deliverables (`results/`)**:
   - [`results/probability_tracking.png`](file:///d:/FAI_Project/results/probability_tracking.png): Shows predicted $P(R), P(P), P(S)$ converging to $70\%$ against the biased player, while staying near $33.3\%$ against the CSP adversary.
   - [`results/cumulative_winrate.png`](file:///d:/FAI_Project/results/cumulative_winrate.png): Visualizes cumulative win-rate progression across all 7 opponents over 1,000 rounds.
   - [`results/transition_heatmap.png`](file:///d:/FAI_Project/results/transition_heatmap.png): Side-by-side empirical transition heatmaps contrasting the CSP adversary with cyclic and biased opponents.

---

## 🏛️ 4. System Architecture

```mermaid
graph TD
    subgraph Environment ["Game Loop & Simultaneous Choice Boundary"]
        GL[Sequential Game Loop]
        VAL[Fair-Play Validator: Zero Lookahead Assertion]
    end

    subgraph Layer1 ["Layer 1: CSP Adversary Engine (csp_adversary.py)"]
        CSP_GEN[Backtracking Search + Forward Checking]
        C1[Constraint 1: Balance +-1]
        C2[Constraint 2: No Triple Repeats]
        C3[Constraint 3: P_next_prev <= 0.45]
        STITCH[Chunk Stitcher & Min-Conflicts]
        ADV[AdversaryAgent]
        CSP_GEN --> C1 & C2 & C3 --> STITCH --> ADV
    end

    subgraph Layer2 ["Layer 2: Knowledge & Reasoning (strategy_rules.py)"]
        HIST[Sliding Window History W=15]
        R_WSLS[Win-Stay / Lose-Shift Rule]
        R_CYC[Periodic Cycling Rule]
        R_COP[Copying / Counter-Copying Rule]
        R_BIAS[Biased Frequency Rule]
        DET[StrategyDetector: Ranked Hypotheses + Confidence]
        RULE_AGENT[RuleBasedAgent]
        HIST --> R_WSLS & R_CYC & R_COP & R_BIAS --> DET --> RULE_AGENT
    end

    subgraph Layer3 ["Layer 3: Applied Bayesian Inference (bayesian_agent.py)"]
        PRIOR[Dirichlet Prior alpha_0]
        GLOBAL_POST[Global Dirichlet-Multinomial Posterior]
        MARKOV_POST[Order-1 Contextual Dirichlet Posteriors]
        BLEND[Adaptive Model Blending: Log-Loss / Accuracy]
        EXP_UTIL[Expected Utility Best Response]
        EXPLAIN[Explainability Logger: P_R, P_P, P_S]
        PRIOR --> GLOBAL_POST & MARKOV_POST --> BLEND --> EXP_UTIL --> EXPLAIN
    end

    subgraph Interface ["Interactive Stone-Paper-Scissors Web Interface"]
        CARDS[Tactile Move Cards: Rock, Paper, Scissors]
        KEYS[Global Keyboard Hotkeys: R, P, S]
        HUD[Obsidian Luxury UI + Live Telemetry Dashboard]
    end

    ADV --> GL
    RULE_AGENT --> GL
    EXP_UTIL --> GL
    GL --> VAL
    VAL --> HIST
    VAL --> GLOBAL_POST & MARKOV_POST
```

---

## 🚀 5. How to Run Everything

### Prerequisites
- **Python 3.9+** (tested on Python 3.14)
- **Node.js v18+** (tested on Node v20/v22)

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/mrityunjayspidy-sys/Rock_Paper_scissor.git
cd Rock_Paper_scissor

# Install Python scientific dependencies
pip install -r requirements.txt

# Install Web dependencies
npm install
```

### 2. Launch Interactive Web App
```bash
npm run dev
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser for instant Stone-Paper-Scissors gameplay.

### 3. Run Benchmark Experiments & Simulations
```bash
# Run 1,000 rounds across 20 seeds (generates results/summary.csv and all plots):
python run_experiments.py --seeds 20 --rounds 1000

# Run a quick reproducible single seed:
python run_experiments.py --seed 42 --rounds 1000

# Launch interactive terminal demo with live strategy detector telemetry:
python run_experiments.py --interactive-demo
```

### 4. Run Automated Test Suites
```bash
# Run Python Pytest test suite (21 unit tests: CSP, Strategy Rules, Bayesian updates):
python -m pytest tests/

# Run TypeScript Vitest test suite (14 unit tests: Markov engine, Rules, Logger):
npm test
```

### 5. Production Web Build
```bash
npm run build
```

---

## 📂 6. Repository File Structure

```
.
├── csp_adversary.py           # Layer 1: CSP move generator & AdversaryAgent
├── strategy_rules.py          # Layer 2: Symbolic human strategy rules & StrategyDetector
├── bayesian_agent.py          # Layer 3: Dirichlet prior updates, model blending & audit log
├── opponents.py               # Benchmark agents (Random, WSLS, Cycler, Copier, Biased)
├── run_experiments.py         # 20-seed Monte Carlo experiment runner & plotter
├── docs/
│   ├── responsible_ai.md      # Responsible AI treatise: Fair play, consent & ethics
│   ├── report.pdf             # Technical project documentation PDF
│   └── plots/                 # Benchmark charts & heatmaps
├── results/                   # Generated experiment deliverables
│   ├── summary.csv            # 20-seed mean ± std win/loss/accuracy metrics
│   ├── probability_tracking.png # Bayesian posterior tracking over 1000 rounds
│   ├── cumulative_winrate.png # Cumulative win rate progression curves
│   └── transition_heatmap.png # Empirical transition matrix heatmaps
├── tests/
│   ├── test_csp.py            # Unit tests for CSP constraints & validator
│   ├── test_strategy_rules.py # Unit tests for symbolic strategy rules
│   ├── test_bayesian.py       # Unit tests for Bayesian Dirichlet posterior shifts
│   ├── test_ai.py             # Unit tests for Markov AI engine
│   └── test_rules.py          # Unit tests for game resolution logic
├── src/                       # Web application & TypeScript engine
│   ├── ai/                    # Markov AI engine, game rules, telemetry logger
│   ├── components/            # React HUD, Arena, GameScreen, About & Stats views
│   ├── App.tsx                # React application controller
│   └── main.tsx               # DOM bootstrap
├── package.json               # Node.js dependencies and script runners
├── requirements.txt           # Python scientific stack dependencies
└── README.md                  # Comprehensive system documentation
```

---

## 📄 7. License

This project is open-source software licensed under the **[MIT License](LICENSE)**.
