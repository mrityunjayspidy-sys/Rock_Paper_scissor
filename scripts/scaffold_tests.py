import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

# 1. packages/core/test/rules.test.ts
rules_test = """import { describe, it, expect } from 'vitest';
import { resolveOutcome, getBeatingMove, getLosingMove, isValidMove, moveToIndex, indexToMove } from '../src/rules';
import { Move } from '../src/types';

describe('Game Rules', () => {
  it('correctly resolves ties', () => {
    expect(resolveOutcome('rock', 'rock')).toBe('tie');
    expect(resolveOutcome('paper', 'paper')).toBe('tie');
    expect(resolveOutcome('scissors', 'scissors')).toBe('tie');
  });

  it('correctly resolves player wins', () => {
    expect(resolveOutcome('rock', 'scissors')).toBe('win');
    expect(resolveOutcome('paper', 'rock')).toBe('win');
    expect(resolveOutcome('scissors', 'paper')).toBe('win');
  });

  it('correctly resolves player losses (bot wins)', () => {
    expect(resolveOutcome('rock', 'paper')).toBe('lose');
    expect(resolveOutcome('paper', 'scissors')).toBe('lose');
    expect(resolveOutcome('scissors', 'rock')).toBe('lose');
  });

  it('identifies beating counter moves', () => {
    expect(getBeatingMove('rock')).toBe('paper');
    expect(getBeatingMove('paper')).toBe('scissors');
    expect(getBeatingMove('scissors')).toBe('rock');
  });

  it('identifies losing moves', () => {
    expect(getLosingMove('rock')).toBe('scissors');
    expect(getLosingMove('paper')).toBe('rock');
    expect(getLosingMove('scissors')).toBe('paper');
  });

  it('validates move strings', () => {
    expect(isValidMove('rock')).toBe(true);
    expect(isValidMove('paper')).toBe(true);
    expect(isValidMove('scissors')).toBe(true);
    expect(isValidMove('invalid')).toBe(false);
    expect(isValidMove(123)).toBe(false);
  });

  it('maps between moves and indices correctly', () => {
    const moves: Move[] = ['rock', 'paper', 'scissors'];
    moves.forEach((move, i) => {
      expect(moveToIndex(move)).toBe(i);
      expect(indexToMove(i)).toBe(move);
    });
  });
});
"""
write_file("packages/core/test/rules.test.ts", rules_test)

