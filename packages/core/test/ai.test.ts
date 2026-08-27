import { describe, it, expect } from 'vitest';
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
