import * as fs from 'fs';
import * as path from 'path';
import { ALL_MOVES, Move, Outcome } from './types';
import { resolveOutcome } from './rules';
import { createAdaptiveAI, chooseMove, updateModel } from './ai';
import { RoundLogger, calculateSummaryStats, exportToCSV, exportToJSON } from './logger';

export type OpponentStrategy = 'uniform_random' | 'fixed_rock' | 'cyclic' | 'win_stay_lose_shift';

export function getOpponentMove(
  strategy: OpponentStrategy,
  roundIndex: number,
  history: Move[],
  lastOutcome?: Outcome
): Move {
  switch (strategy) {
    case 'uniform_random':
      return ALL_MOVES[Math.floor(Math.random() * ALL_MOVES.length)];
    case 'fixed_rock':
      return 'rock';
    case 'cyclic': {
      // Cycles rock -> paper -> scissors -> rock...
      const cycle: Move[] = ['rock', 'paper', 'scissors'];
      return cycle[roundIndex % cycle.length];
    }
    case 'win_stay_lose_shift': {
      if (history.length === 0 || !lastOutcome) {
        return ALL_MOVES[Math.floor(Math.random() * ALL_MOVES.length)];
      }
      const lastMove = history[history.length - 1];
      if (lastOutcome === 'win') {
        // Player won, so stay with same move
        return lastMove;
      } else {
        // Shift to next move in cycle
        const cycle: Move[] = ['rock', 'paper', 'scissors'];
        const idx = cycle.indexOf(lastMove);
        return cycle[(idx + 1) % 3];
      }
    }
  }
}

export function runSimulation(strategy: OpponentStrategy, rounds: number = 1000) {
  let aiState = createAdaptiveAI({ gamma: 0.94, epsilon: 0.08, coldStartRounds: 10 });
  const logger = new RoundLogger();
  const opponentHistory: Move[] = [];
  let lastOutcome: Outcome | undefined = undefined;

  for (let r = 0; r < rounds; r++) {
    const oppMove = getOpponentMove(strategy, r, opponentHistory, lastOutcome);
    const decision = chooseMove(aiState, opponentHistory);

    const outcome = resolveOutcome(oppMove, decision.botMove);
    const predictionCorrect = decision.predictedMove === oppMove;

    logger.recordRound({
      roundNumber: r + 1,
      opponentMove: oppMove,
      predictedMove: decision.predictedMove,
      botMove: decision.botMove,
      result: outcome,
      modelUsed: decision.modelUsed,
      predictionCorrect,
      decisionLatencyMs: decision.decisionLatencyMs,
    });

    aiState = updateModel(
      aiState,
      oppMove,
      decision.predictedMove,
      decision.modelUsed,
      opponentHistory
    );

    opponentHistory.push(oppMove);
    lastOutcome = outcome;
  }

  return {
    strategy,
    rounds,
    stats: logger.getStats(),
    logs: logger.getLogs(),
  };
}

export function runAllSimulations() {
  const outputDir = path.resolve(process.cwd(), '../../docs/report-data');
  const localOutputDir = path.resolve(process.cwd(), 'docs/report-data');
  const targetDir = fs.existsSync(path.dirname(outputDir)) ? outputDir : localOutputDir;

  fs.makedirsSync ? fs.mkdirSync(targetDir, { recursive: true }) : fs.mkdirSync(targetDir, { recursive: true });

  const strategies: OpponentStrategy[] = ['uniform_random', 'fixed_rock', 'cyclic', 'win_stay_lose_shift'];
  const summaryResults: any[] = [];

  console.log('='.repeat(80));
  console.log('ROCK-PAPER-SCISSORS ADAPTIVE MARKOV AI - BENCHMARK SIMULATION');
  console.log('='.repeat(80));

  for (const strat of strategies) {
    const result = runSimulation(strat, 1000);
    const stats = result.stats;

    // Save individual strategy logs
    const jsonPath = path.join(targetDir, `${strat}_1000_rounds.json`);
    const csvPath = path.join(targetDir, `${strat}_1000_rounds.csv`);

    fs.writeFileSync(jsonPath, exportToJSON(result.logs), 'utf-8');
    fs.writeFileSync(csvPath, exportToCSV(result.logs), 'utf-8');

    summaryResults.push({
      Strategy: strat,
      TotalRounds: stats.totalRounds,
      BotWinRate: `${(stats.botWinRate * 100).toFixed(1)}%`,
      HumanWinRate: `${(stats.humanWinRate * 100).toFixed(1)}%`,
      TieRate: `${(stats.tieRate * 100).toFixed(1)}%`,
      PredictionAccuracy: `${(stats.overallPredictionAccuracy * 100).toFixed(1)}%`,
      Order1RollingAcc: `${(stats.modelStats.order1RollingAccuracy * 100).toFixed(1)}%`,
      Order2RollingAcc: `${(stats.modelStats.order2RollingAccuracy * 100).toFixed(1)}%`,
      AvgLatencyMs: `${stats.averageLatencyMs.toFixed(3)}ms`,
    });
  }

  console.table(summaryResults);

  // Write summary files
  const summaryJsonPath = path.join(targetDir, 'summary_report.json');
  const summaryCsvPath = path.join(targetDir, 'summary_report.csv');

  fs.writeFileSync(summaryJsonPath, JSON.stringify(summaryResults, null, 2), 'utf-8');

  const csvHeaders = Object.keys(summaryResults[0]).join(',');
  const csvRows = summaryResults.map((r) => Object.values(r).join(','));
  fs.writeFileSync(summaryCsvPath, [csvHeaders, ...csvRows].join('\n'), 'utf-8');

  console.log(`\nAll report data successfully written to: ${targetDir}`);
}

if (require.main === module || (typeof process !== 'undefined' && process.argv[1]?.includes('simulate'))) {
  runAllSimulations();
}
