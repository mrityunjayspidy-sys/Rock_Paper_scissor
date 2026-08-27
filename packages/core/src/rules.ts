import { Move, Outcome, ALL_MOVES } from './types';

/**
 * Returns the move that beats the specified move.
 */
export function getBeatingMove(move: Move): Move {
  switch (move) {
    case 'rock':
      return 'paper';
    case 'paper':
      return 'scissors';
    case 'scissors':
      return 'rock';
  }
}

/**
 * Returns the move that loses to the specified move.
 */
export function getLosingMove(move: Move): Move {
  switch (move) {
    case 'rock':
      return 'scissors';
    case 'paper':
      return 'rock';
    case 'scissors':
      return 'paper';
  }
}

/**
 * Resolves the round outcome from the player's perspective.
 * 'win' = player won, 'lose' = player lost (bot won), 'tie' = draw.
 */
export function resolveOutcome(playerMove: Move, botMove: Move): Outcome {
  if (playerMove === botMove) {
    return 'tie';
  }
  if (
    (playerMove === 'rock' && botMove === 'scissors') ||
    (playerMove === 'paper' && botMove === 'rock') ||
    (playerMove === 'scissors' && botMove === 'paper')
  ) {
    return 'win';
  }
  return 'lose';
}

/**
 * Validates whether an arbitrary string is a valid Move.
 */
export function isValidMove(move: unknown): move is Move {
  return typeof move === 'string' && (ALL_MOVES as readonly string[]).includes(move);
}

/**
 * Map move to numerical index 0, 1, 2
 */
export function moveToIndex(move: Move): number {
  return move === 'rock' ? 0 : move === 'paper' ? 1 : 2;
}

/**
 * Map numerical index to Move
 */
export function indexToMove(index: number): Move {
  const norm = ((index % 3) + 3) % 3;
  return ALL_MOVES[norm];
}
