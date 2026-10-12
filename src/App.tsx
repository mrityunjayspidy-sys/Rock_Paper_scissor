import React, { useState, useRef, useMemo } from 'react';
import {
  Move,
  Outcome,
  ModelType,
  Difficulty,
  DIFFICULTY_CONFIGS,
  createAdaptiveAI,
  chooseMove,
  updateModel,
  resolveOutcome,
  RoundLogger,
  RoundLog,
  AdaptiveAIState,
  calculateSummaryStats,
  loadSavedLogs,
  saveLogs,
  clearSavedLogs,
  reconstructAiState,
} from './ai';
import { Header } from './components/Header';
import { ModeSelector } from './components/ModeSelector';
import { NoCameraGame } from './components/NoCameraGame';
import { CameraGame } from './components/CameraGame';
import { RevealArena } from './components/RevealArena';
import { StatsView } from './components/StatsView';

type AppView = 'mode-select' | 'play' | 'reveal' | 'stats';

export const App: React.FC = () => {
  const [mode, setMode] = useState<'camera' | 'nocamera'>('nocamera');
  const [difficulty, setDifficulty] = useState<Difficulty>('normal');
  const [view, setView] = useState<AppView>('mode-select');
  const [previousView, setPreviousView] = useState<AppView>('mode-select');

  // Load persisted round logs
  const [logs, setLogs] = useState<RoundLog[]>(() => loadSavedLogs());

  // Initialize Adaptive AI state (reconstructing Markov state if logs exist)
  const [aiState, setAiState] = useState<AdaptiveAIState>(() => {
    if (logs.length > 0) {
      return reconstructAiState(logs, 'normal').aiState;
    }
    return createAdaptiveAI('normal');
  });

  const loggerRef = useRef<RoundLogger>(new RoundLogger(logs));
  const [history, setHistory] = useState<Move[]>(() => logs.map((l) => l.opponentMove));

  // Last round outcome details for Reveal Arena
  const [lastRoundDetails, setLastRoundDetails] = useState<{
    playerMove: Move;
    botMove: Move;
    predictedMove: Move;
    modelUsed: ModelType;
    outcome: Outcome;
    latencyMs: number;
  } | null>(null);

  // Reactive stats computation
  const stats = useMemo(() => calculateSummaryStats(logs), [logs]);

  const handleSelectDifficulty = (newDifficulty: Difficulty) => {
    setDifficulty(newDifficulty);
    setAiState((prev) => ({
      ...prev,
      config: { ...DIFFICULTY_CONFIGS[newDifficulty] },
    }));
  };

  const handleSelectMode = (selectedMode: 'camera' | 'nocamera') => {
    setMode(selectedMode);
    setView('play');
  };

  const handleOpenStats = () => {
    setPreviousView(view);
    setView('stats');
  };

  const handleBackFromStats = () => {
    setView(previousView === 'stats' ? 'mode-select' : previousView);
  };

  const handlePlayMove = (playerMove: Move) => {
    // 1. AI decides bot move based on opponent history & difficulty
    const decision = chooseMove(aiState, history);

    // 2. Resolve outcome
    const outcome = resolveOutcome(playerMove, decision.botMove);
    const predictionCorrect = decision.predictedMove === playerMove;

    // 3. Record in RoundLogger and persist to localStorage
    loggerRef.current.recordRound({
      opponentMove: playerMove,
      predictedMove: decision.predictedMove,
      botMove: decision.botMove,
      result: outcome,
      modelUsed: decision.modelUsed,
      predictionCorrect,
      decisionLatencyMs: decision.decisionLatencyMs,
    });

    const currentLogs = [...loggerRef.current.getLogs()];
    setLogs(currentLogs);
    saveLogs(currentLogs);

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

  const handleBackToHome = () => {
    setView('mode-select');
  };

  const handleNextRound = () => {
    setView('play');
  };

  const handleReset = () => {
    setAiState(createAdaptiveAI(difficulty));
    loggerRef.current.clear();
    clearSavedLogs();
    setLogs([]);
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
      <Header
        mode={mode}
        difficulty={difficulty}
        stats={stats}
        onSwitchMode={() => setView('mode-select')}
        onSelectDifficulty={handleSelectDifficulty}
        onOpenStats={handleOpenStats}
        onReset={handleReset}
        onExitGame={handleBackToHome}
        isHomePage={view === 'mode-select'}
      />

      <main className="flex-1 flex flex-col justify-center">
        {view === 'mode-select' && (
          <ModeSelector
            difficulty={difficulty}
            onSelectDifficulty={handleSelectDifficulty}
            onSelectMode={handleSelectMode}
            stats={stats}
            logs={logs}
            onOpenStats={handleOpenStats}
            onResetStats={handleReset}
            onDownloadJSON={handleDownloadJSON}
            onDownloadCSV={handleDownloadCSV}
          />
        )}

        {view === 'play' && mode === 'nocamera' && (
          <NoCameraGame
            difficulty={difficulty}
            onPlayMove={handlePlayMove}
            onBackToHome={handleBackToHome}
          />
        )}

        {view === 'play' && mode === 'camera' && (
          <CameraGame
            difficulty={difficulty}
            onPlayMove={handlePlayMove}
            onBackToHome={handleBackToHome}
          />
        )}

        {view === 'reveal' && lastRoundDetails && (
          <RevealArena
            difficulty={difficulty}
            playerMove={lastRoundDetails.playerMove}
            botMove={lastRoundDetails.botMove}
            predictedMove={lastRoundDetails.predictedMove}
            modelUsed={lastRoundDetails.modelUsed}
            outcome={lastRoundDetails.outcome}
            latencyMs={lastRoundDetails.latencyMs}
            onNextRound={handleNextRound}
            onBackToHome={handleBackToHome}
          />
        )}

        {view === 'stats' && (
          <StatsView
            logs={logs}
            stats={stats}
            onBack={handleBackFromStats}
            onDownloadJSON={handleDownloadJSON}
            onDownloadCSV={handleDownloadCSV}
            backButtonLabel={previousView === 'mode-select' ? 'Back to Home' : 'Back to Game'}
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

