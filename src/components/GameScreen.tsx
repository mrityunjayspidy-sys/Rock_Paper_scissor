import React, { useEffect } from 'react';
import { ArrowRight, Flame, Shield, Zap, BookOpen } from 'lucide-react';
import { Move, Difficulty, SummaryStats, RoundLog } from '../ai';
import { HomeStats } from './HomeStats';
import { sounds } from '../sound';

interface GameScreenProps {
  difficulty: Difficulty;
  onSelectDifficulty: (d: Difficulty) => void;
  onPlayMove: (move: Move) => void;
  stats: SummaryStats;
  logs: readonly RoundLog[];
  onOpenStats: () => void;
  onOpenAbout?: () => void;
  onResetStats: () => void;
  onDownloadJSON: () => void;
  onDownloadCSV: () => void;
}

interface MoveCardDef {
  move: Move;
  title: string;
  emoji: string;
  hotkey: string;
}

const MOVE_CARDS: MoveCardDef[] = [
  {
    move: 'rock',
    title: 'Rock (Stone)',
    emoji: '✊',
    hotkey: 'R',
  },
  {
    move: 'paper',
    title: 'Paper',
    emoji: '✋',
    hotkey: 'P',
  },
  {
    move: 'scissors',
    title: 'Scissors',
    emoji: '✌️',
    hotkey: 'S',
  },
];

export const GameScreen: React.FC<GameScreenProps> = ({
  difficulty,
  onSelectDifficulty,
  onPlayMove,
  stats,
  logs,
  onOpenStats,
  onOpenAbout,
  onResetStats,
  onDownloadJSON,
  onDownloadCSV,
}) => {
  // Global keyboard shortcuts (R, P, S)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Don't trigger if user is in an input field
      if (['INPUT', 'TEXTAREA'].includes((e.target as HTMLElement)?.tagName)) return;

      const key = e.key.toLowerCase();
      if (key === 'r') {
        sounds.playTick(500);
        onPlayMove('rock');
      } else if (key === 'p') {
        sounds.playTick(600);
        onPlayMove('paper');
      } else if (key === 's') {
        sounds.playTick(700);
        onPlayMove('scissors');
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onPlayMove]);

  const handleCardClick = (move: Move) => {
    sounds.playTick(550);
    onPlayMove(move);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 flex flex-col items-center justify-center min-h-[80vh] text-center">
      {/* Title & Tagline */}
      <h1 className="text-4xl sm:text-6xl font-black text-white tracking-tight mb-3 font-heading">
        Stone Paper <span className="underline decoration-white/30 underline-offset-8">Scissors AI</span>
      </h1>
      <p className="text-base sm:text-lg text-neutral-400 max-w-2xl mb-8">
        Can you outsmart the machine? The AI models your choices in real-time using Order-1 & Order-2 Markov tables with exponential memory decay.
      </p>

      {/* Difficulty Level Selection */}
      <div className="w-full max-w-2xl mb-8">
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
              Instant learning, aggressive multi-order counterplay.
            </p>
          </button>
        </div>
      </div>

      {/* Main Move Selection Cards */}
      <div className="w-full max-w-3xl mb-3 text-center">
        <span className="text-xs uppercase tracking-widest text-neutral-400 font-mono font-bold block mb-1">
          Choose Your Move
        </span>
        <p className="text-xs text-neutral-400 mb-6">
          Click a card or press shortcut keys <span className="font-mono text-white font-bold">[ R, P, S ]</span> on your keyboard
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 w-full max-w-3xl mb-12">
        {MOVE_CARDS.map((card) => (
          <button
            key={card.move}
            id={`play-move-${card.move}`}
            onClick={() => handleCardClick(card.move)}
            className="group relative p-8 sm:p-10 rounded-3xl bg-neutral-950/80 border border-white/10 hover:border-white/50 transition-all duration-200 flex flex-col items-center justify-center text-center shadow-xl hover:shadow-2xl hover:shadow-white/10 hover:-translate-y-2 active:scale-95"
          >
            {/* Hotkey Pill */}
            <span className="absolute top-4 right-4 px-2.5 py-1 rounded-lg bg-neutral-900 border border-white/15 text-xs font-mono font-bold text-neutral-300 group-hover:text-white group-hover:border-white/40 transition-colors">
              {card.hotkey}
            </span>

            {/* Emoji */}
            <span className="text-7xl mb-4 transform group-hover:scale-115 transition-transform duration-200 select-none">
              {card.emoji}
            </span>

            {/* Title */}
            <span className="text-2xl font-bold font-heading text-white mb-1">
              {card.title}
            </span>

            <span className="text-xs text-neutral-500 font-mono">
              [ Press {card.hotkey} ]
            </span>
          </button>
        ))}
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
                    Markov • Rules • Bayesian
                  </span>
                </h3>
                <p className="text-xs text-neutral-400 mt-0.5">
                  Explore how Adaptive Markov decision trees, symbolic strategy detection, Dirichlet Bayesian models, and Fair Play work.
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

      {/* Match Statistics & AI Telemetry Report */}
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
