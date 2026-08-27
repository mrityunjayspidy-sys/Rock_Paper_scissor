import {
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
  _predictedMove?: Move,
  _modelUsed?: ModelType,
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
