# Rock-Paper-Scissors Adaptive AI ✊✋✌️

> **Opponent-Modeling Adaptive Markov AI Engine with MediaPipe Vision & Instant Auto-Detect Mode**
> 
> *Made with Love and Code by **Mrityunjay***

---

## 🌟 Highlights

- **Adaptive Opponent Modeling**: Real-time multi-order Markov transition frequency matrices — Order-1 ($P(m_t \mid m_{t-1})$) and Order-2 ($P(m_t \mid m_{t-2}, m_{t-1})$).
- **Exponential Memory Decay ($\gamma = 0.94$)**: Dynamically discounts older rounds to rapidly adapt to human counter-strategies.
- **Dynamic Rolling Accuracy Model Selection**: Evaluates rolling accuracy over a sliding window ($W=20$) and dynamically executes the superior predictor.
- **Client-Side MediaPipe Vision**: Live 60fps hand landmark tracking with a scale-invariant geometric finger-curl classifier.
- **Instant Auto-Detect Mode**: Hands-free camera play — hold a gesture for 14 frames (~0.25s) and the AI automatically triggers and counters.
- **Luxury Dark Monochrome UI**: Obsidian black design, glassmorphism HUD, Web Audio sound effects, and canvas confetti.
- **Statistical Benchmark Suite**: $N=1000$ rounds per strategy with CSV/JSON exports, latency profiling, and technical PDF report generation.

---

## 📂 Project Structure

```
.
├── src/                          # Application & Engine Source Code
│   ├── ai/                       # Markov Opponent-Modeling AI Engine (TS & Python)
│   │   ├── ai.ts                 # Multi-order Markov engine, decay, & model selection
│   │   ├── rules.ts              # Game resolution & counter move calculation
│   │   ├── classifier.ts         # Scale-invariant hand landmark finger-curl classifier
│   │   ├── logger.ts             # Telemetry round logger & CSV/JSON export
│   │   ├── types.ts              # Shared TypeScript definitions
│   │   ├── index.ts              # Module barrel exports
│   │   └── rps_ai.py             # Python Markov AI engine mirror
│   ├── components/               # React UI Components
│   │   ├── Header.tsx            # Persistent HUD (Win-rate pill & difficulty toggle)
│   │   ├── ModeSelector.tsx      # Mode selection menu (Camera vs No-Camera)
│   │   ├── NoCameraGame.tsx      # Large tactile cards + R/P/S hotkeys
│   │   ├── CameraGame.tsx        # MediaPipe Vision AI + Instant Auto-Detect
│   │   ├── RevealArena.tsx       # Showdown reveal & audio effects
│   │   └── StatsView.tsx         # Full telemetry history table & dataset exports
│   ├── sound.ts                  # Synthesized Web Audio API sound effects
│   ├── index.css                 # Dark luxury monochrome design system
│   ├── App.tsx                   # Main application controller
│   ├── main.tsx                  # React DOM entrypoint
│   ├── simulate.ts               # TypeScript benchmark simulation runner
│   └── simulate.py               # Python benchmark runner, plotter, & PDF builder
├── tests/                        # Automated Test Suites & Sample Inputs
│   ├── ai.test.ts                # Vitest Markov engine unit tests
│   ├── classifier.test.ts        # Vitest hand landmark classifier tests
│   ├── logger.test.ts            # Vitest telemetry logger tests
│   ├── rules.test.ts             # Vitest RPS game rule tests
│   ├── test_ai.py                # Pytest Markov engine tests
│   ├── test_rules.py             # Pytest game rule tests
│   └── sample_inputs/            # Sample input datasets & fixtures
│       ├── benchmark_strategies.json
│       ├── sample_hand_landmarks.json
│       └── sample_game_sessions.json
├── docs/                         # Technical Report, Screenshots, Plots & Data
│   ├── report.pdf                # Publication-quality technical documentation PDF
│   ├── screenshots/              # UI gameplay and mode screenshots
│   │   ├── camera_mode.png
│   │   ├── manual_cards_mode.png
│   │   └── statistics_dashboard.png
│   ├── plots/                    # High-resolution benchmark figures (300 DPI)
│   │   ├── win_rate_comparison.png
│   │   ├── cumulative_accuracy_progression.png
│   │   ├── transition_matrix_heatmap.png
│   │   └── decision_latency_distribution.png
│   └── report-data/              # Benchmark simulation CSV & JSON datasets
│       ├── summary_report.json / .csv
│       ├── uniform_random_1000_rounds.json / .csv
│       ├── fixed_rock_1000_rounds.json / .csv
│       ├── cyclic_1000_rounds.json / .csv
│       └── win_stay_lose_shift_1000_rounds.json / .csv
├── README.md                     # Technical overview & documentation
├── requirements.txt              # Python dependencies
├── package.json                  # Node.js dependencies & scripts
├── tsconfig.json                 # TypeScript compiler configuration
├── vite.config.ts                # Vite build and development configuration
├── index.html                    # Web entry HTML
├── .gitignore                    # Git ignore definitions
└── LICENSE                       # MIT License
```

