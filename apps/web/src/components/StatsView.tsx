import React, { useState } from 'react';
import { RoundLog, SummaryStats } from '@rps/core';
import { Download, ArrowLeft, BarChart2, Brain } from 'lucide-react';

interface StatsViewProps {
  logs: readonly RoundLog[];
  stats: SummaryStats;
  onBack: () => void;
  onDownloadJSON: () => void;
  onDownloadCSV: () => void;
}

export const StatsView: React.FC<StatsViewProps> = ({
  logs,
  stats,
  onBack,
  onDownloadJSON,
  onDownloadCSV,
}) => {
  const [filter, setFilter] = useState<'all' | 'win' | 'lose' | 'tie'>('all');

  const filteredLogs = logs.filter((l) => (filter === 'all' ? true : l.result === filter));

  return (
    <div className="w-full max-w-6xl mx-auto px-4 py-8 animate-pop-in">
      {/* Top Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 mb-8">
        <button
          onClick={onBack}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-neutral-900 hover:bg-neutral-800 text-neutral-200 border border-white/10 text-sm font-medium transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Game</span>
        </button>

        <div className="flex items-center gap-2">
          <button
            onClick={onDownloadJSON}
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-neutral-900 hover:bg-neutral-800 text-white border border-white/20 text-xs font-semibold transition-colors"
          >
            <Download className="w-4 h-4" />
            <span>Export JSON</span>
          </button>
          <button
            onClick={onDownloadCSV}
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-white text-black hover:bg-neutral-200 text-xs font-bold transition-colors shadow-md shadow-white/10"
          >
            <Download className="w-4 h-4" />
            <span>Export CSV</span>
          </button>
        </div>
      </div>

      <div className="mb-8">
        <h2 className="text-3xl font-black font-heading text-white tracking-tight mb-2">
          Performance & Model Statistics
        </h2>
        <p className="text-sm text-neutral-400">
          In-depth diagnostics on Markov Order-1 and Order-2 prediction accuracy and win rates.
        </p>
      </div>

      {/* Summary KPI Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
        <div className="p-5 rounded-2xl bg-neutral-950/80 border border-white/10">
          <span className="text-xs text-neutral-400 block mb-1">Total Rounds</span>
          <span className="text-3xl font-bold font-mono text-white">{stats.totalRounds}</span>
        </div>

        <div className="p-5 rounded-2xl bg-neutral-950/80 border border-white/25">
          <span className="text-xs text-white block mb-1">Overall AI Accuracy</span>
          <span className="text-3xl font-bold font-mono text-white">
            {(stats.overallPredictionAccuracy * 100).toFixed(1)}%
          </span>
        </div>

        <div className="p-5 rounded-2xl bg-neutral-950/80 border border-white/15">
          <span className="text-xs text-neutral-300 block mb-1">Bot Win Rate</span>
          <span className="text-3xl font-bold font-mono text-white">
            {(stats.botWinRate * 100).toFixed(1)}%
          </span>
          <span className="text-[10px] text-neutral-500 block mt-1">vs 33.3% Baseline</span>
        </div>

        <div className="p-5 rounded-2xl bg-neutral-950/80 border border-white/10">
          <span className="text-xs text-neutral-400 block mb-1">Avg Latency</span>
          <span className="text-3xl font-bold font-mono text-white">
            {stats.averageLatencyMs.toFixed(3)} ms
          </span>
        </div>
      </div>

      {/* Model Breakdown Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="p-6 rounded-2xl bg-neutral-950/80 border border-white/10">
          <h3 className="text-base font-bold text-white font-heading mb-4 flex items-center gap-2">
            <Brain className="w-4 h-4 text-white" />
            Model Accuracy Metrics (Rolling Window)
          </h3>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-neutral-300">Markov Order-1 P(m_t | m_t-1)</span>
                <span className="font-mono text-white font-bold">
                  {(stats.modelStats.order1RollingAccuracy * 100).toFixed(1)}%
                </span>
              </div>
              <div className="w-full h-2 rounded-full bg-neutral-800 overflow-hidden">
                <div
                  className="h-full bg-white rounded-full"
                  style={{ width: `${Math.min(100, stats.modelStats.order1RollingAccuracy * 100)}%` }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-neutral-300">Markov Order-2 P(m_t | m_t-2, m_t-1)</span>
                <span className="font-mono text-white font-bold">
                  {(stats.modelStats.order2RollingAccuracy * 100).toFixed(1)}%
                </span>
              </div>
              <div className="w-full h-2 rounded-full bg-neutral-800 overflow-hidden">
                <div
                  className="h-full bg-neutral-300 rounded-full"
                  style={{ width: `${Math.min(100, stats.modelStats.order2RollingAccuracy * 100)}%` }}
                />
              </div>
            </div>
          </div>
        </div>

        <div className="p-6 rounded-2xl bg-neutral-950/80 border border-white/10">
          <h3 className="text-base font-bold text-white font-heading mb-4 flex items-center gap-2">
            <BarChart2 className="w-4 h-4 text-white" />
            Model Selection Usage Counts
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
            <div className="p-3 rounded-xl bg-black border border-white/10">
              <span className="text-[11px] text-neutral-400 block mb-1">Order-1</span>
              <span className="text-lg font-bold font-mono text-white">
                {stats.modelStats.modelUsageCounts['order-1'] || 0}
              </span>
            </div>
            <div className="p-3 rounded-xl bg-black border border-white/10">
              <span className="text-[11px] text-neutral-400 block mb-1">Order-2</span>
              <span className="text-lg font-bold font-mono text-white">
                {stats.modelStats.modelUsageCounts['order-2'] || 0}
              </span>
            </div>
            <div className="p-3 rounded-xl bg-black border border-white/10">
              <span className="text-[11px] text-neutral-400 block mb-1">Cold Start</span>
              <span className="text-lg font-bold font-mono text-neutral-300">
                {stats.modelStats.modelUsageCounts['cold-start'] || 0}
              </span>
            </div>
            <div className="p-3 rounded-xl bg-black border border-white/10">
              <span className="text-[11px] text-neutral-400 block mb-1">Random (ε)</span>
              <span className="text-lg font-bold font-mono text-neutral-400">
                {stats.modelStats.modelUsageCounts.random || 0}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Round-by-Round History Table */}
      <div className="p-6 rounded-2xl bg-neutral-950/80 border border-white/10">
        <div className="flex flex-wrap items-center justify-between gap-4 mb-4">
          <h3 className="text-lg font-bold text-white font-heading">
            Full Round History ({filteredLogs.length})
          </h3>

          <div className="flex items-center gap-1 bg-black p-1 rounded-xl border border-white/10 text-xs">
            {(['all', 'win', 'lose', 'tie'] as const).map((opt) => (
              <button
                key={opt}
                onClick={() => setFilter(opt)}
                className={`px-3 py-1 rounded-lg capitalize font-medium transition-colors ${
                  filter === opt ? 'bg-white text-black font-bold' : 'text-neutral-400 hover:text-white'
                }`}
              >
                {opt}
              </button>
            ))}
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-white/10 text-neutral-400 font-mono">
                <th className="py-3 px-3">#</th>
                <th className="py-3 px-3">Your Move</th>
                <th className="py-3 px-3">Predicted Move</th>
                <th className="py-3 px-3">Bot Move</th>
                <th className="py-3 px-3">Result</th>
                <th className="py-3 px-3">Model</th>
                <th className="py-3 px-3">Prediction</th>
                <th className="py-3 px-3">Latency</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5 font-mono">
              {filteredLogs.length === 0 ? (
                <tr>
                  <td colSpan={8} className="py-8 text-center text-neutral-500">
                    No rounds recorded yet.
                  </td>
                </tr>
              ) : (
                filteredLogs.slice().reverse().map((log) => (
                  <tr key={log.roundNumber} className="hover:bg-white/5 transition-colors">
                    <td className="py-2.5 px-3 text-neutral-500">{log.roundNumber}</td>
                    <td className="py-2.5 px-3 font-semibold text-white uppercase">{log.opponentMove}</td>
                    <td className="py-2.5 px-3 text-neutral-300 uppercase">{log.predictedMove}</td>
                    <td className="py-2.5 px-3 text-white uppercase">{log.botMove}</td>
                    <td className="py-2.5 px-3">
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                          log.result === 'win'
                            ? 'bg-white text-black'
                            : log.result === 'lose'
                            ? 'bg-neutral-800 text-neutral-300 border border-white/10'
                            : 'bg-neutral-900 text-neutral-400 border border-white/5'
                        }`}
                      >
                        {log.result}
                      </span>
                    </td>
                    <td className="py-2.5 px-3 text-neutral-400">{log.modelUsed}</td>
                    <td className="py-2.5 px-3">
                      {log.predictionCorrect ? (
                        <span className="text-white font-bold">Hit</span>
                      ) : (
                        <span className="text-neutral-600">Miss</span>
                      )}
                    </td>
                    <td className="py-2.5 px-3 text-neutral-400">{log.decisionLatencyMs.toFixed(2)}ms</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
