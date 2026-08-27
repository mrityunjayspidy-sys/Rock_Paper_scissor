import React, { useEffect } from 'react';
import { Move } from '@rps/core';
import { sounds } from '../sound';

interface NoCameraGameProps {
  onPlayMove: (move: Move) => void;
  disabled?: boolean;
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
    title: 'Rock',
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

export const NoCameraGame: React.FC<NoCameraGameProps> = ({ onPlayMove, disabled = false }) => {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (disabled) return;
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
  }, [disabled, onPlayMove]);

  const handleCardClick = (move: Move) => {
    if (disabled) return;
    sounds.playTick(550);
    onPlayMove(move);
  };

  return (
    <div className="w-full max-w-4xl mx-auto px-4 py-12 flex flex-col items-center">
      <div className="text-center mb-10">
        <h2 className="text-3xl sm:text-4xl font-bold text-white font-heading mb-2">
          Make Your Move
        </h2>
        <p className="text-sm text-neutral-400">
          Tap a card or press the corresponding shortcut key <span className="font-mono text-white font-bold">(R, P, S)</span>
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 w-full max-w-3xl">
        {MOVE_CARDS.map((card) => (
          <button
            key={card.move}
            onClick={() => handleCardClick(card.move)}
            disabled={disabled}
            className="group relative p-10 rounded-3xl bg-neutral-950/80 border border-white/10 hover:border-white/50 transition-all duration-200 flex flex-col items-center justify-center text-center shadow-xl hover:shadow-2xl hover:shadow-white/5 hover:-translate-y-1.5 active:scale-95 disabled:opacity-50 disabled:pointer-events-none"
          >
            {/* Hotkey Pill */}
            <span className="absolute top-4 right-4 px-2.5 py-1 rounded-lg bg-neutral-900 border border-white/15 text-xs font-mono font-bold text-neutral-300 group-hover:text-white group-hover:border-white/40 transition-colors">
              {card.hotkey}
            </span>

            {/* Emoji */}
            <span className="text-7xl mb-5 transform group-hover:scale-110 transition-transform duration-200 select-none">
              {card.emoji}
            </span>

            {/* Title */}
            <span className="text-2xl font-bold font-heading text-white mb-1">
              {card.title}
            </span>

            <span className="text-xs text-neutral-500 font-mono">
              [ {card.hotkey} ]
            </span>
          </button>
        ))}
      </div>
    </div>
  );
};
