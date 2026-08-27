import React from 'react';
import { Camera, Keyboard, Brain, Cpu, ShieldCheck, ArrowRight } from 'lucide-react';

interface ModeSelectorProps {
  onSelectMode: (mode: 'camera' | 'nocamera') => void;
}

export const ModeSelector: React.FC<ModeSelectorProps> = ({ onSelectMode }) => {
  return (
    <div className="max-w-4xl mx-auto px-4 py-16 flex flex-col items-center justify-center min-h-[80vh] text-center">
      <h1 className="text-4xl sm:text-6xl font-black text-white tracking-tight mb-4 font-heading">
        Beat the <span className="underline decoration-white/30 underline-offset-8">Adaptive AI</span>
      </h1>
      <p className="text-base sm:text-lg text-neutral-400 max-w-2xl mb-12">
        The bot analyzes your past move sequences using Order-1 & Order-2 Markov frequency tables with exponential decay (γ=0.94) to predict and counter your next move.
      </p>

      {/* Mode Selection Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-3xl">
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
    </div>
  );
};
