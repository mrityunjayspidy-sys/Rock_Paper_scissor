# Rock-Paper-Scissors Adaptive AI ✊✋✌️

> **Opponent-Modeling Adaptive Markov AI Engine with MediaPipe Vision & Instant Auto-Detect Mode**
> 
> *Made with Love and Code by **Mrityunjay***

---

## 🌟 Highlights

- **Adaptive Opponent Modeling**: Real-time Markov Order-1 ($P(m_t \mid m_{t-1})$) and Order-2 ($P(m_t \mid m_{t-2}, m_{t-1})$) transition frequency matrices.
- **Exponential Decay ($\gamma = 0.94$)**: Dynamically discounts older rounds to continuously adapt to human player counter-strategies.
- **Rolling Accuracy Model Selection**: Tracks rolling predictive accuracy for both models and dynamically chooses the superior model.
- **Client-Side MediaPipe Tasks Vision**: Live 60fps hand landmark tracking with a scale-invariant geometric finger-curl classifier.
- **Instant Auto-Detect Mode**: Hands-free camera play — hold Rock, Paper, or Scissors for 0.25s and the AI automatically recognizes the move and counters instantly.
- **Monochrome Luxury Design**: Ultra-sleek obsidian black, crisp white typography, and glassmorphism interface.
- **Statistical Benchmark Suite**: Fully reproducible simulations ($N=1000$ rounds) against uniform random, fixed, cyclic, and reactive strategies with CSV/JSON exports in `docs/report-data/`.

---

## 📂 Monorepo Structure

```
.
├── packages/
│   └── core/                     # Shared TypeScript Engine (Zero I/O, Pure Functions)
│       ├── src/
│       │   ├── types.ts          # Move, Outcome, ModelType, RoundLog, AIState
│       │   ├── rules.ts          # Game resolution & counter move calculation
│       │   ├── ai.ts             # Markov AI engine (Order-1, Order-2, Decay, ε-Greedy)
│       │   ├── logger.ts         # RoundLogger, KPI metrics, JSON/CSV exports
│       │   ├── classifier.ts     # Geometric hand landmark finger-curl classifier
│       │   └── simulate.ts       # N=1000 rounds simulation runner
│       └── test/                 # 18 Vitest unit tests (100% pass)
├── apps/
│   ├── web/                      # React 18 + Vite + TypeScript Web Application
│   │   ├── src/
│   │   │   ├── components/
│   │   │   │   ├── Header.tsx        # Persistent HUD (Win-rate pill & mode toggle)
│   │   │   │   ├── ModeSelector.tsx  # Minimalist mode selection screen
│   │   │   │   ├── NoCameraGame.tsx  # Large tactile cards + R/P/S hotkeys
│   │   │   │   ├── CameraGame.tsx    # MediaPipe Vision AI + Instant Auto-Detect
│   │   │   │   ├── RevealArena.tsx   # Synchronized showdown reveal & audio effects
│   │   │   │   └── StatsView.tsx     # Full history table & CSV/JSON export
│   │   │   ├── sound.ts          # Synthesized Web Audio API sound effects
│   │   │   └── index.css         # Dark luxury monochrome design system
│   └── mobile/                   # React Native (Expo) Mobile App
│       └── App.tsx               # Touch controls, camera gesture mode & native exports
├── scripts/
│   └── simulate_benchmarks.py    # Python benchmark suite & statistical validation
└── docs/
    └── report-data/              # Generated benchmark simulation datasets
        ├── summary_report.json / .csv
        ├── uniform_random_1000_rounds.json / .csv
        ├── fixed_rock_1000_rounds.json / .csv
        ├── cyclic_1000_rounds.json / .csv
        └── win_stay_lose_shift_1000_rounds.json / .csv
```

---

## 📊 Benchmark Simulation Results ($N=1000$ Rounds Each)

| Strategy | Opponent Pattern | Total Rounds | Bot Win Rate | Player Win Rate | Tie Rate | Prediction Accuracy | Decision Latency |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Uniform Random** | $P(\text{move}) = 1/3$ | 1000 | **32.6%** | 33.7% | 33.7% | **33.8%** | 0.0037 ms |
| **Fixed Rock** | Always plays Rock | 1000 | **94.6%** | 2.7% | 2.7% | **100.0%** | 0.0033 ms |
| **Cyclic** | Rock $\to$ Paper $\to$ Scissors | 1000 | **94.9%** | 3.0% | 2.1% | **99.7%** | 0.0030 ms |
| **Reactive (WSLS)** | Win-Stay, Lose-Shift | 1000 | **86.8%** | 7.9% | 5.3% | **91.5%** | 0.0031 ms |

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
npm install
```

### 2. Run Web App (Vite Dev Server)
```bash
npm run web:dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

### 3. Run Unit Tests
```bash
npm run test --workspace=@rps/core
```

### 4. Run Benchmark Simulations
```bash
# TypeScript Simulation:
npm run simulate

# Python Simulation & Report Generation:
python scripts/simulate_benchmarks.py
```

### 5. Build for Production
```bash
npm run web:build
```

---

## 📜 License & Credits

Built with ❤️ and Code by **Mrityunjay** © 2026.
All rights reserved.