---

## 🔬 Mathematical Approach & Formulation

### 1. Markov Transition Modeling
The AI treats human opponent play as a non-stationary Markov decision process.

- **Order-1 Transition Probability**:
  $$P_1(m_t \mid m_{t-1}) = \frac{C(m_{t-1}, m_t) + \alpha}{\sum_{m'} C(m_{t-1}, m') + 3\alpha}$$
  where $\alpha = 0.05$ is Laplace smoothing.

- **Order-2 Transition Probability**:
  $$P_2(m_t \mid m_{t-2}, m_{t-1}) = \frac{C(m_{t-2}, m_{t-1}, m_t) + \alpha}{\sum_{m'} C(m_{t-2}, m_{t-1}, m') + 3\alpha}$$

### 2. Exponential Memory Decay ($\gamma = 0.94$)
At each timestep $t$, prior observations are discounted by factor $\gamma$:
$$C_{t+1}(s, a) = \gamma \cdot C_t(s, a) + \mathbb{I}(s = s_t, a = a_t)$$
This enables the AI to rapidly discard stale habits when the player adapts.

### 3. Dynamic Model Selection & $\varepsilon$-Greedy Exploration
- Tracks rolling accuracy over a sliding window ($W=20$ rounds).
- If Order-2 demonstrates superior rolling accuracy or equal accuracy with higher confidence, the engine dynamically executes Order-2.
- An exploration parameter ($\varepsilon = 0.02$ on Hard, $\varepsilon = 0.10$ on Normal) prevents deterministic predictability.

---

## 📊 Benchmark Results ($N=1000$ Rounds Each)

| Opponent Strategy | Behavioral Pattern | Total Rounds | Bot Win Rate | Player Win Rate | Tie Rate | Prediction Accuracy | Decision Latency |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Uniform Random** | $P(\text{move}) = 1/3$ | 1000 | **35.3%** | 32.5% | 32.2% | **35.5%** | 0.0028 ms |
| **Fixed Rock** | Inflexible $m_t = \text{Rock}$ | 1000 | **92.9%** | 3.5% | 3.6% | **100.0%** | 0.0027 ms |
| **Cyclic** | Rock $\to$ Paper $\to$ Scissors | 1000 | **93.2%** | 3.5% | 3.3% | **99.7%** | 0.0027 ms |
| **Reactive (WSLS)** | Win-Stay, Lose-Shift | 1000 | **87.3%** | 6.8% | 5.9% | **92.5%** | 0.0028 ms |

---

## 🚀 How to Run

### Prerequisites
- **Node.js**: v18+ (tested on Node v20+)
- **Python**: 3.9+ (tested on Python 3.14)

### 1. Install Dependencies

```bash
# Install Node / Web dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Launch Interactive Web Game (Vite)

```bash
npm run dev
```
Open **[http://localhost:3000](http://localhost:3000)** in your browser.

### 3. Run Automated Tests

```bash
# Run TypeScript Vitest unit test suite (18+ tests):
npm test

# Run Python Pytest test suite:
python -m pytest tests/
```

### 4. Run Benchmark Simulations & Generate Report

```bash
# Run Python benchmark simulation suite, generate plots & PDF report:
python src/simulate.py

# Run TypeScript simulation runner:
npm run simulate
```

### 5. Production Web Build

```bash
npm run build
```

---

## 💻 Sample Input / Output

### Terminal Simulation Sample Output:

```
======================================================================
RUNNING ROCK-PAPER-SCISSORS BENCHMARK SUITE (N=1000 ROUNDS EACH)
======================================================================
Strategy: uniform_random         | Bot Win:  35.3% | Acc:  35.5% | Avg Lat: 0.0028ms
Strategy: fixed_rock             | Bot Win:  92.9% | Acc: 100.0% | Avg Lat: 0.0027ms
Strategy: cyclic                 | Bot Win:  93.2% | Acc:  99.7% | Avg Lat: 0.0027ms
Strategy: win_stay_lose_shift    | Bot Win:  87.3% | Acc:  92.5% | Avg Lat: 0.0028ms

All 4 benchmark plots successfully saved to: docs/plots
Technical Report PDF successfully generated at: docs/report.pdf
```

### Telemetry Record Format (`RoundLog` JSON):

```json
{
  "roundNumber": 42,
  "opponentMove": "rock",
  "predictedMove": "rock",
  "botMove": "paper",
  "result": "lose",
  "modelUsed": "order-2",
  "predictionCorrect": true,
  "decisionLatencyMs": 0.003,
  "timestamp": 1725375600000
}
```

---

## 📄 License

This project is open-source software licensed under the **[MIT License](LICENSE)**.
