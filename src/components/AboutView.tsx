import React, { useState } from 'react';
import {
  ArrowLeft,
  Brain,
  Cpu,
  Layers,
  Scale,
  ShieldCheck,
  Target,
  Sparkles,
  BarChart3,
  CheckCircle2,
  Lock,
  Eye,
  Activity,
  Terminal,
} from 'lucide-react';

interface AboutViewProps {
  onBack: () => void;
  backButtonLabel?: string;
}

type TabKey = 'overview' | 'markov' | 'csp' | 'rules' | 'bayesian' | 'vision' | 'responsible' | 'benchmarks';

export const AboutView: React.FC<AboutViewProps> = ({
  onBack,
  backButtonLabel = 'Back to Game',
}) => {
  const [activeTab, setActiveTab] = useState<TabKey>('overview');

  const tabs: { key: TabKey; label: string; icon: React.ReactNode; badge?: string }[] = [
    { key: 'overview', label: 'System Architecture', icon: <Layers className="w-4 h-4" /> },
    { key: 'markov', label: 'Adaptive Markov AI', icon: <Brain className="w-4 h-4" /> },
    { key: 'csp', label: 'CSP Adversary (Layer 1)', icon: <Cpu className="w-4 h-4" />, badge: 'Adversary' },
    { key: 'rules', label: 'Strategy Rules (Layer 2)', icon: <Activity className="w-4 h-4" /> },
    { key: 'bayesian', label: 'Bayesian Inference (Layer 3)', icon: <Target className="w-4 h-4" /> },
    { key: 'vision', label: 'MediaPipe Vision AI', icon: <Eye className="w-4 h-4" /> },
    { key: 'responsible', label: 'Responsible AI & Ethics', icon: <ShieldCheck className="w-4 h-4" /> },
    { key: 'benchmarks', label: 'Empirical Benchmarks', icon: <BarChart3 className="w-4 h-4" />, badge: '20 Seeds' },
  ];

  return (
    <div className="w-full max-w-6xl mx-auto px-4 py-8 text-left animate-fadeIn">
      {/* Top Breadcrumb & Header Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-6 border-b border-white/10 mb-8">
        <div className="flex items-center gap-3">
          <button
            onClick={onBack}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-neutral-900 hover:bg-neutral-800 text-white border border-white/10 text-xs font-semibold transition-all hover:scale-105 shadow-md"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>{backButtonLabel}</span>
          </button>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl sm:text-3xl font-black text-white font-heading tracking-tight">
                About the AI & Algorithms
              </h1>
              <span className="text-[10px] uppercase font-mono px-2.5 py-0.5 rounded-full bg-white/10 text-white border border-white/20">
                Multi-Layer Monorepo
              </span>
            </div>
            <p className="text-xs sm:text-sm text-neutral-400 mt-1">
              Probabilistic Opponent Modeller • Constraint Satisfaction • Symbolic Reasoning • Bayesian Decision Theory
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 font-mono text-xs text-neutral-400">
          <span className="px-3 py-1.5 rounded-xl bg-neutral-950 border border-white/10">
            Python 3.14 & TypeScript 5
          </span>
        </div>
      </div>

      {/* Horizontal Tab Navigation */}
      <div className="flex items-center gap-2 overflow-x-auto pb-3 mb-8 border-b border-white/5 scrollbar-thin scrollbar-thumb-white/10">
        {tabs.map((tab) => {
          const isActive = activeTab === tab.key;
          return (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`flex items-center gap-2 px-4 py-2.5 rounded-2xl text-xs font-semibold transition-all whitespace-nowrap shrink-0 border ${
                isActive
                  ? 'bg-white text-black border-white shadow-lg shadow-white/10 font-bold scale-[1.02]'
                  : 'bg-neutral-950/70 text-neutral-400 border-white/10 hover:text-white hover:border-white/30'
              }`}
            >
              {tab.icon}
              <span>{tab.label}</span>
              {tab.badge && (
                <span
                  className={`text-[9px] px-1.5 py-0.5 rounded font-mono uppercase ${
                    isActive ? 'bg-black text-white' : 'bg-white/10 text-neutral-300'
                  }`}
                >
                  {tab.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* TAB CONTENT PANELS */}
      <div className="space-y-8">
        {/* ========================================================================= */}
        {/* 1. SYSTEM ARCHITECTURE & OVERVIEW */}
        {/* ========================================================================= */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            <div className="glass-panel p-6 sm:p-8 rounded-3xl bg-neutral-950/80 border border-white/10 shadow-2xl">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 rounded-2xl bg-white/10 text-white flex items-center justify-center border border-white/20">
                  <Sparkles className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-xl font-bold text-white font-heading">
                    Probabilistic Opponent Modeller Overview
                  </h2>
                  <p className="text-xs text-neutral-400">
                    Comprehensive multi-layer artificial intelligence framework for non-cooperative sequential games
                  </p>
                </div>
              </div>

              <p className="text-sm text-neutral-300 leading-relaxed mb-6">
                In classical game theory, a two-player zero-sum game like Rock-Paper-Scissors has a unique
                Nash Equilibrium: playing moves uniformly at random (P = 1/3). However, actual human players
                repeatedly violate stationarity and randomness due to cognitive biases (such as win-stay/lose-shift,
                periodic cycling, or recency bias). This project constructs a complete, state-of-the-art
                <strong> Probabilistic Opponent Modeller</strong> structured across three distinct AI paradigms:
              </p>

              {/* 3 Architecture Cards */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div className="p-5 rounded-2xl bg-black/60 border border-white/10 hover:border-white/20 transition-all">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-mono font-bold text-neutral-400 uppercase">Layer 1</span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-white/10 text-white">CSP</span>
                  </div>
                  <h3 className="text-base font-bold text-white mb-2">Constraint Adversary</h3>
                  <p className="text-xs text-neutral-400 leading-relaxed mb-3">
                    Synthesizes 1000-move sequences via backtracking with forward checking. Enforces balance (±1),
                    no triple repeats, and bounded transition probability (P ≤ 0.45, H = 1.585 bits).
                  </p>
                  <span className="text-[11px] font-mono text-neutral-300 block">File: csp_adversary.py</span>
                </div>

                <div className="p-5 rounded-2xl bg-black/60 border border-white/10 hover:border-white/20 transition-all">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-mono font-bold text-neutral-400 uppercase">Layer 2</span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-white/10 text-white">Symbolic</span>
                  </div>
                  <h3 className="text-base font-bold text-white mb-2">Knowledge & Reasoning</h3>
                  <p className="text-xs text-neutral-400 leading-relaxed mb-3">
                    Detects cognitive heuristics over sliding history windows (WSLS, cycling, copying, bias).
                    Outputs ranked hypotheses with confidence scores [0, 1] and natural language explanations.
                  </p>
                  <span className="text-[11px] font-mono text-neutral-300 block">File: strategy_rules.py</span>
                </div>

                <div className="p-5 rounded-2xl bg-black/60 border border-white/10 hover:border-white/20 transition-all">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-mono font-bold text-neutral-400 uppercase">Layer 3</span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-white/10 text-white">Bayesian</span>
                  </div>
                  <h3 className="text-base font-bold text-white mb-2">Applied & Responsible AI</h3>
                  <p className="text-xs text-neutral-400 leading-relaxed mb-3">
                    Dirichlet-Multinomial conjugate updating, contextual Markov Dirichlet models, dynamic blending,
                    expected utility best response, explainability audit logs, and zero-lookahead fair play protocols.
                  </p>
                  <span className="text-[11px] font-mono text-neutral-300 block">File: bayesian_agent.py</span>
                </div>
              </div>

              {/* ASCII Diagram Box */}
              <div className="p-4 rounded-2xl bg-black/80 border border-white/10 font-mono text-[11px] text-neutral-300 overflow-x-auto leading-relaxed">
                <div className="text-neutral-500 mb-1">// End-to-End System Execution Flow</div>
                <div>[User Input / Vision Gesture]  &lt;---&gt;  [Simultaneous Move Engine]  &lt;---&gt;  [CSP Adversary / Test Opponents]</div>
                <div>              |                                     |</div>
                <div>              v                                     v</div>
                <div>   [Sliding Window W=15]                 [Immutable History H_&lt;t]  &lt;-- Zero Lookahead Assertion</div>
                <div>              |                                     |</div>
                <div>              v                                     v</div>
                <div>[Layer 2: Symbolic Strategy Rules]       [Layer 3: Bayesian Dirichlet Markov Modeller]</div>
                <div>   - Win-Stay / Lose-Shift (WSLS)           - Conjugate Prior α_t = α_0 + counts</div>
                <div>   - Periodic Cycling Detection             - Contextual Dirichlet Transitions</div>
                <div>   - Reactive Copying / Bias                - Expected Utility argmax E[U(a, s)]</div>
                <div>              |                                     |</div>
                <div>              +------------------+------------------+</div>
                <div>                                 |</div>
                <div>                                 v</div>
                <div>                  [Optimal Counter Move Committed]</div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* 2. ADAPTIVE MARKOV ENGINE (WEB CLIENT) */}
        {/* ========================================================================= */}
        {activeTab === 'markov' && (
          <div className="space-y-6">
            <div className="glass-panel p-6 sm:p-8 rounded-3xl bg-neutral-950/80 border border-white/10 shadow-2xl">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-2xl bg-white/10 text-white flex items-center justify-center border border-white/20">
                  <Brain className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-xl font-bold text-white font-heading">
                    Adaptive Markov Decision Engine (Web Client)
                  </h2>
                  <p className="text-xs text-neutral-400">
                    Dual multi-order transition probability matrices with exponential decay
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                {/* Order-1 */}
                <div className="p-5 rounded-2xl bg-black/60 border border-white/10">
                  <h3 className="text-sm font-bold text-white mb-2 flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-white" />
                    Order-1 Markov Transition Matrix
                  </h3>
                  <p className="text-xs text-neutral-400 leading-relaxed mb-4">
                    Models the conditional probability of the opponent&apos;s next move m_t given their immediately
                    preceding move m_(t-1).
                  </p>
                  <div className="p-3 rounded-xl bg-neutral-900 border border-white/10 font-mono text-xs text-neutral-200 mb-3">
                    P1(m_t | m_(t-1)) = [C(m_(t-1), m_t) + α] / [∑ C(m_(t-1), m&apos;) + 3α]
                  </div>
                  <p className="text-[11px] text-neutral-500">
                    Where α = 0.05 is the Laplace smoothing parameter preventing division by zero.
                  </p>
                </div>

                {/* Order-2 */}
                <div className="p-5 rounded-2xl bg-black/60 border border-white/10">
                  <h3 className="text-sm font-bold text-white mb-2 flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-white" />
                    Order-2 Markov Transition Matrix
                  </h3>
                  <p className="text-xs text-neutral-400 leading-relaxed mb-4">
                    Tracks two-step sequential dependencies m_t conditioned on context pair (m_(t-2), m_(t-1)).
                  </p>
                  <div className="p-3 rounded-xl bg-neutral-900 border border-white/10 font-mono text-xs text-neutral-200 mb-3">
                    P2(m_t | m_(t-2), m_(t-1)) = [C(m_(t-2), m_(t-1), m_t) + α] / [∑ C + 3α]
                  </div>
                  <p className="text-[11px] text-neutral-500">
                    Captures complex behavioral patterns like alternating feints and cyclic loops.
                  </p>
                </div>
              </div>

              {/* Exponential Memory Decay & Model Selection */}
              <div className="p-5 rounded-2xl bg-black/40 border border-white/10 space-y-4">
                <h3 className="text-sm font-bold text-white">Exponential Memory Decay (γ = 0.94)</h3>
                <p className="text-xs text-neutral-300 leading-relaxed">
                  Human players adapt when they notice an AI countering them. To avoid being anchored by stale habits,
                  prior observation tallies are dynamically discounted at every round:
                </p>
                <div className="p-3 rounded-xl bg-neutral-900 border border-white/10 font-mono text-xs text-white max-w-xl">
                  C_(t+1)(s, a) = γ · C_t(s, a) + 𝕀(s = s_t, a = a_t)
                </div>
                <p className="text-xs text-neutral-400">
                  With γ = 0.94, an action played 15 rounds ago retains only 39.5% weight, allowing rapid adaptation to sudden player strategy shifts.
                </p>

                <div className="pt-4 border-t border-white/10 flex flex-wrap items-center justify-between gap-4 text-xs">
                  <div>
                    <span className="text-neutral-400">Dynamic Model Selection: </span>
                    <span className="text-white font-mono font-semibold">Rolling Window W=20</span>
                  </div>
                  <div>
                    <span className="text-neutral-400">Decision Latency: </span>
                    <span className="text-white font-mono font-semibold">&lt; 0.01 ms (sub-millisecond)</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* 3. LAYER 1: CSP ADVERSARY */}
        {/* ========================================================================= */}
        {activeTab === 'csp' && (
          <div className="space-y-6">
            <div className="glass-panel p-6 sm:p-8 rounded-3xl bg-neutral-950/80 border border-white/10 shadow-2xl">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-2xl bg-white/10 text-white flex items-center justify-center border border-white/20">
                  <Cpu className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-xl font-bold text-white font-heading">
                    Layer 1: Constraint Satisfaction (CSP) Adversary
                  </h2>
                  <p className="text-xs text-neutral-400">
                    Backtracking search move generator enforcing hard mathematical constraints (csp_adversary.py)
                  </p>
                </div>
              </div>

              <p className="text-sm text-neutral-300 leading-relaxed mb-6">
                To rigorously stress-test the opponent predictor, we built a constraint-based adversary that produces
                sequences of length N = 1000 via backtracking search with forward checking, chunk stitching,
                and entropy maximization.
              </p>

              {/* 3 Mandatory Constraints */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div className="p-5 rounded-2xl bg-black/60 border border-white/10">
                  <div className="flex items-center gap-2 text-white font-bold text-sm mb-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    <span>1. Balanced Usage (±1)</span>
                  </div>
                  <p className="text-xs text-neutral-400 leading-relaxed">
                    Over N=1000, each of Rock, Paper, and Scissors is assigned exactly 333 or 334 times (differing by at most ±1),
                    preventing any stationary frequency bias from being exploited.
                  </p>
                </div>

                <div className="p-5 rounded-2xl bg-black/60 border border-white/10">
                  <div className="flex items-center gap-2 text-white font-bold text-sm mb-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    <span>2. Zero Triple Repeats</span>
                  </div>
                  <p className="text-xs text-neutral-400 leading-relaxed">
                    Hard constraint: s_i ≠ s_(i-1) or s_(i-1) ≠ s_(i-2). The same move never appears three times consecutively,
                    ruling out obvious static play.
                  </p>
                </div>

                <div className="p-5 rounded-2xl bg-black/60 border border-white/10">
                  <div className="flex items-center gap-2 text-white font-bold text-sm mb-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    <span>3. Low Predictability</span>
                  </div>
                  <p className="text-xs text-neutral-400 leading-relaxed">
                    Transition probability ceiling: P(m_t | m_(t-1)) ≤ 0.45. Achieves empirical transition matrix entropy of
                    <strong> 1.585 bits</strong> (100% of theoretical maximum log2(3) = 1.585).
                  </p>
                </div>
              </div>

              {/* Technical Execution details */}
              <div className="p-5 rounded-2xl bg-black/40 border border-white/10 space-y-4">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <Terminal className="w-4 h-4 text-neutral-400" />
                  Algorithm & Scaling Strategy
                </h3>
                <ul className="space-y-2 text-xs text-neutral-300">
                  <li className="flex items-start gap-2">
                    <span className="text-white font-mono font-bold">•</span>
                    <span><strong>Forward Checking</strong>: Prunes candidates immediately if remaining counts cannot satisfy balance or if triple repeats are detected.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-white font-mono font-bold">•</span>
                    <span><strong>Entropy-Maximizing Value Ordering</strong>: Prioritizes assigning the transition (m_(t-1), m) with the lowest current occurrence count to distribute transitions uniformly.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-white font-mono font-bold">•</span>
                    <span><strong>Chunk Stitching (Chunk Size = 100)</strong>: Solves in partitioned blocks with boundary verification, scaling effortlessly to N = 1000 in milliseconds with Min-Conflicts fallback.</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-white font-mono font-bold">•</span>
                    <span><strong>AdversaryAgent</strong>: Wraps the validated sequence into an interactive agent with the standard <code className="font-mono bg-neutral-900 px-1 py-0.5 rounded text-white">play(history)</code> interface.</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* 4. LAYER 2: KNOWLEDGE & REASONING */}
        {/* ========================================================================= */}
        {activeTab === 'rules' && (
          <div className="space-y-6">
            <div className="glass-panel p-6 sm:p-8 rounded-3xl bg-neutral-950/80 border border-white/10 shadow-2xl">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-2xl bg-white/10 text-white flex items-center justify-center border border-white/20">
                  <Activity className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-xl font-bold text-white font-heading">
                    Layer 2: Knowledge & Reasoning (Strategy Detection)
                  </h2>
                  <p className="text-xs text-neutral-400">
                    Symbolic human strategy induction rules over sliding history windows (strategy_rules.py)
                  </p>
                </div>
              </div>

              <p className="text-sm text-neutral-300 leading-relaxed mb-6">
                Psychological studies in behavioral game theory (Wang et al., 2014) reveal that humans exhibit identifiable
                reactive strategies. Layer 2 formalizes these behaviors into explicit symbolic detection rules over a sliding
                window of the last 10 to 20 rounds.
              </p>

              {/* 4 Symbolic Rules */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
                <div className="p-4 rounded-2xl bg-black/60 border border-white/10">
                  <span className="text-xs font-mono font-bold text-neutral-400 block mb-1">Rule 1</span>
                  <h3 className="text-sm font-bold text-white mb-2">Win-Stay / Lose-Shift (WSLS)</h3>
                  <p className="text-xs text-neutral-400 leading-relaxed mb-2">
                    Opponents repeat winning moves and switch away from losing moves.
                  </p>
                  <div className="p-2.5 rounded-xl bg-neutral-900 text-[11px] font-mono text-neutral-300">
                    Explanation: &quot;Opponent stayed after 4 of the last 5 wins&quot;
                  </div>
                </div>

                <div className="p-4 rounded-2xl bg-black/60 border border-white/10">
                  <span className="text-xs font-mono font-bold text-neutral-400 block mb-1">Rule 2</span>
                  <h3 className="text-sm font-bold text-white mb-2">Periodic Cycling (R → P → S)</h3>
                  <p className="text-xs text-neutral-400 leading-relaxed mb-2">
                    Detects clockwise (R → P → S) or counter-clockwise cycling with estimated period length.
                  </p>
                  <div className="p-2.5 rounded-xl bg-neutral-900 text-[11px] font-mono text-neutral-300">
                    Explanation: &quot;Clockwise cycling (R→P→S) observed in 9 of 10 rounds&quot;
                  </div>
                </div>

                <div className="p-4 rounded-2xl bg-black/60 border border-white/10">
                  <span className="text-xs font-mono font-bold text-neutral-400 block mb-1">Rule 3</span>
                  <h3 className="text-sm font-bold text-white mb-2">Copying & Counter-Copying</h3>
                  <p className="text-xs text-neutral-400 leading-relaxed mb-2">
                    Opponent imitates the bot&apos;s previous move (mirroring) or proactively counters the bot&apos;s previous move.
                  </p>
                  <div className="p-2.5 rounded-xl bg-neutral-900 text-[11px] font-mono text-neutral-300">
                    Explanation: &quot;Opponent copied my move in 8 of the last 10 rounds&quot;
                  </div>
                </div>

                <div className="p-4 rounded-2xl bg-black/60 border border-white/10">
                  <span className="text-xs font-mono font-bold text-neutral-400 block mb-1">Rule 4</span>
                  <h3 className="text-sm font-bold text-white mb-2">Biased & Constant Play</h3>
                  <p className="text-xs text-neutral-400 leading-relaxed mb-2">
                    Detects significant frequency skew where one move exceeds the 33.3% uniform baseline.
                  </p>
                  <div className="p-2.5 rounded-xl bg-neutral-900 text-[11px] font-mono text-neutral-300">
                    Explanation: &quot;Opponent heavily biased towards Rock (70.0% of recent moves)&quot;
                  </div>
                </div>
              </div>

              {/* StrategyDetector & RuleBasedAgent */}
              <div className="p-5 rounded-2xl bg-black/40 border border-white/10 text-xs text-neutral-300 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-white">StrategyDetector & RuleBasedAgent Architecture:</span>
                  <span className="font-mono text-neutral-400">Confidence Threshold: 0.55</span>
                </div>
                <p className="leading-relaxed">
                  The <code className="font-mono text-white">StrategyDetector</code> polls all active rules, computes their confidence scores,
                  and ranks them. The <code className="font-mono text-white">RuleBasedAgent</code> evaluates the top-ranked hypothesis:
                  if confidence exceeds 0.55, it deterministically plays the optimal counter-move; otherwise, it falls back to a uniform random response.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* 5. LAYER 3: BAYESIAN INFERENCE */}
        {/* ========================================================================= */}
        {activeTab === 'bayesian' && (
          <div className="space-y-6">
            <div className="glass-panel p-6 sm:p-8 rounded-3xl bg-neutral-950/80 border border-white/10 shadow-2xl">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-2xl bg-white/10 text-white flex items-center justify-center border border-white/20">
                  <Target className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-xl font-bold text-white font-heading">
                    Layer 3: Applied Bayesian Inference & Decision Theory
                  </h2>
                  <p className="text-xs text-neutral-400">
                    Conjugate Dirichlet-Multinomial prior updating & contextual Markov Dirichlet models (bayesian_agent.py)
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                {/* Prior Updating */}
                <div className="p-5 rounded-2xl bg-black/60 border border-white/10">
                  <h3 className="text-sm font-bold text-white mb-2">Conjugate Dirichlet-Multinomial Updating</h3>
                  <p className="text-xs text-neutral-400 leading-relaxed mb-3">
                    We model opponent choices as categorical samples parameterized by Dirichlet conjugate priors:
                  </p>
                  <div className="p-3 rounded-xl bg-neutral-900 border border-white/10 font-mono text-xs text-white mb-3">
                    α_t = α_0 + counts
                    <br />
                    E[P(move = m)] = α_(t, m) / ∑ α_(t, k)
                  </div>
                  <p className="text-[11px] text-neutral-400">
                    Prior parameters α_0 = (1, 1, 1) initialize uniform uninformative beliefs, shifting smoothly toward empirical counts as evidence arrives.
                  </p>
                </div>

                {/* Contextual Model */}
                <div className="p-5 rounded-2xl bg-black/60 border border-white/10">
                  <h3 className="text-sm font-bold text-white mb-2">Contextual Markov Dirichlet Model</h3>
                  <p className="text-xs text-neutral-400 leading-relaxed mb-3">
                    Extends Bayesian updating to transition contexts. Maintains 3 independent Dirichlet priors:
                  </p>
                  <div className="p-3 rounded-xl bg-neutral-900 border border-white/10 font-mono text-xs text-white mb-3">
                    Dirichlet(α | context = Rock)
                    <br />
                    Dirichlet(α | context = Paper)
                    <br />
                    Dirichlet(α | context = Scissors)
                  </div>
                  <p className="text-[11px] text-neutral-400">
                    Learns context-dependent transition behaviors while preserving Bayesian uncertainty estimates.
                  </p>
                </div>
              </div>

              {/* Decision Theory & Audit Trail */}
              <div className="p-5 rounded-2xl bg-black/40 border border-white/10 space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-bold text-white">Expected Utility Best Response</h3>
                  <span className="font-mono text-xs text-neutral-400">Payoff Matrix: Win +1, Tie 0, Loss -1</span>
                </div>
                <p className="text-xs text-neutral-300 leading-relaxed">
                  Rather than naively picking the argmax, the agent computes the expected utility of each candidate move a in [Rock, Paper, Scissors]:
                </p>
                <div className="p-3 rounded-xl bg-neutral-900 border border-white/10 font-mono text-xs text-white max-w-xl">
                  a* = argmax_a ∑ P(state) · Utility(action, state)
                </div>
                <p className="text-xs text-neutral-400">
                  Every round produces an <strong>Explainability Audit Record</strong>: logging round number, predicted probabilities (P(R), P(P), P(S)),
                  chosen move, opponent action, and decision latency.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* 6. MEDIAPIPE VISION AI */}
        {/* ========================================================================= */}
        {activeTab === 'vision' && (
          <div className="space-y-6">
            <div className="glass-panel p-6 sm:p-8 rounded-3xl bg-neutral-950/80 border border-white/10 shadow-2xl">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-2xl bg-white/10 text-white flex items-center justify-center border border-white/20">
                  <Eye className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-xl font-bold text-white font-heading">
                    MediaPipe Vision AI & Gesture Classification
                  </h2>
                  <p className="text-xs text-neutral-400">
                    Real-time 21-point hand landmark tracking running 100% on-device (classifier.ts)
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div className="p-5 rounded-2xl bg-black/60 border border-white/10">
                  <h3 className="text-sm font-bold text-white mb-2">✊ Rock Gesture</h3>
                  <p className="text-xs text-neutral-400 leading-relaxed">
                    All 4 non-thumb fingers (Index, Middle, Ring, Pinky) are curled closed. Tip-to-wrist Euclidean distance
                    is smaller than PIP joint distance.
                  </p>
                </div>

                <div className="p-5 rounded-2xl bg-black/60 border border-white/10">
                  <h3 className="text-sm font-bold text-white mb-2">✋ Paper Gesture</h3>
                  <p className="text-xs text-neutral-400 leading-relaxed">
                    All 4 non-thumb fingers are extended straight outward. Finger tips are furthest from the wrist root landmark.
                  </p>
                </div>

                <div className="p-5 rounded-2xl bg-black/60 border border-white/10">
                  <h3 className="text-sm font-bold text-white mb-2">✌️ Scissors Gesture</h3>
                  <p className="text-xs text-neutral-400 leading-relaxed">
                    Index and Middle fingers are extended outward, while Ring and Pinky fingers remain tightly curled into the palm.
                  </p>
                </div>
              </div>

              <div className="p-5 rounded-2xl bg-black/40 border border-white/10 space-y-3">
                <h3 className="text-sm font-bold text-white">Instant Auto-Detect Mode</h3>
                <p className="text-xs text-neutral-300 leading-relaxed">
                  Features a 14-frame temporal debounce (~0.25 seconds of gesture stability). When a player holds a recognizable
                  sign in front of their webcam, the vision engine locks in the gesture and immediately triggers the showdown arena
                  without requiring mouse clicks or hotkeys.
                </p>
                <div className="p-3 rounded-xl bg-neutral-900 border border-white/10 text-[11px] font-mono text-emerald-400">
                  ✓ Scale-Invariant Geometric Landmark Normalization • 60 FPS WebGL Pipeline
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* 7. RESPONSIBLE AI & FAIR PLAY */}
        {/* ========================================================================= */}
        {activeTab === 'responsible' && (
          <div className="space-y-6">
            <div className="glass-panel p-6 sm:p-8 rounded-3xl bg-neutral-950/80 border border-white/10 shadow-2xl">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-2xl bg-white/10 text-white flex items-center justify-center border border-white/20">
                  <ShieldCheck className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-xl font-bold text-white font-heading">
                    Applied & Responsible AI Framework
                  </h2>
                  <p className="text-xs text-neutral-400">
                    Ethical engineering: fair play verification, data consent, privacy, and bias limits (docs/responsible_ai.md)
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                {/* Fair Play */}
                <div className="p-5 rounded-2xl bg-black/60 border border-white/10">
                  <div className="flex items-center gap-2 text-white font-bold text-sm mb-2">
                    <Lock className="w-4 h-4 text-emerald-400" />
                    <span>Fair Play: Zero Lookahead</span>
                  </div>
                  <p className="text-xs text-neutral-400 leading-relaxed mb-3">
                    The bot must never peek at the opponent&apos;s current move before committing its action.
                  </p>
                  <div className="p-2.5 rounded-xl bg-neutral-900 font-mono text-[10px] text-neutral-300">
                    assert len(history) == round - 1
                  </div>
                </div>

                {/* Consent & Privacy */}
                <div className="p-5 rounded-2xl bg-black/60 border border-white/10">
                  <div className="flex items-center gap-2 text-white font-bold text-sm mb-2">
                    <ShieldCheck className="w-4 h-4 text-emerald-400" />
                    <span>Explicit Consent Protocol</span>
                  </div>
                  <p className="text-xs text-neutral-400 leading-relaxed mb-3">
                    User telemetry is stored purely on the client (<code className="font-mono text-white">localStorage</code>).
                  </p>
                  <p className="text-[11px] text-neutral-400">
                    Zero video stream upload. Camera frames are processed entirely in browser memory and immediately discarded.
                  </p>
                </div>

                {/* Right to Erasure */}
                <div className="p-5 rounded-2xl bg-black/60 border border-white/10">
                  <div className="flex items-center gap-2 text-white font-bold text-sm mb-2">
                    <Scale className="w-4 h-4 text-emerald-400" />
                    <span>Right to Erasure (GDPR)</span>
                  </div>
                  <p className="text-xs text-neutral-400 leading-relaxed mb-3">
                    Users can reset all model states and purge stored game logs at any time via the one-click Reset button.
                  </p>
                  <p className="text-[11px] text-neutral-400">
                    Acknowledges epistemic limits: predictions are probabilistic forecasts, not deterministic absolutes.
                  </p>
                </div>
              </div>

              <div className="p-5 rounded-2xl bg-black/40 border border-white/10 text-xs text-neutral-300 space-y-2">
                <span className="font-bold text-white block">Epistemic Uncertainty & Model Bias:</span>
                <p className="leading-relaxed">
                  A probabilistic model fitted to one player cannot be assumed to generalize across distinct individuals.
                  Internal weights are deliberately kept localized and are erased between users to eliminate bias accumulation.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================================= */}
        {/* 8. EMPIRICAL BENCHMARKS & EXPERIMENTAL RESULTS */}
        {/* ========================================================================= */}
        {activeTab === 'benchmarks' && (
          <div className="space-y-6">
            <div className="glass-panel p-6 sm:p-8 rounded-3xl bg-neutral-950/80 border border-white/10 shadow-2xl">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-2xl bg-white/10 text-white flex items-center justify-center border border-white/20">
                  <BarChart3 className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-xl font-bold text-white font-heading">
                    Empirical Benchmark Suite (1,000 Rounds × 20 Seeds)
                  </h2>
                  <p className="text-xs text-neutral-400">
                    Statistical evaluation of Bayesian Predictor across 20 distinct random seeds (results/summary.csv)
                  </p>
                </div>
              </div>

              {/* Data Table */}
              <div className="overflow-x-auto rounded-2xl border border-white/10 mb-6">
                <table className="w-full text-left text-xs font-mono">
                  <thead className="bg-neutral-900 border-b border-white/10 text-neutral-300">
                    <tr>
                      <th className="py-3 px-4 font-bold">Opponent Strategy</th>
                      <th className="py-3 px-4 font-bold">Bot Win %</th>
                      <th className="py-3 px-4 font-bold">Loss %</th>
                      <th className="py-3 px-4 font-bold">Tie %</th>
                      <th className="py-3 px-4 font-bold">Prediction Acc %</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/5 bg-black/40">
                    <tr className="hover:bg-white/5 transition-colors">
                      <td className="py-3 px-4 font-bold text-white flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-neutral-400" />
                        Uniform Random
                      </td>
                      <td className="py-3 px-4 text-white">33.36% ± 1.60%</td>
                      <td className="py-3 px-4 text-neutral-400">33.53% ± 1.36%</td>
                      <td className="py-3 px-4 text-neutral-400">33.11% ± 1.36%</td>
                      <td className="py-3 px-4 text-neutral-300">33.04% ± 1.44%</td>
                    </tr>
                    <tr className="hover:bg-white/5 transition-colors">
                      <td className="py-3 px-4 font-bold text-white flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-blue-400" />
                        Rule-Based Agent
                      </td>
                      <td className="py-3 px-4 text-white">41.07% ± 2.00%</td>
                      <td className="py-3 px-4 text-neutral-400">29.74% ± 1.50%</td>
                      <td className="py-3 px-4 text-neutral-400">29.19% ± 1.87%</td>
                      <td className="py-3 px-4 text-neutral-300">41.56% ± 1.79%</td>
                    </tr>
                    <tr className="hover:bg-white/5 transition-colors">
                      <td className="py-3 px-4 font-bold text-white flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-purple-400" />
                        Bayesian Agent (Self)
                      </td>
                      <td className="py-3 px-4 text-white">33.53% ± 1.34%</td>
                      <td className="py-3 px-4 text-neutral-400">33.25% ± 1.60%</td>
                      <td className="py-3 px-4 text-neutral-400">33.22% ± 1.53%</td>
                      <td className="py-3 px-4 text-neutral-300">33.51% ± 1.60%</td>
                    </tr>
                    <tr className="hover:bg-white/5 transition-colors bg-white/[0.02]">
                      <td className="py-3 px-4 font-bold text-white flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-amber-400" />
                        CSP Adversary
                      </td>
                      <td className="py-3 px-4 text-white font-bold">46.94% ± 1.94%</td>
                      <td className="py-3 px-4 text-neutral-400">15.29% ± 1.45%</td>
                      <td className="py-3 px-4 text-neutral-400">37.78% ± 2.62%</td>
                      <td className="py-3 px-4 text-neutral-300 font-bold">48.75% ± 1.55%</td>
                    </tr>
                    <tr className="hover:bg-white/5 transition-colors">
                      <td className="py-3 px-4 font-bold text-white flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-yellow-400" />
                        Biased (70% Rock)
                      </td>
                      <td className="py-3 px-4 text-white font-bold">69.51% ± 1.25%</td>
                      <td className="py-3 px-4 text-neutral-400">15.21% ± 1.00%</td>
                      <td className="py-3 px-4 text-neutral-400">15.28% ± 0.92%</td>
                      <td className="py-3 px-4 text-neutral-300">69.67% ± 1.19%</td>
                    </tr>
                    <tr className="hover:bg-white/5 transition-colors">
                      <td className="py-3 px-4 font-bold text-white flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-emerald-400" />
                        Cyclic (R → P → S)
                      </td>
                      <td className="py-3 px-4 text-white font-bold">99.57% ± 0.06%</td>
                      <td className="py-3 px-4 text-neutral-400">0.18% ± 0.06%</td>
                      <td className="py-3 px-4 text-neutral-400">0.26% ± 0.07%</td>
                      <td className="py-3 px-4 text-neutral-300 font-bold">99.80% ± 0.00%</td>
                    </tr>
                    <tr className="hover:bg-white/5 transition-colors">
                      <td className="py-3 px-4 font-bold text-white flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-cyan-400" />
                        Win-Stay / Lose-Shift
                      </td>
                      <td className="py-3 px-4 text-white font-bold">98.44% ± 0.55%</td>
                      <td className="py-3 px-4 text-neutral-400">1.10% ± 0.39%</td>
                      <td className="py-3 px-4 text-neutral-400">0.46% ± 0.17%</td>
                      <td className="py-3 px-4 text-neutral-300 font-bold">98.14% ± 0.53%</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              {/* Stress Test Interpretation */}
              <div className="p-5 rounded-2xl bg-black/40 border border-white/10 space-y-3">
                <h3 className="text-sm font-bold text-white">CSP Stress Test Findings</h3>
                <p className="text-xs text-neutral-300 leading-relaxed">
                  Against pure <code className="font-mono text-white">RandomAgent</code>, the predictor stays at 33.36%, proving convergence
                  to the Nash baseline when no pattern exists. Against the <code className="font-mono text-white">CSP Adversary</code>,
                  which features uniform transition probabilities (≤ 0.45) and 1.585 bits of entropy, the model achieves a
                  46.94% win rate and holds losses down to 15.29%. This occurs because the CSP rule strictly forbidding triple repeats
                  creates a subtle negative autocorrelation that the contextual Markov Dirichlet model successfully exploits.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
