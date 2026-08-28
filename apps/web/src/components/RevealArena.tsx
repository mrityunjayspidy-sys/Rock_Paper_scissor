import React, { useEffect } from 'react';
import { Move, Outcome, ModelType, Difficulty } from '@rps/core';
import confetti from 'canvas-confetti';
import { Trophy, XCircle, MinusCircle, ArrowRight, Zap, Brain } from 'lucide-react';
import { sounds } from '../sound';

interface RevealArenaProps {
  difficulty: Difficulty;
  playerMove: Move;
  botMove: Move;
  predictedMove: Move;
  modelUsed: ModelType;
  outcome: Outcome;
  latencyMs: number;
  onNextRound: () => void;
}

const MOVE_DATA: Record<Move, { emoji: string; name: string }> = {
  rock: { emoji: '✊', name: 'Rock' },
  paper: { emoji: '✋', name: 'Paper' },
  scissors: { emoji: '✌️', name: 'Scissors' },
};

export const RevealArena: React.FC<RevealArenaProps> = ({
  difficulty,
  playerMove,
  botMove,
  predictedMove,
  modelUsed,
  outcome,
  latencyMs,
  onNextRound,
}) => {
  useEffect(() => {
    if (outcome === 'win') {
      sounds.playWin();
      confetti({
        particleCount: 70,
        spread: 65,
        origin: { y: 0.6 },
        colors: ['#ffffff', '#a1a1aa', '#71717a', '#d4d4d8'],
      });
    } else if (outcome === 'lose') {
      sounds.playLose();
    } else {
      sounds.playTie();
    }

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.code === 'Space' || e.code === 'Enter') {
        onNextRound();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [outcome, onNextRound]);

  const getOutcomeBanner = () => {
    switch (outcome) {
      case 'win':
        return {
          title: 'VICTORY',
          subtitle: 'You outsmarted the adaptive model this round',
          icon: <Trophy className="w-8 h-8 text-white" />,
          containerClass: 'border-white/30 bg-neutral-950/90 shadow-white/10',
        };
      case 'lose':
        return {
          title: 'DEFEAT',
          subtitle: 'The AI model anticipated your pattern',
          icon: <XCircle className="w-8 h-8 text-neutral-400" />,
          containerClass: 'border-white/15 bg-neutral-950/80',
        };
      case 'tie':
        return {
          title: 'DRAW',
          subtitle: 'Both chose the exact same move',
          icon: <MinusCircle className="w-8 h-8 text-neutral-300" />,
          containerClass: 'border-white/20 bg-neutral-950/80',
        };
    }
  };

  const banner = getOutcomeBanner();

  return (
    <div className="w-full max-w-4xl mx-auto px-4 py-8 flex flex-col items-center animate-pop-in">
      {/* Outcome Banner */}
      <div
        className={`w-full max-w-2xl p-7 rounded-3xl border backdrop-blur-xl text-center mb-8 shadow-2xl flex flex-col items-center ${banner.containerClass}`}
      >
        <div className="mb-2.5">{banner.icon}</div>
        <h2 className="text-3xl sm:text-5xl font-black font-heading text-white tracking-wider mb-1">
          {banner.title}
        </h2>
        <p className="text-sm text-neutral-400">{banner.subtitle}</p>
      </div>

      {/* Showdown Move Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-8 w-full max-w-2xl mb-8">
        {/* Player Card */}
        <div className="p-8 rounded-3xl bg-neutral-950/80 border border-white/15 flex flex-col items-center text-center shadow-xl">
          <span className="text-xs uppercase tracking-widest text-neutral-400 font-bold mb-4 font-mono">
            Your Move
          </span>
          <span className="text-7xl mb-4 select-none animate-float">
            {MOVE_DATA[playerMove].emoji}
          </span>
          <span className="text-2xl font-bold font-heading text-white">
            {MOVE_DATA[playerMove].name}
          </span>
        </div>

        {/* Bot Card */}
        <div className="p-8 rounded-3xl bg-neutral-950/80 border border-white/30 flex flex-col items-center text-center shadow-xl shadow-white/5">
          <span className="text-xs uppercase tracking-widest text-white font-bold mb-4 flex items-center gap-1 font-mono">
            <Brain className="w-3.5 h-3.5" /> Bot Move ({difficulty.toUpperCase()})
          </span>
          <span className="text-7xl mb-4 select-none animate-float">
            {MOVE_DATA[botMove].emoji}
          </span>
          <span className="text-2xl font-bold font-heading text-white">
            {MOVE_DATA[botMove].name}
          </span>
        </div>
      </div>

      {/* AI Decision Breakdown Insight Card */}
      <div className="w-full max-w-2xl p-4.5 rounded-2xl bg-neutral-950/60 border border-white/10 mb-8 text-xs text-neutral-300 grid grid-cols-1 sm:grid-cols-4 gap-3">
        <div className="flex items-center gap-2.5">
          <Zap className="w-4 h-4 text-white shrink-0" />
          <div>
            <span className="text-neutral-500 block">AI Predicted:</span>
            <span className="font-mono font-bold text-white uppercase">
              {predictedMove} {predictedMove === playerMove ? '✅' : '❌'}
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2.5">
          <Brain className="w-4 h-4 text-neutral-300 shrink-0" />
          <div>
            <span className="text-neutral-500 block">Active Model:</span>
            <span className="font-mono font-bold text-white uppercase">
              {modelUsed}
            </span>
          </div>
        </div>

        <div>
          <span className="text-neutral-500 block">Difficulty:</span>
          <span className="font-mono font-bold text-white uppercase">
            {difficulty}
          </span>
        </div>

        <div className="flex items-center gap-2.5">
          <span className="font-mono text-white font-bold text-sm">⏱</span>
          <div>
            <span className="text-neutral-500 block">Latency:</span>
            <span className="font-mono font-bold text-white">
              {latencyMs.toFixed(3)} ms
            </span>
          </div>
        </div>
      </div>

      {/* Next Round Button */}
      <button
        onClick={onNextRound}
        className="px-10 py-4 rounded-2xl bg-white text-black hover:bg-neutral-200 font-bold text-lg font-heading shadow-xl shadow-white/10 hover:-translate-y-0.5 active:scale-95 transition-all flex items-center gap-2.5"
      >
        <span>Play Next Round</span>
        <ArrowRight className="w-5 h-5 text-black" />
      </button>
      <span className="text-xs text-neutral-500 mt-2.5 font-mono">Press Space or Enter</span>
    </div>
  );
};
