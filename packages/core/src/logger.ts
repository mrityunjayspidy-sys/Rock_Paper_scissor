import { RoundLog, SummaryStats, ModelType } from './types';
import { getRollingAccuracy } from './ai';

/**
 * RoundLogger tracks round records, calculates summary metrics,
 * and handles CSV and JSON exports.
 */
export class RoundLogger {
  private logs: RoundLog[] = [];

  constructor(initialLogs: RoundLog[] = []) {
    this.logs = [...initialLogs];
  }

  public recordRound(log: Omit<RoundLog, 'roundNumber' | 'timestamp'> & { roundNumber?: number; timestamp?: number }): RoundLog {
    const fullLog: RoundLog = {
      roundNumber: log.roundNumber ?? this.logs.length + 1,
      opponentMove: log.opponentMove,
      predictedMove: log.predictedMove,
      botMove: log.botMove,
      result: log.result,
      modelUsed: log.modelUsed,
      predictionCorrect: log.predictionCorrect,
      decisionLatencyMs: Number(log.decisionLatencyMs.toFixed(3)),
      timestamp: log.timestamp ?? Date.now(),
    };
    this.logs.push(fullLog);
    return fullLog;
  }

  public getLogs(): readonly RoundLog[] {
    return this.logs;
  }

  public clear(): void {
    this.logs = [];
  }

  public getStats(): SummaryStats {
    return calculateSummaryStats(this.logs);
  }

  public exportJSON(): string {
    return exportToJSON(this.logs);
  }

  public exportCSV(): string {
    return exportToCSV(this.logs);
  }
}

export function calculateSummaryStats(logs: readonly RoundLog[]): SummaryStats {
  const totalRounds = logs.length;
  if (totalRounds === 0) {
    return {
      totalRounds: 0,
      humanWins: 0,
      botWins: 0,
      ties: 0,
      humanWinRate: 0,
      botWinRate: 0,
      tieRate: 0,
      overallPredictionAccuracy: 0,
      averageLatencyMs: 0,
      modelStats: {
        order1RollingAccuracy: 0,
        order2RollingAccuracy: 0,
        order1LifetimeAccuracy: 0,
        order2LifetimeAccuracy: 0,
        modelUsageCounts: {
          'order-1': 0,
          'order-2': 0,
          random: 0,
          'cold-start': 0,
        },
      },
    };
  }

  let humanWins = 0;
  let botWins = 0;
  let ties = 0;
  let correctPredictions = 0;
  let totalLatency = 0;

  const modelUsage: Record<ModelType, number> = {
    'order-1': 0,
    'order-2': 0,
    random: 0,
    'cold-start': 0,
  };

  const o1Hits: number[] = [];
  const o2Hits: number[] = [];
  let o1Total = 0;
  let o1Correct = 0;
  let o2Total = 0;
  let o2Correct = 0;

  for (const log of logs) {
    if (log.result === 'win') humanWins++;
    else if (log.result === 'lose') botWins++;
    else ties++;

    if (log.predictionCorrect) correctPredictions++;
    totalLatency += log.decisionLatencyMs;

    modelUsage[log.modelUsed] = (modelUsage[log.modelUsed] || 0) + 1;

    if (log.modelUsed === 'order-1') {
      o1Total++;
      if (log.predictionCorrect) o1Correct++;
      o1Hits.push(log.predictionCorrect ? 1 : 0);
    } else if (log.modelUsed === 'order-2') {
      o2Total++;
      if (log.predictionCorrect) o2Correct++;
      o2Hits.push(log.predictionCorrect ? 1 : 0);
    }
  }

  const recentWindow = 20;
  const recentO1 = o1Hits.slice(-recentWindow);
  const recentO2 = o2Hits.slice(-recentWindow);

  return {
    totalRounds,
    humanWins,
    botWins,
    ties,
    humanWinRate: Number((humanWins / totalRounds).toFixed(4)),
    botWinRate: Number((botWins / totalRounds).toFixed(4)),
    tieRate: Number((ties / totalRounds).toFixed(4)),
    overallPredictionAccuracy: Number((correctPredictions / totalRounds).toFixed(4)),
    averageLatencyMs: Number((totalLatency / totalRounds).toFixed(3)),
    modelStats: {
      order1RollingAccuracy: Number(getRollingAccuracy(recentO1).toFixed(4)),
      order2RollingAccuracy: Number(getRollingAccuracy(recentO2).toFixed(4)),
      order1LifetimeAccuracy: o1Total > 0 ? Number((o1Correct / o1Total).toFixed(4)) : 0,
      order2LifetimeAccuracy: o2Total > 0 ? Number((o2Correct / o2Total).toFixed(4)) : 0,
      modelUsageCounts: modelUsage,
    },
  };
}

export function exportToJSON(logs: readonly RoundLog[]): string {
  return JSON.stringify(logs, null, 2);
}

export function exportToCSV(logs: readonly RoundLog[]): string {
  const headers = [
    'Round',
    'OpponentMove',
    'PredictedMove',
    'BotMove',
    'Result',
    'ModelUsed',
    'PredictionCorrect',
    'DecisionLatencyMs',
    'Timestamp',
  ];

  const rows = logs.map((log) => [
    log.roundNumber,
    log.opponentMove,
    log.predictedMove,
    log.botMove,
    log.result,
    log.modelUsed,
    log.predictionCorrect ? 'true' : 'false',
    log.decisionLatencyMs.toFixed(3),
    new Date(log.timestamp).toISOString(),
  ]);

  return [headers.join(','), ...rows.map((row) => row.join(','))].join('\n');
}
