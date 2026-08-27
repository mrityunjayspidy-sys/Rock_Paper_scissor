import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

# 1. packages/core/package.json
package_json = """{
  "name": "@rps/core",
  "version": "1.0.0",
  "description": "Shared TypeScript game logic and Markov opponent modeling AI for Rock Paper Scissors",
  "main": "./dist/index.js",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "types": "./src/index.ts",
      "import": "./src/index.ts",
      "default": "./src/index.ts"
    }
  },
  "scripts": {
    "build": "tsc",
    "test": "vitest run",
    "test:watch": "vitest",
    "simulate": "tsx src/simulate.ts"
  },
  "dependencies": {},
  "devDependencies": {
    "@types/node": "^22.10.2",
    "tsx": "^4.19.2",
    "typescript": "^5.7.2",
    "vitest": "^2.1.8"
  }
}
"""
write_file("packages/core/package.json", package_json)

# 2. packages/core/tsconfig.json
tsconfig_json = """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "test"]
}
"""
write_file("packages/core/tsconfig.json", tsconfig_json)

# 3. packages/core/src/types.ts
types_ts = """/**
 * Core Move types
 */
export type Move = 'rock' | 'paper' | 'scissors';

export const ALL_MOVES: readonly Move[] = ['rock', 'paper', 'scissors'] as const;

export type Outcome = 'win' | 'lose' | 'tie';

export type ModelType = 'order-1' | 'order-2' | 'random' | 'cold-start';

export interface AIConfig {
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
"""
write_file("packages/core/src/types.ts", types_ts)

# 4. packages/core/src/rules.ts
rules_ts = """import { Move, Outcome, ALL_MOVES } from './types';

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
"""
write_file("packages/core/src/rules.ts", rules_ts)

