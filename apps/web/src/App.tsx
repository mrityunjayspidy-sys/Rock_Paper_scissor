import React, { useState, useRef } from 'react';
import {
  Move,
  Outcome,
  ModelType,
  createAdaptiveAI,
  chooseMove,
  updateModel,
  resolveOutcome,
  RoundLogger,
  AdaptiveAIState,
} from '@rps/core';
import { Header } from './components/Header';
import { ModeSelector } from './components/ModeSelector';
import { NoCameraGame } from './components/NoCameraGame';
import { CameraGame } from './components/CameraGame';
import { RevealArena } from './components/RevealArena';
import { StatsView } from './components/StatsView';

type AppView = 'mode-select' | 'play' | 'reveal' | 'stats';

export const App: React.FC = () => {
  const [mode, setMode] = useState<'camera' | 'nocamera'>('nocamera');
  const [view, setView] = useState<AppView>('mode-select');

  const [aiState, setAiState] = useState<AdaptiveAIState>(() =>
    createAdaptiveAI({ gamma: 0.94, epsilon: 0.08, coldStartRounds: 10 })
  );
  const loggerRef = useRef<RoundLogger>(new RoundLogger());
  const [history, setHistory] = useState<Move[]>([]);

  // Last round outcome details for Reveal Arena
  const [lastRoundDetails, setLastRoundDetails] = useState<{
    playerMove: Move;
    botMove: Move;
    predictedMove: Move;
    modelUsed: ModelType;
    outcome: Outcome;
    latencyMs: number;
  } | null>(null);

  const stats = loggerRef.current.getStats();

  const handleSelectMode = (selectedMode: 'camera' | 'nocamera') => {
    setMode(selectedMode);
    setView('play');
  };

  const handlePlayMove = (playerMove: Move) => {
    // 1. AI decides bot move based on opponent history
    const decision = chooseMove(aiState, history);

    // 2. Resolve outcome
    const outcome = resolveOutcome(playerMove, decision.botMove);
    const predictionCorrect = decision.predictedMove === playerMove;

    // 3. Record in RoundLogger
    loggerRef.current.recordRound({
      opponentMove: playerMove,
      predictedMove: decision.predictedMove,
      botMove: decision.botMove,
      result: outcome,
      modelUsed: decision.modelUsed,
      predictionCorrect,
      decisionLatencyMs: decision.decisionLatencyMs,
    });

    // 4. Update Markov AI model
    const newAiState = updateModel(
      aiState,
      playerMove,
      decision.predictedMove,
      decision.modelUsed,
      history
    );
    setAiState(newAiState);
    setHistory((prev) => [...prev, playerMove]);

    // 5. Store for Reveal Arena
    setLastRoundDetails({
      playerMove,
      botMove: decision.botMove,
      predictedMove: decision.predictedMove,
      modelUsed: decision.modelUsed,
      outcome,
      latencyMs: decision.decisionLatencyMs,
    });

    setView('reveal');
  };

  const handleNextRound = () => {
    setView('play');
  };

  const handleReset = () => {
    setAiState(createAdaptiveAI({ gamma: 0.94, epsilon: 0.08, coldStartRounds: 10 }));
    loggerRef.current.clear();
    setHistory([]);
    setLastRoundDetails(null);
    setView('mode-select');
  };

  const handleDownloadJSON = () => {
    const jsonStr = loggerRef.current.exportJSON();
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `rps_game_logs_${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleDownloadCSV = () => {
    const csvStr = loggerRef.current.exportCSV();
    const blob = new Blob([csvStr], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `rps_game_logs_${Date.now()}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen flex flex-col bg-black text-white selection:bg-white selection:text-black">
      {view !== 'mode-select' && (
        <Header
          mode={mode}
          stats={stats}
          onSwitchMode={() => setView('mode-select')}
          onOpenStats={() => setView('stats')}
          onReset={handleReset}
        />
      )}

      <main className="flex-1 flex flex-col justify-center">
        {view === 'mode-select' && <ModeSelector onSelectMode={handleSelectMode} />}

        {view === 'play' && mode === 'nocamera' && <NoCameraGame onPlayMove={handlePlayMove} />}

        {view === 'play' && mode === 'camera' && <CameraGame onPlayMove={handlePlayMove} />}

        {view === 'reveal' && lastRoundDetails && (
          <RevealArena
            playerMove={lastRoundDetails.playerMove}
            botMove={lastRoundDetails.botMove}
            predictedMove={lastRoundDetails.predictedMove}
            modelUsed={lastRoundDetails.modelUsed}
            outcome={lastRoundDetails.outcome}
            latencyMs={lastRoundDetails.latencyMs}
            onNextRound={handleNextRound}
          />
        )}

        {view === 'stats' && (
          <StatsView
            logs={loggerRef.current.getLogs()}
            stats={stats}
            onBack={() => setView('play')}
            onDownloadJSON={handleDownloadJSON}
            onDownloadCSV={handleDownloadCSV}
          />
        )}
      </main>

      <footer className="py-5 border-t border-white/10 text-center text-xs text-neutral-400 font-mono">
        Rock-Paper-Scissors Adaptive AI &copy; 2026 • Made With Love And Code by <span className="text-white font-semibold">Mrityunjay</span>
      </footer>
    </div>
  );
};

export default App;
