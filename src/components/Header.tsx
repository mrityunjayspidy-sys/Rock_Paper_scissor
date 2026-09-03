import React from 'react';
import { Sparkles, BarChart3, RotateCcw, Video, Keyboard, Flame, Zap, Shield } from 'lucide-react';
import { SummaryStats, Difficulty } from '../ai';

interface HeaderProps {
  mode: 'camera' | 'nocamera';
  difficulty: Difficulty;
  stats: SummaryStats;
  onSwitchMode: () => void;
  onSelectDifficulty: (d: Difficulty) => void;
  onOpenStats: () => void;
  onReset: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  mode,
  difficulty,
  stats,
  onSwitchMode,
  onSelectDifficulty,
  onOpenStats,
  onReset,
}) => {
  return (
    <header className="w-full border-b border-white/10 bg-black/85 backdrop-blur-xl sticky top-0 z-40 px-4 py-3.5">
      <div className="max-w-6xl mx-auto flex flex-wrap items-center justify-between gap-4">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-white text-black flex items-center justify-center shadow-lg shadow-white/10">
            <Sparkles className="w-5 h-5 text-black" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
              RPS Adaptive AI
              <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded-full bg-white/10 text-white border border-white/20">
                Markov v2
              </span>
            </h1>
            <p className="text-xs text-neutral-400">Order-1 & Order-2 Opponent Modeling</p>
          </div>
        </div>

        {/* 3-Level Difficulty Selector */}
        <div className="flex items-center gap-1 bg-neutral-900/90 p-1 rounded-xl border border-white/10 text-xs">
          <span className="text-[11px] text-neutral-500 font-mono px-1.5 hidden sm:inline">AI:</span>
          <button
            onClick={() => onSelectDifficulty('easy')}
            className={`flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-semibold transition-all ${
              difficulty === 'easy'
                ? 'bg-neutral-800 text-white border border-white/20 shadow-sm'
                : 'text-neutral-400 hover:text-white'
            }`}
            title="Casual AI - higher randomness & forgiving play"
          >
            <Shield className="w-3 h-3 text-neutral-400" />
            <span>Easy</span>
          </button>

          <button
            onClick={() => onSelectDifficulty('normal')}
            className={`flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-semibold transition-all ${
              difficulty === 'normal'
                ? 'bg-white/20 text-white border border-white/30 font-bold'
                : 'text-neutral-400 hover:text-white'
            }`}
            title="Standard Adaptive AI - balanced Markov learning"
          >
            <Zap className="w-3 h-3 text-white" />
            <span>Normal</span>
          </button>

          <button
            onClick={() => onSelectDifficulty('hard')}
            className={`flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-bold transition-all ${
              difficulty === 'hard'
                ? 'bg-white text-black shadow-md shadow-white/10'
                : 'text-neutral-400 hover:text-white'
            }`}
            title="Mastermind AI - ruthless instant learning & counter-strategy"
          >
            <Flame className="w-3 h-3 text-current fill-current" />
            <span>Hard</span>
          </button>
        </div>

        {/* Live HUD Quick Stats */}
        <div className="flex items-center gap-3 bg-neutral-900/90 px-4 py-1.5 rounded-xl border border-white/10 text-xs">
          <div className="flex items-center gap-1.5">
            <span className="text-neutral-400">Rounds:</span>
            <span className="font-mono font-semibold text-white">{stats.totalRounds}</span>
          </div>
          <span className="text-neutral-700">|</span>
          <div className="flex items-center gap-1.5">
            <span className="text-neutral-300">You:</span>
            <span className="font-mono font-semibold text-white">
              {stats.humanWins} ({(stats.humanWinRate * 100).toFixed(0)}%)
            </span>
          </div>
          <span className="text-neutral-700">|</span>
          <div className="flex items-center gap-1.5">
            <span className="text-neutral-400">Bot:</span>
            <span className="font-mono font-semibold text-neutral-200">
              {stats.botWins} ({(stats.botWinRate * 100).toFixed(0)}%)
            </span>
          </div>
          <span className="text-neutral-700">|</span>
          <div className="flex items-center gap-1.5">
            <span className="text-neutral-500">Ties:</span>
            <span className="font-mono font-semibold text-neutral-300">{stats.ties}</span>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2">
          <button
            onClick={onSwitchMode}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium bg-neutral-900 hover:bg-neutral-800 text-neutral-200 border border-white/15 transition-all hover:border-white/30"
            title="Switch input mode"
          >
            {mode === 'camera' ? (
              <>
                <Video className="w-3.5 h-3.5 text-white" />
                <span>Camera</span>
              </>
            ) : (
              <>
                <Keyboard className="w-3.5 h-3.5 text-white" />
                <span>No Camera</span>
              </>
            )}
          </button>

          <button
            onClick={onOpenStats}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold bg-white text-black hover:bg-neutral-200 shadow-md shadow-white/10 transition-all"
          >
            <BarChart3 className="w-3.5 h-3.5" />
            <span>Stats & Export</span>
          </button>

          <button
            onClick={onReset}
            className="p-2 rounded-xl text-neutral-400 hover:text-white hover:bg-neutral-900 border border-transparent hover:border-white/10 transition-colors"
            title="Reset game state"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
};
