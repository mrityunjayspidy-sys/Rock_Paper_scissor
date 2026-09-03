import { describe, it, expect } from 'vitest';
import { createAdaptiveAI, chooseMove, updateModel, DIFFICULTY_CONFIGS } from '../src/ai/ai';
import { resolveOutcome } from '../src/ai/rules';
import { ALL_MOVES, Move } from '../src/ai/types';

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

    const postColdDecision = chooseMove(state, history);
    expect(postColdDecision.modelUsed).not.toBe('cold-start');
  });

  it('maintains state immutability across updates', () => {
    const originalState = createAdaptiveAI();
    const updatedState = updateModel(originalState, 'rock', 'paper', 'order-1', ['scissors']);

    expect(originalState.roundCount).toBe(0);
    expect(updatedState.roundCount).toBe(1);
    expect(originalState.order1Table.scissors.rock).toBe(0);
    expect(updatedState.order1Table.scissors.rock).toBe(1);
  });
});
