import React from 'react';
import { Camera, Keyboard, Brain, Cpu, ShieldCheck, ArrowRight, Flame, Shield, Zap, Play, BookOpen } from 'lucide-react';
import { Difficulty, SummaryStats, RoundLog } from '../ai';
import { HomeStats } from './HomeStats';

interface ModeSelectorProps {
  difficulty: Difficulty;
  onSelectDifficulty: (d: Difficulty) => void;
  onSelectMode: (mode: 'camera' | 'nocamera') => void;
  stats: SummaryStats;
  logs: readonly RoundLog[];
  onOpenStats: () => void;
  onOpenAbout?: () => void;
  onResetStats: () => void;
  onDownloadJSON: () => void;
  onDownloadCSV: () => void;
}

export const ModeSelector: React.FC<ModeSelectorProps> = ({
  difficulty,
  onSelectDifficulty,
  onSelectMode,
  stats,
  logs,
  onOpenStats,
  onOpenAbout,
  onResetStats,
  onDownloadJSON,
  onDownloadCSV,
}) => {
  return (
    <div className="max-w-4xl mx-auto px-4 py-12 flex flex-col items-center justify-center min-h-[80vh] text-center">
      <h1 className="text-4xl sm:text-6xl font-black text-white tracking-tight mb-3 font-heading">
        Beat the <span className="underline decoration-white/30 underline-offset-8">Adaptive AI</span>
      </h1>
      <p className="text-base sm:text-lg text-neutral-400 max-w-2xl mb-8">
        The bot learns from your past move sequences using Order-1 & Order-2 Markov tables with exponential decay to anticipate and counter your next move.
      </p>

      {/* Difficulty Level Selection */}
      <div className="w-full max-w-2xl mb-10">
        <span className="text-xs uppercase tracking-widest text-neutral-400 font-mono font-bold block mb-3">
          Select AI Difficulty Level
        </span>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {/* Easy */}
          <button
            onClick={() => onSelectDifficulty('easy')}
            className={`p-4 rounded-2xl border text-left transition-all flex flex-col justify-between ${
              difficulty === 'easy'
                ? 'bg-neutral-900 border-white text-white ring-2 ring-white/20'
                : 'bg-neutral-950/60 border-white/10 text-neutral-400 hover:border-white/30 hover:text-neutral-200'
            }`}
          >
            <div className="flex items-center justify-between mb-1.5">
              <span className="font-bold font-heading text-base flex items-center gap-1.5">
                <Shield className="w-4 h-4 text-neutral-300" /> Easy
              </span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/10">Casual</span>
            </div>
            <p className="text-xs text-neutral-400">Forgiving AI with higher randomness and blunders.</p>
          </button>

          {/* Normal */}
          <button
            onClick={() => onSelectDifficulty('normal')}
            className={`p-4 rounded-2xl border text-left transition-all flex flex-col justify-between ${
              difficulty === 'normal'
                ? 'bg-neutral-900 border-white text-white ring-2 ring-white/20'
                : 'bg-neutral-950/60 border-white/10 text-neutral-400 hover:border-white/30 hover:text-neutral-200'
            }`}
          >
            <div className="flex items-center justify-between mb-1.5">
              <span className="font-bold font-heading text-base flex items-center gap-1.5">
                <Zap className="w-4 h-4 text-white" /> Normal
              </span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/10">Adaptive</span>
            </div>
            <p className="text-xs text-neutral-400">Balanced Markov opponent modeling with decay.</p>
          </button>

          {/* Hard */}
          <button
            onClick={() => onSelectDifficulty('hard')}
            className={`p-4 rounded-2xl border text-left transition-all flex flex-col justify-between ${
              difficulty === 'hard'
                ? 'bg-white text-black border-white ring-2 ring-white/40 shadow-lg shadow-white/10'
                : 'bg-neutral-950/60 border-white/10 text-neutral-400 hover:border-white/30 hover:text-neutral-200'
            }`}
          >
            <div className="flex items-center justify-between mb-1.5">
              <span className="font-bold font-heading text-base flex items-center gap-1.5">
                <Flame className={`w-4 h-4 ${difficulty === 'hard' ? 'text-black fill-current' : 'text-white'}`} /> Hard
              </span>
              <span className={`text-[10px] font-mono px-2 py-0.5 rounded ${difficulty === 'hard' ? 'bg-black text-white font-bold' : 'bg-white/10'}`}>
                Ruthless
              </span>
            </div>
            <p className={`text-xs ${difficulty === 'hard' ? 'text-neutral-800 font-medium' : 'text-neutral-400'}`}>
              Instant learning from round 2, aggressive multi-order counterplay.
            </p>
          </button>
        </div>
      </div>

      {/* Mode Selection Cards (Playing Block) */}
      <div className="w-full max-w-3xl mb-4 text-center">
        <span className="text-xs uppercase tracking-widest text-neutral-400 font-mono font-bold block mb-1">
          Start Playing • Select Input Mode
        </span>
        <p className="text-xs text-neutral-400 mb-6">
          Choose between gesture camera detection or keyboard shortcuts to begin your match against the AI.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-3xl mb-12">
        {/* Camera Mode */}
        <button
          onClick={() => onSelectMode('camera')}
          className="group relative p-8 rounded-3xl bg-neutral-950/80 border border-white/10 hover:border-white/40 transition-all duration-300 text-left hover:shadow-2xl hover:shadow-white/5 hover:-translate-y-1 flex flex-col justify-between"
        >
          <div>
            <div className="w-14 h-14 rounded-2xl bg-white/10 border border-white/20 flex items-center justify-center mb-6 group-hover:scale-105 group-hover:bg-white group-hover:text-black transition-all">
              <Camera className="w-7 h-7 text-white group-hover:text-black transition-colors" />
            </div>
            <div className="flex items-center justify-between mb-2">
              <h2 className="text-2xl font-bold text-white font-heading">Camera Mode</h2>
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-white text-black">
                Vision AI
              </span>
            </div>
            <p className="text-sm text-neutral-400 mb-6 leading-relaxed">
              Instant hand gesture detection via MediaPipe Vision. Features instant auto-trigger and 3-2-1 countdown.
            </p>
          </div>

          <div className="space-y-2.5 border-t border-white/10 pt-4 text-xs text-neutral-300">
            <div className="flex items-center gap-2">
              <Cpu className="w-3.5 h-3.5 text-white" />
              <span>Real-time 21-point hand landmark tracking</span>
            </div>
            <div className="flex items-center gap-2">
              <ShieldCheck className="w-3.5 h-3.5 text-white" />
              <span>100% Client-side, zero video upload</span>
            </div>
          </div>
        </button>

        {/* No Camera Mode */}
        <button
          onClick={() => onSelectMode('nocamera')}
          className="group relative p-8 rounded-3xl bg-neutral-950/80 border border-white/10 hover:border-white/40 transition-all duration-300 text-left hover:shadow-2xl hover:shadow-white/5 hover:-translate-y-1 flex flex-col justify-between"
        >
          <div>
            <div className="w-14 h-14 rounded-2xl bg-white/10 border border-white/20 flex items-center justify-center mb-6 group-hover:scale-105 group-hover:bg-white group-hover:text-black transition-all">
              <Keyboard className="w-7 h-7 text-white group-hover:text-black transition-colors" />
            </div>
            <div className="flex items-center justify-between mb-2">
              <h2 className="text-2xl font-bold text-white font-heading">No Camera</h2>
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-neutral-800 text-neutral-200 border border-white/15">
                Keyboard & Tap
              </span>
            </div>
            <p className="text-sm text-neutral-400 mb-6 leading-relaxed">
              Play using large tactile targets or keyboard shortcuts (R for Rock, P for Paper, S for Scissors).
            </p>
          </div>

          <div className="space-y-2.5 border-t border-white/10 pt-4 text-xs text-neutral-300">
            <div className="flex items-center gap-2">
              <Brain className="w-3.5 h-3.5 text-white" />
              <span>Full Order-1 & Order-2 Markov AI engine</span>
            </div>
            <div className="flex items-center gap-2">
              <ArrowRight className="w-3.5 h-3.5 text-white" />
              <span>Instant showdown & decision latency logs</span>
            </div>
          </div>
        </button>
      </div>

      {/* AI Architecture & Algorithms Explorer Banner */}
      {onOpenAbout && (
        <div className="w-full max-w-4xl mx-auto mb-8">
          <div className="p-4 sm:p-5 rounded-3xl bg-neutral-950/80 border border-white/10 hover:border-white/20 transition-all flex flex-wrap items-center justify-between gap-4 text-left shadow-2xl backdrop-blur-xl">
            <div className="flex items-center gap-3.5">
              <div className="w-10 h-10 rounded-2xl bg-white/10 border border-white/20 flex items-center justify-center text-white shrink-0">
                <BookOpen className="w-5 h-5 text-white" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  About the AI Architecture & Algorithms
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-white/10 text-white border border-white/20">
                    CSP • Rules • Bayesian
                  </span>
                </h3>
                <p className="text-xs text-neutral-400 mt-0.5">
                  Explore how Constraint Satisfaction, symbolic strategy detection, Dirichlet Markov models, and Fair Play work.
                </p>
              </div>
            </div>
            <button
              id="home-open-about-btn"
              onClick={onOpenAbout}
              className="px-4 py-2 rounded-xl bg-white text-black hover:bg-neutral-200 text-xs font-bold flex items-center gap-1.5 transition-all shadow-md shadow-white/10 hover:scale-105"
            >
              <span>Explore Architecture</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}

      {/* Match Statistics & AI Telemetry Report (Below the Playing Block) */}
      <HomeStats
        stats={stats}
        logs={logs}
        difficulty={difficulty}
        onOpenStats={onOpenStats}
        onResetStats={onResetStats}
        onDownloadJSON={onDownloadJSON}
        onDownloadCSV={onDownloadCSV}
      />
    </div>
  );
};
