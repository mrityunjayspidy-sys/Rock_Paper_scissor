import React, { useState } from 'react';
import { SummaryStats, RoundLog, Move, Difficulty } from '../ai';
import {
  Trophy,
  Cpu,
  Target,
  History,
  Activity,
  ArrowRight,
  RotateCcw,
  Download,
  Flame,
  Brain,
  Zap,
  CheckCircle2,
  HelpCircle,
} from 'lucide-react';

interface HomeStatsProps {
  stats: SummaryStats;
  logs: readonly RoundLog[];
  difficulty: Difficulty;
  onOpenStats: () => void;
  onResetStats: () => void;
  onDownloadJSON: () => void;
  onDownloadCSV: () => void;
}

const MOVE_EMOJIS: Record<Move, string> = {
  rock: '✊',
  paper: '✋',
  scissors: '✌️',
};

export const HomeStats: React.FC<HomeStatsProps> = ({
  stats,
  logs,
  difficulty,
  onOpenStats,
  onResetStats,
  onDownloadJSON,
  onDownloadCSV,
}) => {
  const [showConfirmReset, setShowConfirmReset] = useState(false);

  // Compute streak from recent logs
  const calculateStreak = () => {
    if (logs.length === 0) return null;
    const lastResult = logs[logs.length - 1].result;
    let count = 0;
    for (let i = logs.length - 1; i >= 0; i--) {
      if (logs[i].result === lastResult) {
        count++;
      } else {
        break;
      }
    }
    return { result: lastResult, count };
  };

  const streak = calculateStreak();
  const recentLogs = logs.slice(-8); // Show up to last 8 rounds

  const handleResetClick = () => {
    if (!showConfirmReset) {
      setShowConfirmReset(true);
      setTimeout(() => setShowConfirmReset(false), 4000);
    } else {
      onResetStats();
      setShowConfirmReset(false);
    }
  };

  return (
    <section
      id="home-stats-section"
      aria-label="Match Statistics and AI Telemetry"
      className="w-full max-w-4xl mx-auto mb-10 text-left"
    >
      <div className="glass-panel p-6 sm:p-8 rounded-3xl relative overflow-hidden border border-white/10 shadow-2xl bg-neutral-950/70 backdrop-blur-xl">
        {/* Top Header Bar */}
        <div className="flex flex-wrap items-center justify-between gap-4 pb-6 border-b border-white/10">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-white/10 border border-white/20 flex items-center justify-center text-white shadow-inner">
              <Activity className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-bold font-heading text-white tracking-tight">
                  Match Statistics & Telemetry
                </h2>
                {stats.totalRounds > 0 ? (
                  <span className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-mono font-medium bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                    Live Record
                  </span>
                ) : (
                  <span className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-mono font-medium bg-white/10 text-neutral-300 border border-white/15">
                    <span className="w-1.5 h-1.5 rounded-full bg-neutral-400" />
                    Standby
                  </span>
                )}
              </div>
              <p className="text-xs text-neutral-400">
                {stats.totalRounds > 0
                  ? `Performance record across ${stats.totalRounds} completed rounds against ${difficulty.toUpperCase()} AI`
                  : 'Historical stats before initiating game play • Ready for round 1'}
              </p>
            </div>
          </div>

          {/* Quick Action Buttons */}
          <div className="flex items-center gap-2">
            {stats.totalRounds > 0 && (
              <>
                <button
                  id="home-stats-export-csv"
                  onClick={onDownloadCSV}
                  className="px-3 py-1.5 rounded-xl bg-neutral-900 hover:bg-neutral-800 text-neutral-300 hover:text-white border border-white/10 text-xs font-semibold flex items-center gap-1.5 transition-all"
                  title="Export match logs as CSV"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span className="hidden sm:inline">CSV</span>
                </button>

                <button
                  id="home-stats-export-json"
                  onClick={onDownloadJSON}
                  className="px-3 py-1.5 rounded-xl bg-neutral-900 hover:bg-neutral-800 text-neutral-300 hover:text-white border border-white/10 text-xs font-semibold flex items-center gap-1.5 transition-all"
                  title="Export match logs as JSON"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span className="hidden sm:inline">JSON</span>
                </button>

                <button
                  id="home-stats-reset-btn"
                  onClick={handleResetClick}
                  className={`px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-all border ${
                    showConfirmReset
                      ? 'bg-rose-500/20 text-rose-300 border-rose-500/40 animate-pulse'
                      : 'bg-neutral-900 hover:bg-neutral-800 text-neutral-400 hover:text-neutral-200 border-white/10'
                  }`}
                  title={showConfirmReset ? 'Click again to confirm reset' : 'Reset all stats'}
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                  <span>{showConfirmReset ? 'Confirm Reset?' : 'Reset'}</span>
                </button>
              </>
            )}

            <button
              id="home-stats-view-detailed-btn"
              onClick={onOpenStats}
              className="px-3.5 py-1.5 rounded-xl bg-white text-black hover:bg-neutral-200 text-xs font-bold flex items-center gap-1.5 transition-all shadow-md shadow-white/10"
            >
              <span>Full Analytics</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* 4 Primary KPI Metrics Grid */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 my-6">
          {/* 1. Total Rounds */}
          <div className="p-4 sm:p-5 rounded-2xl bg-black/60 border border-white/10 hover:border-white/20 transition-all flex flex-col justify-between">
            <div className="flex items-center justify-between text-neutral-400 mb-2">
              <span className="text-[11px] font-mono uppercase tracking-wider font-semibold">
                Rounds Played
              </span>
              <History className="w-4 h-4 text-neutral-400" />
            </div>
            <div>
              <span className="text-3xl sm:text-4xl font-black font-mono text-white block tracking-tight">
                {stats.totalRounds}
              </span>
              <span className="text-[11px] text-neutral-400 block mt-1">
                {stats.totalRounds > 0
                  ? `${stats.humanWins}W • ${stats.botWins}L • ${stats.ties}T`
                  : '0 completed games'}
              </span>
            </div>
          </div>

          {/* 2. Player Win Rate */}
          <div className="p-4 sm:p-5 rounded-2xl bg-black/60 border border-white/10 hover:border-white/20 transition-all flex flex-col justify-between">
            <div className="flex items-center justify-between text-neutral-400 mb-2">
              <span className="text-[11px] font-mono uppercase tracking-wider font-semibold">
                Your Win Rate
              </span>
              <Trophy className="w-4 h-4 text-white" />
            </div>
            <div>
              <span className="text-3xl sm:text-4xl font-black font-mono text-white block tracking-tight">
                {stats.totalRounds > 0 ? (stats.humanWinRate * 100).toFixed(1) : '0.0'}%
              </span>
              <span className="text-[11px] text-neutral-400 block mt-1">
                {stats.totalRounds > 0 ? `${stats.humanWins} player wins` : 'Ready to benchmark'}
              </span>
            </div>
            {/* Mini Progress Bar */}
            <div className="w-full h-1.5 rounded-full bg-neutral-800 mt-3 overflow-hidden flex">
              <div
                className="h-full bg-white transition-all duration-500"
                style={{ width: `${stats.totalRounds > 0 ? stats.humanWinRate * 100 : 0}%` }}
                title={`You: ${(stats.humanWinRate * 100).toFixed(1)}%`}
              />
              <div
                className="h-full bg-neutral-500 transition-all duration-500"
                style={{ width: `${stats.totalRounds > 0 ? stats.tieRate * 100 : 0}%` }}
                title={`Ties: ${(stats.tieRate * 100).toFixed(1)}%`}
              />
              <div
                className="h-full bg-neutral-700 transition-all duration-500"
                style={{ width: `${stats.totalRounds > 0 ? stats.botWinRate * 100 : 0}%` }}
                title={`Bot: ${(stats.botWinRate * 100).toFixed(1)}%`}
              />
            </div>
          </div>

          {/* 3. Bot Win Rate */}
          <div className="p-4 sm:p-5 rounded-2xl bg-black/60 border border-white/10 hover:border-white/20 transition-all flex flex-col justify-between">
            <div className="flex items-center justify-between text-neutral-400 mb-2">
              <span className="text-[11px] font-mono uppercase tracking-wider font-semibold">
                Bot Win Rate
              </span>
              <Cpu className="w-4 h-4 text-neutral-300" />
            </div>
            <div>
              <span className="text-3xl sm:text-4xl font-black font-mono text-white block tracking-tight">
                {stats.totalRounds > 0 ? (stats.botWinRate * 100).toFixed(1) : '0.0'}%
              </span>
              <span className="text-[11px] text-neutral-400 block mt-1">
                {stats.totalRounds > 0 ? (
                  <span>
                    {stats.botWinRate * 100 >= 33.3 ? '+' : ''}
                    {(stats.botWinRate * 100 - 33.3).toFixed(1)}% vs 33.3% baseline
                  </span>
                ) : (
                  'Baseline: 33.3% random'
                )}
              </span>
            </div>
          </div>

          {/* 4. AI Prediction Accuracy */}
          <div className="p-4 sm:p-5 rounded-2xl bg-black/60 border border-white/10 hover:border-white/20 transition-all flex flex-col justify-between">
            <div className="flex items-center justify-between text-neutral-400 mb-2">
              <span className="text-[11px] font-mono uppercase tracking-wider font-semibold">
                AI Accuracy
              </span>
              <Target className="w-4 h-4 text-white" />
            </div>
            <div>
              <span className="text-3xl sm:text-4xl font-black font-mono text-white block tracking-tight">
                {stats.totalRounds > 0 ? (stats.overallPredictionAccuracy * 100).toFixed(1) : '0.0'}%
              </span>
              <span className="text-[11px] text-neutral-400 block mt-1">
                {stats.totalRounds > 0 ? 'Markov sequence detection' : 'Dual Order-1 & Order-2'}
              </span>
            </div>
          </div>
        </div>

        {/* Dynamic Section: Active Session Details OR Standby AI Guide */}
        {stats.totalRounds > 0 ? (
          <div className="space-y-5 pt-2">
            {/* Recent Match Form Strip */}
            <div className="p-4 rounded-2xl bg-black/40 border border-white/10">
              <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
                <span className="text-xs font-semibold text-neutral-300 flex items-center gap-1.5">
                  <Flame className="w-3.5 h-3.5 text-white" />
                  Recent Form (Last {recentLogs.length} Rounds)
                </span>
                {streak && (
                  <span
                    className={`text-[11px] font-mono px-2 py-0.5 rounded-full font-bold ${
                      streak.result === 'win'
                        ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                        : streak.result === 'lose'
                        ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                        : 'bg-neutral-800 text-neutral-300 border border-white/10'
                    }`}
                  >
                    {streak.result === 'win' && `🔥 ${streak.count} Win Streak`}
                    {streak.result === 'lose' && `⚡ AI Lead (${streak.count} in a row)`}
                    {streak.result === 'tie' && `⚖️ ${streak.count} Consecutive Ties`}
                  </span>
                )}
              </div>

              {/* Badges strip */}
              <div className="flex flex-wrap items-center gap-2">
                {recentLogs.map((log) => (
                  <div
                    key={log.roundNumber}
                    className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl border text-xs font-mono transition-transform hover:scale-105 ${
                      log.result === 'win'
                        ? 'bg-white text-black border-white font-bold shadow-sm shadow-white/20'
                        : log.result === 'lose'
                        ? 'bg-neutral-900 text-neutral-300 border-white/10'
                        : 'bg-neutral-950 text-neutral-400 border-white/5'
                    }`}
                    title={`Round #${log.roundNumber}: You played ${log.opponentMove}, Bot played ${log.botMove} (${log.result.toUpperCase()})`}
                  >
                    <span className="font-bold">
                      {log.result === 'win' ? 'W' : log.result === 'lose' ? 'L' : 'T'}
                    </span>
                    <span className="text-sm">
                      {MOVE_EMOJIS[log.opponentMove]} vs {MOVE_EMOJIS[log.botMove]}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Markov Order-1 vs Order-2 Accuracy Diagnostics */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="p-4 rounded-2xl bg-black/40 border border-white/10">
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <span className="text-neutral-300 font-semibold flex items-center gap-1.5">
                    <Brain className="w-3.5 h-3.5 text-neutral-400" />
                    Markov Order-1 Rolling Accuracy
                  </span>
                  <span className="font-mono text-white font-bold">
                    {(stats.modelStats.order1RollingAccuracy * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="w-full h-2 rounded-full bg-neutral-800 overflow-hidden mb-2">
                  <div
                    className="h-full bg-white rounded-full transition-all duration-500"
                    style={{
                      width: `${Math.min(100, stats.modelStats.order1RollingAccuracy * 100)}%`,
                    }}
                  />
                </div>
                <p className="text-[11px] text-neutral-500">
                  Transitions P(m_t | m_t-1) • Used {stats.modelStats.modelUsageCounts['order-1']} times
                </p>
              </div>

              <div className="p-4 rounded-2xl bg-black/40 border border-white/10">
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <span className="text-neutral-300 font-semibold flex items-center gap-1.5">
                    <Brain className="w-3.5 h-3.5 text-white" />
                    Markov Order-2 Rolling Accuracy
                  </span>
                  <span className="font-mono text-white font-bold">
                    {(stats.modelStats.order2RollingAccuracy * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="w-full h-2 rounded-full bg-neutral-800 overflow-hidden mb-2">
                  <div
                    className="h-full bg-neutral-300 rounded-full transition-all duration-500"
                    style={{
                      width: `${Math.min(100, stats.modelStats.order2RollingAccuracy * 100)}%`,
                    }}
                  />
                </div>
                <p className="text-[11px] text-neutral-500">
                  Transitions P(m_t | m_t-2, m_t-1) • Used {stats.modelStats.modelUsageCounts['order-2']} times
                </p>
              </div>
            </div>

            {/* Latency & Telemetry Footer */}
            <div className="flex flex-wrap items-center justify-between text-xs text-neutral-400 pt-2 border-t border-white/10 font-mono">
              <div className="flex items-center gap-2">
                <Zap className="w-3.5 h-3.5 text-white" />
                <span>Decision Latency: {stats.averageLatencyMs.toFixed(3)} ms</span>
              </div>
              <div>
                <span>Difficulty Profile: </span>
                <span className="text-white font-bold uppercase">{difficulty}</span>
              </div>
            </div>
          </div>
        ) : (
          /* Empty / Initial State (Before starting first play) */
          <div className="p-5 rounded-2xl bg-black/40 border border-white/10 text-left">
            <div className="flex items-start gap-3">
              <div className="p-2 rounded-xl bg-white/10 text-white mt-0.5">
                <HelpCircle className="w-4 h-4" />
              </div>
              <div className="flex-1">
                <h3 className="text-sm font-bold text-white mb-1">
                  AI Model Benchmarking Ready
                </h3>
                <p className="text-xs text-neutral-400 mb-3 leading-relaxed">
                  No rounds recorded yet in this session. Once you make your first move, real-time Markov transition tables will compute your psychological patterns, reaction latencies, and prediction hit rates right here.
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 text-[11px] text-neutral-300 font-mono">
                  <div className="flex items-center gap-1.5 p-2 rounded-lg bg-neutral-900/80 border border-white/5">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                    <span>Order-1: 1-step counter model</span>
                  </div>
                  <div className="flex items-center gap-1.5 p-2 rounded-lg bg-neutral-900/80 border border-white/5">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                    <span>Order-2: 2-step sequence memory</span>
                  </div>
                  <div className="flex items-center gap-1.5 p-2 rounded-lg bg-neutral-900/80 border border-white/5">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                    <span>Exponential Decay: Adaptive shift</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </section>
  );
};