# 5. packages/core/src/ai.ts
ai_ts = """import {
  AdaptiveAIState,
  AIConfig,
  ALL_MOVES,
  BotDecision,
  ModelType,
  Move,
  PredictionResult,
} from './types';
import { getBeatingMove } from './rules';

export const DEFAULT_AI_CONFIG: AIConfig = {
  gamma: 0.94,
  epsilon: 0.08,
  coldStartRounds: 10,
  rollingWindowSize: 20,
  laplaceSmoothing: 0.05,
};

function createInitialMoveRecord(): Record<Move, number> {
  return {
    rock: 0,
    paper: 0,
    scissors: 0,
  };
}

function createInitialOrder1Table(): Record<Move, Record<Move, number>> {
  return {
    rock: createInitialMoveRecord(),
    paper: createInitialMoveRecord(),
    scissors: createInitialMoveRecord(),
  };
}

function createInitialOrder2Table(): Record<string, Record<Move, number>> {
  const table: Record<string, Record<Move, number>> = {};
  for (const m1 of ALL_MOVES) {
    for (const m2 of ALL_MOVES) {
      table[`${m1},${m2}`] = createInitialMoveRecord();
    }
  }
  return table;
}

/**
 * Initializes a new pure Adaptive AI state.
 */
export function createAdaptiveAI(config?: Partial<AIConfig>): AdaptiveAIState {
  const mergedConfig: AIConfig = { ...DEFAULT_AI_CONFIG, ...config };
  return {
    config: mergedConfig,
    roundCount: 0,
    order1Table: createInitialOrder1Table(),
    order2Table: createInitialOrder2Table(),
    order1History: [],
    order2History: [],
    order1TotalPredictions: 0,
    order1CorrectPredictions: 0,
    order2TotalPredictions: 0,
    order2CorrectPredictions: 0,
  };
}

/**
 * Calculates rolling accuracy from a binary history array (1=correct, 0=wrong).
 */
export function getRollingAccuracy(history: number[]): number {
  if (history.length === 0) return 0.3333;
  const sum = history.reduce((a, b) => a + b, 0);
  return sum / history.length;
}

/**
 * Predicts the opponent's next move based on transition tables.
 */
function predictFromDistribution(
  dist: Record<Move, number>,
  smoothing: number,
  rng: () => number = Math.random
): { move: Move; confidence: number } {
  const smoothedCounts = {
    rock: (dist.rock || 0) + smoothing,
    paper: (dist.paper || 0) + smoothing,
    scissors: (dist.scissors || 0) + smoothing,
  };
  const total = smoothedCounts.rock + smoothedCounts.paper + smoothedCounts.scissors;

  let bestMove: Move = ALL_MOVES[Math.floor(rng() * ALL_MOVES.length)];
  let maxProb = -1;

  for (const move of ALL_MOVES) {
    const prob = smoothedCounts[move] / total;
    if (prob > maxProb) {
      maxProb = prob;
      bestMove = move;
    }
  }

  return { move: bestMove, confidence: maxProb };
}

/**
 * Pure function to predict the opponent's next move.
 */
export function predictNextMove(
  state: AdaptiveAIState,
  history: readonly Move[],
  rng: () => number = Math.random
): PredictionResult {
  const totalHistory = history.length;

  if (totalHistory === 0) {
    const randomMove = ALL_MOVES[Math.floor(rng() * ALL_MOVES.length)];
    return {
      predictedMove: randomMove,
      modelUsed: 'random',
      confidence: 0.3333,
    };
  }

  const lastMove = history[totalHistory - 1];
  const order1Dist = state.order1Table[lastMove] || createInitialMoveRecord();
  const order1Pred = predictFromDistribution(order1Dist, state.config.laplaceSmoothing, rng);

  let order2Pred: { move: Move; confidence: number } | null = null;
  if (totalHistory >= 2) {
    const prevMove = history[totalHistory - 2];
    const key = `${prevMove},${lastMove}`;
    const order2Dist = state.order2Table[key] || createInitialMoveRecord();
    const order2RawTotal = (order2Dist.rock || 0) + (order2Dist.paper || 0) + (order2Dist.scissors || 0);
    // If order 2 has seen observations for this key, predict with order 2
    if (order2RawTotal > 0.05) {
      order2Pred = predictFromDistribution(order2Dist, state.config.laplaceSmoothing, rng);
    }
  }

  const order1Acc = getRollingAccuracy(state.order1History);
  const order2Acc = getRollingAccuracy(state.order2History);

  // Model selection logic:
  // Use order-2 if available and accurate; else use order-1
  let selectedModel: ModelType = 'order-1';
  let predictedMove = order1Pred.move;
  let confidence = order1Pred.confidence;

  if (order2Pred) {
    if (order2Acc > order1Acc) {
      selectedModel = 'order-2';
      predictedMove = order2Pred.move;
      confidence = order2Pred.confidence;
    } else if (Math.abs(order2Acc - order1Acc) < 0.08 && order2Pred.confidence >= order1Pred.confidence) {
      selectedModel = 'order-2';
      predictedMove = order2Pred.move;
      confidence = order2Pred.confidence;
    }
  }

  return {
    predictedMove,
    modelUsed: selectedModel,
    confidence,
    order1Predicted: order1Pred.move,
    order2Predicted: order2Pred?.move,
    order1Confidence: order1Pred.confidence,
    order2Confidence: order2Pred?.confidence,
  };
}

/**
 * Pure function to choose the bot's move given game state and history.
 */
export function chooseMove(
  state: AdaptiveAIState,
  history: readonly Move[],
  rng: () => number = Math.random
): BotDecision {
  const startTime = typeof performance !== 'undefined' ? performance.now() : Date.now();

  const prediction = predictNextMove(state, history, rng);
  const isColdStart = history.length < state.config.coldStartRounds;
  const isExploration = rng() < state.config.epsilon;

  let botMove: Move;
  let finalModelUsed: ModelType = prediction.modelUsed;

  if (isColdStart) {
    botMove = ALL_MOVES[Math.floor(rng() * ALL_MOVES.length)];
    finalModelUsed = 'cold-start';
  } else if (isExploration) {
    botMove = ALL_MOVES[Math.floor(rng() * ALL_MOVES.length)];
    finalModelUsed = 'random';
  } else {
    botMove = getBeatingMove(prediction.predictedMove);
  }

  const endTime = typeof performance !== 'undefined' ? performance.now() : Date.now();
  const decisionLatencyMs = Math.max(0.01, endTime - startTime);

  return {
    botMove,
    predictedMove: prediction.predictedMove,
    modelUsed: finalModelUsed,
    confidence: prediction.confidence,
    decisionLatencyMs,
  };
}

/**
 * Pure function to update the Adaptive AI state with exponential decay and new move observation.
 */
export function updateModel(
  state: AdaptiveAIState,
  actualMove: Move,
  predictedMove?: Move,
  modelUsed?: ModelType,
  historyBeforeMove: readonly Move[] = []
): AdaptiveAIState {
  const gamma = state.config.gamma;
  const rollingWindow = state.config.rollingWindowSize;

  // 1. Exponential decay on Order-1 table
  const newOrder1Table: Record<Move, Record<Move, number>> = {
    rock: { ...state.order1Table.rock },
    paper: { ...state.order1Table.paper },
    scissors: { ...state.order1Table.scissors },
  };

  for (const m1 of ALL_MOVES) {
    for (const m2 of ALL_MOVES) {
      newOrder1Table[m1][m2] = newOrder1Table[m1][m2] * gamma;
    }
  }

  // 2. Exponential decay on Order-2 table
  const newOrder2Table: Record<string, Record<Move, number>> = {};
  for (const key of Object.keys(state.order2Table)) {
    newOrder2Table[key] = {
      rock: state.order2Table[key].rock * gamma,
      paper: state.order2Table[key].paper * gamma,
      scissors: state.order2Table[key].scissors * gamma,
    };
  }

  // 3. Update accuracy tracking for Order-1 & Order-2 BEFORE updating tables
  let newOrder1History = [...state.order1History];
  let newOrder2History = [...state.order2History];
  let o1Total = state.order1TotalPredictions;
  let o1Correct = state.order1CorrectPredictions;
  let o2Total = state.order2TotalPredictions;
  let o2Correct = state.order2CorrectPredictions;

  if (historyBeforeMove.length >= 1) {
    const lastMove = historyBeforeMove[historyBeforeMove.length - 1];
    const o1Dist = state.order1Table[lastMove] || createInitialMoveRecord();
    const o1P = predictFromDistribution(o1Dist, state.config.laplaceSmoothing);
    const isO1Correct = o1P.move === actualMove ? 1 : 0;

    newOrder1History.push(isO1Correct);
    if (newOrder1History.length > rollingWindow) {
      newOrder1History.shift();
    }
    o1Total += 1;
    if (isO1Correct === 1) o1Correct += 1;
  }

  if (historyBeforeMove.length >= 2) {
    const prev2 = historyBeforeMove[historyBeforeMove.length - 2];
    const prev1 = historyBeforeMove[historyBeforeMove.length - 1];
    const key = `${prev2},${prev1}`;
    const o2Dist = state.order2Table[key] || createInitialMoveRecord();
    const o2P = predictFromDistribution(o2Dist, state.config.laplaceSmoothing);
    const isO2Correct = o2P.move === actualMove ? 1 : 0;

    newOrder2History.push(isO2Correct);
    if (newOrder2History.length > rollingWindow) {
      newOrder2History.shift();
    }
    o2Total += 1;
    if (isO2Correct === 1) o2Correct += 1;
  }

  // 4. Increment counts for observed move
  if (historyBeforeMove.length >= 1) {
    const lastMove = historyBeforeMove[historyBeforeMove.length - 1];
    newOrder1Table[lastMove][actualMove] = (newOrder1Table[lastMove][actualMove] || 0) + 1.0;
  }

  if (historyBeforeMove.length >= 2) {
    const prev2 = historyBeforeMove[historyBeforeMove.length - 2];
    const prev1 = historyBeforeMove[historyBeforeMove.length - 1];
    const key = `${prev2},${prev1}`;
    if (!newOrder2Table[key]) {
      newOrder2Table[key] = createInitialMoveRecord();
    }
    newOrder2Table[key][actualMove] = (newOrder2Table[key][actualMove] || 0) + 1.0;
  }

  return {
    config: state.config,
    roundCount: state.roundCount + 1,
    order1Table: newOrder1Table,
    order2Table: newOrder2Table,
    order1History: newOrder1History,
    order2History: newOrder2History,
    order1TotalPredictions: o1Total,
    order1CorrectPredictions: o1Correct,
    order2TotalPredictions: o2Total,
    order2CorrectPredictions: o2Correct,
  };
}
"""
write_file("packages/core/src/ai.ts", ai_ts)

