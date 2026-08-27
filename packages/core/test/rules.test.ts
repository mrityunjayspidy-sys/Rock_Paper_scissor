import { describe, it, expect } from 'vitest';
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
