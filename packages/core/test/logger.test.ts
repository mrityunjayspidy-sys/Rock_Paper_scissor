import { describe, it, expect } from 'vitest';
import { RoundLogger, exportToCSV, exportToJSON } from '../src/logger';
import { RoundLog } from '../src/types';

describe('RoundLogger', () => {
  it('records rounds and computes correct summary statistics', () => {
    const logger = new RoundLogger();

    logger.recordRound({
      opponentMove: 'rock',
      predictedMove: 'rock',
      botMove: 'paper',
      result: 'lose', // bot won
      modelUsed: 'order-1',
      predictionCorrect: true,
      decisionLatencyMs: 0.12,
    });

    logger.recordRound({
      opponentMove: 'paper',
      predictedMove: 'rock',
      botMove: 'paper',
      result: 'tie',
      modelUsed: 'order-2',
      predictionCorrect: false,
      decisionLatencyMs: 0.15,
    });

    const stats = logger.getStats();
    expect(stats.totalRounds).toBe(2);
    expect(stats.botWins).toBe(1);
    expect(stats.ties).toBe(1);
    expect(stats.humanWins).toBe(0);
    expect(stats.botWinRate).toBe(0.5);
    expect(stats.overallPredictionAccuracy).toBe(0.5);
    expect(stats.modelStats.modelUsageCounts['order-1']).toBe(1);
    expect(stats.modelStats.modelUsageCounts['order-2']).toBe(1);
  });

  it('exports valid JSON and CSV format', () => {
    const logs: RoundLog[] = [
      {
        roundNumber: 1,
        opponentMove: 'scissors',
        predictedMove: 'scissors',
        botMove: 'rock',
        result: 'lose',
        modelUsed: 'order-1',
        predictionCorrect: true,
        decisionLatencyMs: 0.25,
        timestamp: 1700000000000,
      },
    ];

    const jsonStr = exportToJSON(logs);
    const parsed = JSON.parse(jsonStr);
    expect(parsed).toHaveLength(1);
    expect(parsed[0].opponentMove).toBe('scissors');

    const csvStr = exportToCSV(logs);
    expect(csvStr).toContain('Round,OpponentMove,PredictedMove,BotMove,Result,ModelUsed,PredictionCorrect,DecisionLatencyMs,Timestamp');
    expect(csvStr).toContain('1,scissors,scissors,rock,lose,order-1,true,0.250');
  });
});