# 6. packages/core/src/logger.ts
logger_ts = """import { RoundLog, SummaryStats, ModelAccuracyStats, ModelType, Outcome } from './types';
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

  return [headers.join(','), ...rows.map((row) => row.join(','))].join('\\n');
}
"""
write_file("packages/core/src/logger.ts", logger_ts)

# 7. packages/core/src/classifier.ts
classifier_ts = """import { Move, Landmark3D, HandClassificationResult } from './types';

/**
 * 21 Landmark index reference in MediaPipe:
 * 0: Wrist
 * Thumb: 1: CMC, 2: MCP, 3: IP, 4: TIP
 * Index: 5: MCP, 6: PIP, 7: DIP, 8: TIP
 * Middle: 9: MCP, 10: PIP, 11: DIP, 12: TIP
 * Ring: 13: MCP, 14: PIP, 15: DIP, 16: TIP
 * Pinky: 17: MCP, 18: PIP, 19: DIP, 20: TIP
 */

function distance3D(a: Landmark3D, b: Landmark3D): number {
  const dx = a.x - b.x;
  const dy = a.y - b.y;
  const dz = a.z - b.z;
  return Math.sqrt(dx * dx + dy * dy + dz * dz);
}

/**
 * Evaluates finger curl by comparing the distance from fingertip to wrist
 * against the distance from PIP joint to wrist.
 * In a curled finger, tip is closer to wrist than PIP is to wrist.
 */
function isFingerExtended(
  wrist: Landmark3D,
  mcp: Landmark3D,
  pip: Landmark3D,
  tip: Landmark3D
): boolean {
  const tipDist = distance3D(tip, wrist);
  const pipDist = distance3D(pip, wrist);
  const mcpDist = distance3D(mcp, wrist);

  return tipDist > pipDist * 1.1 && tipDist > mcpDist * 1.25;
}

/**
 * Evaluates thumb extension relative to index MCP and wrist.
 */
function isThumbExtended(
  wrist: Landmark3D,
  cmc: Landmark3D,
  mcp: Landmark3D,
  tip: Landmark3D,
  indexMcp: Landmark3D
): boolean {
  const thumbTipDistToIndexMcp = distance3D(tip, indexMcp);
  const thumbMcpDistToIndexMcp = distance3D(mcp, indexMcp);
  const tipDistToWrist = distance3D(tip, wrist);
  const cmcDistToWrist = distance3D(cmc, wrist);

  return thumbTipDistToIndexMcp > thumbMcpDistToIndexMcp * 1.15 && tipDistToWrist > cmcDistToWrist * 1.15;
}

/**
 * Geometric classifier for 21 MediaPipe hand landmarks.
 * Classifies 'rock', 'paper', or 'scissors' with confidence metric.
 */
export function classifyHandGesture(landmarks: Landmark3D[]): HandClassificationResult {
  if (!landmarks || landmarks.length < 21) {
    return {
      move: null,
      confidence: 0,
      fingersExtended: { thumb: false, index: false, middle: false, ring: false, pinky: false },
      reason: 'Incomplete hand landmarks (expected 21 points)',
    };
  }

  const wrist = landmarks[0];

  const thumbExt = isThumbExtended(wrist, landmarks[1], landmarks[2], landmarks[4], landmarks[5]);
  const indexExt = isFingerExtended(wrist, landmarks[5], landmarks[6], landmarks[8]);
  const middleExt = isFingerExtended(wrist, landmarks[9], landmarks[10], landmarks[12]);
  const ringExt = isFingerExtended(wrist, landmarks[13], landmarks[14], landmarks[16]);
  const pinkyExt = isFingerExtended(wrist, landmarks[17], landmarks[18], landmarks[20]);

  const fingersExtended = {
    thumb: thumbExt,
    index: indexExt,
    middle: middleExt,
    ring: ringExt,
    pinky: pinkyExt,
  };

  const extendedCount = [indexExt, middleExt, ringExt, pinkyExt].filter(Boolean).length;

  // Rock: 0 fingers extended (all 4 curled). Thumb usually tucked.
  if (extendedCount === 0) {
    const confidence = thumbExt ? 0.82 : 0.96;
    return { move: 'rock', confidence, fingersExtended };
  }

  // Paper: 4 fingers extended (all open), thumb usually extended.
  if (extendedCount >= 3) {
    if (indexExt && middleExt && ringExt && pinkyExt) {
      const confidence = thumbExt ? 0.98 : 0.88;
      return { move: 'paper', confidence, fingersExtended };
    }
    if (extendedCount === 3 && (thumbExt || pinkyExt)) {
      return { move: 'paper', confidence: 0.78, fingersExtended };
    }
  }

  // Scissors: Index and Middle extended; Ring and Pinky curled.
  if (indexExt && middleExt && !ringExt && !pinkyExt) {
    return { move: 'scissors', confidence: 0.94, fingersExtended };
  }

  // Partial scissors tolerance (e.g. index extended, middle borderline)
  if (indexExt && !ringExt && !pinkyExt && !middleExt) {
    return { move: 'scissors', confidence: 0.65, fingersExtended, reason: 'Index extended but middle curled' };
  }

  return {
    move: null,
    confidence: 0.35,
    fingersExtended,
    reason: 'Ambiguous hand pose — please show clear Rock, Paper, or Scissors',
  };
}
"""
write_file("packages/core/src/classifier.ts", classifier_ts)

# 8. packages/core/src/index.ts
index_ts = """export * from './types';
export * from './rules';
export * from './ai';
export * from './logger';
export * from './classifier';
"""
write_file("packages/core/src/index.ts", index_ts)

# 9. packages/core/src/simulate.ts
simulate_ts = """import * as fs from 'fs';
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
  fs.writeFileSync(summaryCsvPath, [csvHeaders, ...csvRows].join('\\n'), 'utf-8');

  console.log(`\\nAll report data successfully written to: ${targetDir}`);
}

if (require.main === module || (typeof process !== 'undefined' && process.argv[1]?.includes('simulate'))) {
  runAllSimulations();
}
"""
write_file("packages/core/src/simulate.ts", simulate_ts)

print("Core source files and simulate.ts created!")