# 2. packages/core/test/ai.test.ts
ai_test = """import { describe, it, expect } from 'vitest';
import { createAdaptiveAI, chooseMove, updateModel } from '../src/ai';
import { resolveOutcome } from '../src/rules';
import { ALL_MOVES, Move } from '../src/types';

describe('Adaptive Markov AI Engine', () => {
  it('handles cold start: first 10 rounds are logged as cold-start', () => {
    let state = createAdaptiveAI({ coldStartRounds: 10, epsilon: 0 });
    const history: Move[] = [];

    for (let i = 0; i < 10; i++) {
      const decision = chooseMove(state, history);
      expect(decision.modelUsed).toBe('cold-start');
      expect(ALL_MOVES).toContain(decision.botMove);

      const actualMove: Move = 'rock';
      state = updateModel(state, actualMove, decision.predictedMove, decision.modelUsed, history);
      history.push(actualMove);
    }

    expect(history.length).toBe(10);
    // 11th round should no longer be cold-start
    const decision11 = chooseMove(state, history);
    expect(decision11.modelUsed).not.toBe('cold-start');
  });

  it('applies exponential decay gamma to frequency tables', () => {
    const gamma = 0.90;
    let state = createAdaptiveAI({ gamma, coldStartRounds: 0, epsilon: 0 });

    // Round 1: opponent plays rock
    state = updateModel(state, 'rock', 'rock', 'order-1', []);
    // Round 2: opponent plays rock following rock
    state = updateModel(state, 'rock', 'rock', 'order-1', ['rock']);

    // Round 3: update again with rock following rock
    state = updateModel(state, 'rock', 'rock', 'order-1', ['rock', 'rock']);
    // Expected: 1.0 * gamma + 1.0 = 1.90
    expect(state.order1Table.rock.rock).toBeCloseTo(1.0 * gamma + 1.0, 4);
  });

  it('converges to high win-rate (> 85%) against a fixed-strategy opponent', () => {
    let state = createAdaptiveAI({ gamma: 0.94, epsilon: 0.05, coldStartRounds: 10 });
    const history: Move[] = [];
    let botWins = 0;
    const totalRounds = 500;

    for (let r = 0; r < totalRounds; r++) {
      const oppMove: Move = 'rock'; // Opponent always plays rock
      const decision = chooseMove(state, history);
      const outcome = resolveOutcome(oppMove, decision.botMove);

      if (outcome === 'lose') {
        // From player perspective 'lose' means bot won
        botWins++;
      }

      state = updateModel(state, oppMove, decision.predictedMove, decision.modelUsed, history);
      history.push(oppMove);
    }

    const botWinRate = botWins / totalRounds;
    // Against fixed 'rock', after 10 rounds cold start, bot should play 'paper' almost 100% of the time
    expect(botWinRate).toBeGreaterThan(0.85);
  });

  it('converges to high win-rate (> 75%) against a cyclic opponent (rock->paper->scissors)', () => {
    let state = createAdaptiveAI({ gamma: 0.94, epsilon: 0.05, coldStartRounds: 10 });
    const history: Move[] = [];
    const cycle: Move[] = ['rock', 'paper', 'scissors'];
    let botWins = 0;
    const totalRounds = 600;

    for (let r = 0; r < totalRounds; r++) {
      const oppMove: Move = cycle[r % cycle.length];
      const decision = chooseMove(state, history);
      const outcome = resolveOutcome(oppMove, decision.botMove);

      if (outcome === 'lose') {
        botWins++;
      }

      state = updateModel(state, oppMove, decision.predictedMove, decision.modelUsed, history);
      history.push(oppMove);
    }

    const botWinRate = botWins / totalRounds;
    // Order-1 Markov captures transition rock->paper, paper->scissors, scissors->rock easily
    expect(botWinRate).toBeGreaterThan(0.75);
  });

  it('converges to ~33% win-rate against a uniformly random opponent over 500+ rounds', () => {
    let state = createAdaptiveAI({ gamma: 0.94, epsilon: 0.08, coldStartRounds: 10 });
    const history: Move[] = [];
    let botWins = 0;
    const totalRounds = 800;

    for (let r = 0; r < totalRounds; r++) {
      const oppMove: Move = ALL_MOVES[Math.floor(Math.random() * ALL_MOVES.length)];
      const decision = chooseMove(state, history);
      const outcome = resolveOutcome(oppMove, decision.botMove);

      if (outcome === 'lose') {
        botWins++;
      }

      state = updateModel(state, oppMove, decision.predictedMove, decision.modelUsed, history);
      history.push(oppMove);
    }

    const botWinRate = botWins / totalRounds;
    // Against uniform random, theoretical win rate is 33.33%.
    // With N=800, standard error is ~1.6%, 3 sigma is ~5%.
    // Win rate should be between 27% and 40%.
    expect(botWinRate).toBeGreaterThan(0.27);
    expect(botWinRate).toBeLessThan(0.40);
  });
});
"""
write_file("packages/core/test/ai.test.ts", ai_test)

# 3. packages/core/test/logger.test.ts
logger_test = """import { describe, it, expect } from 'vitest';
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
"""
write_file("packages/core/test/logger.test.ts", logger_test)

