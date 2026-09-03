/**
 * Rock Paper Scissors - Adaptive AI Type Definitions
 */

export type Move = 'rock' | 'paper' | 'scissors';

export const ALL_MOVES: readonly Move[] = ['rock', 'paper', 'scissors'] as const;

export type Outcome = 'win' | 'lose' | 'tie';

export type ModelType = 'order-1' | 'order-2' | 'random' | 'cold-start';

export type Difficulty = 'easy' | 'normal' | 'hard';

export interface AIConfig {
  /** Difficulty level preset */
  difficulty: Difficulty;
  /** Exponential decay factor applied every round before incrementing (default: 0.94) */
  gamma: number;
  /** Exploration rate: probability of making a uniform random move (default: 0.08) */
  epsilon: number;
  /** Number of initial rounds to play randomly for cold start (default: 10) */
  coldStartRounds: number;
  /** Rolling window size for accuracy tracking (default: 20) */
  rollingWindowSize: number;
  /** Smoothing constant for probability calculations (default: 0.05) */
  laplaceSmoothing: number;
  /** Probability of intentionally making a suboptimal move (Easy mode only) */
  blunderRate?: number;
}

export interface PredictionResult {
  predictedMove: Move;
  modelUsed: ModelType;
  confidence: number;
  order1Predicted?: Move;
  order2Predicted?: Move;
  order1Confidence?: number;
  order2Confidence?: number;
}

export interface BotDecision {
  botMove: Move;
  predictedMove: Move;
  modelUsed: ModelType;
  confidence: number;
  decisionLatencyMs: number;
}

export interface RoundLog {
  roundNumber: number;
  opponentMove: Move;
  predictedMove: Move;
  botMove: Move;
  result: Outcome;
  modelUsed: ModelType;
  predictionCorrect: boolean;
  decisionLatencyMs: number;
  timestamp: number;
}

export interface AdaptiveAIState {
  config: AIConfig;
  roundCount: number;
  /** Order-1 Markov counts: [lastMove][nextMove] */
  order1Table: Record<Move, Record<Move, number>>;
  /** Order-2 Markov counts: [`${move1},${move2}`][nextMove] */
  order2Table: Record<string, Record<Move, number>>;
  /** Rolling accuracy window for Order-1 (1 for correct, 0 for incorrect) */
  order1History: number[];
  /** Rolling accuracy window for Order-2 (1 for correct, 0 for incorrect) */
  order2History: number[];
  /** Total predictions made by Order-1 */
  order1TotalPredictions: number;
  /** Total correct predictions by Order-1 */
  order1CorrectPredictions: number;
  /** Total predictions made by Order-2 */
  order2TotalPredictions: number;
  /** Total correct predictions by Order-2 */
  order2CorrectPredictions: number;
}

export interface ModelAccuracyStats {
  order1RollingAccuracy: number;
  order2RollingAccuracy: number;
  order1LifetimeAccuracy: number;
  order2LifetimeAccuracy: number;
  modelUsageCounts: Record<ModelType, number>;
}

export interface SummaryStats {
  totalRounds: number;
  humanWins: number;
  botWins: number;
  ties: number;
  humanWinRate: number;
  botWinRate: number;
  tieRate: number;
  overallPredictionAccuracy: number;
  averageLatencyMs: number;
  modelStats: ModelAccuracyStats;
}

export interface Landmark3D {
  x: number;
  y: number;
  z: number;
}

export interface HandClassificationResult {
  move: Move | null;
  confidence: number;
  fingersExtended: {
    thumb: boolean;
    index: boolean;
    middle: boolean;
    ring: boolean;
    pinky: boolean;
  };
  reason?: string;
}
