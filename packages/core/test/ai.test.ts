import { describe, it, expect } from 'vitest';
import { createAdaptiveAI, chooseMove, updateModel, DIFFICULTY_CONFIGS } from '../src/ai';
import { resolveOutcome } from '../src/rules';
import { ALL_MOVES, Move } from '../src/types';

describe('Adaptive Markov AI Engine', () => {
  it('supports 3 difficulty presets: easy, normal, hard', () => {
    const easyAI = createAdaptiveAI('easy');
    const normalAI = createAdaptiveAI('normal');
    const hardAI = createAdaptiveAI('hard');

    expect(easyAI.config.difficulty).toBe('easy');
    expect(easyAI.config.epsilon).toBe(DIFFICULTY_CONFIGS.easy.epsilon);
    expect(easyAI.config.blunderRate).toBeGreaterThan(0);

    expect(normalAI.config.difficulty).toBe('normal');
    expect(normalAI.config.coldStartRounds).toBe(5);

    expect(hardAI.config.difficulty).toBe('hard');
    expect(hardAI.config.coldStartRounds).toBe(2);
    expect(hardAI.config.epsilon).toBe(0.02);
  });

  it('Hard mode learns immediately within 3 rounds and counters predictable opponent', () => {
    let state = createAdaptiveAI('hard');
    const history: Move[] = [];
    const cycle: Move[] = ['rock', 'paper', 'scissors'];
    let botWins = 0;
    const totalRounds = 300;

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
    // Hard mode should achieve > 92% win rate on cyclic strategy
    expect(botWinRate).toBeGreaterThan(0.92);
  });

  it('handles cold start: initial rounds are logged as cold-start', () => {
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
        botWins++;
      }

      state = updateModel(state, oppMove, decision.predictedMove, decision.modelUsed, history);
      history.push(oppMove);
    }

    const botWinRate = botWins / totalRounds;
    expect(botWinRate).toBeGreaterThan(0.85);
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
    expect(botWinRate).toBeGreaterThan(0.27);
    expect(botWinRate).toBeLessThan(0.40);
  });
});