# 4. packages/core/test/classifier.test.ts
classifier_test = """import { describe, it, expect } from 'vitest';
import { classifyHandGesture } from '../src/classifier';
import { Landmark3D } from '../src/types';

function createDummyHand(curledFingers: { thumb: boolean; index: boolean; middle: boolean; ring: boolean; pinky: boolean }): Landmark3D[] {
  const landmarks: Landmark3D[] = [];
  // Wrist at (0, 0, 0)
  landmarks.push({ x: 0, y: 0, z: 0 });

  // Thumb: 1, 2, 3, 4
  landmarks.push({ x: 0.1, y: 0.1, z: 0 });
  landmarks.push({ x: 0.2, y: 0.2, z: 0 });
  landmarks.push({ x: 0.3, y: 0.3, z: 0 });
  landmarks.push(curledFingers.thumb ? { x: 0.15, y: 0.15, z: 0 } : { x: 0.5, y: 0.5, z: 0 });

  // Index: 5, 6, 7, 8
  landmarks.push({ x: 0.2, y: 0.3, z: 0 });
  landmarks.push({ x: 0.2, y: 0.5, z: 0 });
  landmarks.push({ x: 0.2, y: 0.7, z: 0 });
  landmarks.push(curledFingers.index ? { x: 0.2, y: 0.35, z: 0 } : { x: 0.2, y: 0.9, z: 0 });

  // Middle: 9, 10, 11, 12
  landmarks.push({ x: 0.0, y: 0.3, z: 0 });
  landmarks.push({ x: 0.0, y: 0.5, z: 0 });
  landmarks.push({ x: 0.0, y: 0.7, z: 0 });
  landmarks.push(curledFingers.middle ? { x: 0.0, y: 0.35, z: 0 } : { x: 0.0, y: 0.95, z: 0 });

  // Ring: 13, 14, 15, 16
  landmarks.push({ x: -0.2, y: 0.3, z: 0 });
  landmarks.push({ x: -0.2, y: 0.5, z: 0 });
  landmarks.push({ x: -0.2, y: 0.7, z: 0 });
  landmarks.push(curledFingers.ring ? { x: -0.2, y: 0.35, z: 0 } : { x: -0.2, y: 0.9, z: 0 });

  // Pinky: 17, 18, 19, 20
  landmarks.push({ x: -0.4, y: 0.3, z: 0 });
  landmarks.push({ x: -0.4, y: 0.45, z: 0 });
  landmarks.push({ x: -0.4, y: 0.6, z: 0 });
  landmarks.push(curledFingers.pinky ? { x: -0.4, y: 0.3, z: 0 } : { x: -0.4, y: 0.8, z: 0 });

  return landmarks;
}

describe('Geometric Hand Landmark Classifier', () => {
  it('classifies Rock when all 4 fingers are curled', () => {
    const rockHand = createDummyHand({ thumb: true, index: true, middle: true, ring: true, pinky: true });
    const result = classifyHandGesture(rockHand);
    expect(result.move).toBe('rock');
    expect(result.confidence).toBeGreaterThan(0.8);
  });

  it('classifies Paper when all 4 fingers are extended', () => {
    const paperHand = createDummyHand({ thumb: false, index: false, middle: false, ring: false, pinky: false });
    const result = classifyHandGesture(paperHand);
    expect(result.move).toBe('paper');
    expect(result.confidence).toBeGreaterThan(0.85);
  });

  it('classifies Scissors when index and middle are extended while ring and pinky are curled', () => {
    const scissorsHand = createDummyHand({ thumb: true, index: false, middle: false, ring: true, pinky: true });
    const result = classifyHandGesture(scissorsHand);
    expect(result.move).toBe('scissors');
    expect(result.confidence).toBeGreaterThan(0.85);
  });

  it('handles invalid or empty landmarks gracefully', () => {
    const result = classifyHandGesture([]);
    expect(result.move).toBeNull();
    expect(result.confidence).toBe(0);
    expect(result.reason).toContain('Incomplete');
  });
});
"""
write_file("packages/core/test/classifier.test.ts", classifier_test)

print("Test suite scaffolded!")
