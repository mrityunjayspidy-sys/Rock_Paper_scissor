import { Landmark3D, HandClassificationResult, Move } from './types';

/**
 * 21 Landmark index reference in MediaPipe:
 * 0: Wrist
 * Thumb: 1: CMC, 2: MCP, 3: IP, 4: TIP
 * Index: 5: MCP, 6: PIP, 7: DIP, 8: TIP
 * Middle: 9: MCP, 10: PIP, 11: DIP, 12: TIP
 * Ring: 13: MCP, 14: PIP, 15: DIP, 16: TIP
 * Pinky: 17: MCP, 18: PIP, 19: DIP, 20: TIP
 */

export function distance3D(a: Landmark3D, b: Landmark3D): number {
  const dx = a.x - b.x;
  const dy = a.y - b.y;
  const dz = (a.z || 0) - (b.z || 0);
  return Math.sqrt(dx * dx + dy * dy + dz * dz);
}

/**
 * Robust evaluation of finger extension using scale-invariant multi-metric analysis:
 * 1. Ratio of (Tip-to-Wrist) / (PIP-to-Wrist)
 * 2. Ratio of (Tip-to-MCP) / (PIP-to-MCP)
 * 3. Tip distance to palm center relative to palm scale
 */
export function isFingerExtendedRobust(
  wrist: Landmark3D,
  mcp: Landmark3D,
  pip: Landmark3D,
  dip: Landmark3D,
  tip: Landmark3D,
  palmScale: number
): boolean {
  const tipToWrist = distance3D(tip, wrist);
  const pipToWrist = distance3D(pip, wrist);
  const tipToMcp = distance3D(tip, mcp);
  const pipToMcp = distance3D(pip, mcp);
  const dipToMcp = distance3D(dip, mcp);

  // Metric 1: Ratio relative to wrist
  const wristRatio = tipToWrist / Math.max(0.001, pipToWrist);
  // Metric 2: Ratio relative to MCP joint
  const mcpRatio = tipToMcp / Math.max(0.001, pipToMcp);
  // Metric 3: Extension compared to DIP
  const isFartherThanDip = tipToMcp > dipToMcp * 1.05;

  // Curled detection: if tip is folded back closer to MCP or wrist
  if (mcpRatio < 1.05 || tipToMcp < palmScale * 0.45) {
    return false;
  }

  // Extended detection: strong MCP extension and wrist extension
  if (mcpRatio > 1.25 && (wristRatio > 1.02 || isFartherThanDip)) {
    return true;
  }

  // Moderate extension
  return tipToMcp > palmScale * 0.7 && wristRatio > 1.0;
}

/**
 * Robust evaluation of thumb extension relative to wrist and index MCP.
 */
export function isThumbExtendedRobust(
  wrist: Landmark3D,
  _cmc: Landmark3D,
  mcp: Landmark3D,
  ip: Landmark3D,
  tip: Landmark3D,
  indexMcp: Landmark3D,
  palmScale: number
): boolean {
  const tipToIndexMcp = distance3D(tip, indexMcp);
  const mcpToIndexMcp = distance3D(mcp, indexMcp);
  const tipToWrist = distance3D(tip, wrist);
  const ipToWrist = distance3D(ip, wrist);

  const thumbSpanRatio = tipToIndexMcp / Math.max(0.001, mcpToIndexMcp);
  const isExtendedFromWrist = tipToWrist > ipToWrist * 1.05;

  return thumbSpanRatio > 1.15 && (isExtendedFromWrist || tipToIndexMcp > palmScale * 0.65);
}

/**
 * Ultra-fast, high-accuracy geometric hand landmark classifier.
 * Handles rapid motion, tilting, variable camera distances, and angles.
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
  const middleMcp = landmarks[9];
  const palmScale = Math.max(0.05, distance3D(wrist, middleMcp));

  const thumbExt = isThumbExtendedRobust(
    wrist,
    landmarks[1],
    landmarks[2],
    landmarks[3],
    landmarks[4],
    landmarks[5],
    palmScale
  );

  const indexExt = isFingerExtendedRobust(
    wrist,
    landmarks[5],
    landmarks[6],
    landmarks[7],
    landmarks[8],
    palmScale
  );

  const middleExt = isFingerExtendedRobust(
    wrist,
    landmarks[9],
    landmarks[10],
    landmarks[11],
    landmarks[12],
    palmScale
  );

  const ringExt = isFingerExtendedRobust(
    wrist,
    landmarks[13],
    landmarks[14],
    landmarks[15],
    landmarks[16],
    palmScale
  );

  const pinkyExt = isFingerExtendedRobust(
    wrist,
    landmarks[17],
    landmarks[18],
    landmarks[19],
    landmarks[20],
    palmScale
  );

  const fingersExtended = {
    thumb: thumbExt,
    index: indexExt,
    middle: middleExt,
    ring: ringExt,
    pinky: pinkyExt,
  };

  const mainFingers = [indexExt, middleExt, ringExt, pinkyExt];
  const extendedCount = mainFingers.filter(Boolean).length;

  let move: Move | null = null;
  let confidence = 0;
  let reason: string | undefined = undefined;

  // 1. SCISSORS: Index + Middle extended, Ring + Pinky curled
  if (indexExt && middleExt && !ringExt && !pinkyExt) {
    move = 'scissors';
    confidence = 0.96;
  }
  // Alternate Scissors: Index extended, Middle extended (or nearly extended), Ring & Pinky tightly curled
  else if (indexExt && !ringExt && !pinkyExt) {
    const middleTipToMcp = distance3D(landmarks[12], landmarks[9]);
    if (middleTipToMcp > palmScale * 0.55) {
      move = 'scissors';
      confidence = 0.88;
    }
  }

  // 2. ROCK: All 4 main fingers curled
  if (!move && extendedCount === 0) {
    move = 'rock';
    confidence = thumbExt ? 0.90 : 0.98;
  }
  // Tolerant Rock: at most 1 finger marginally loose while others tightly curled
  else if (!move && extendedCount === 1) {
    const curledCount = [
      distance3D(landmarks[8], landmarks[5]) < palmScale * 0.65,
      distance3D(landmarks[12], landmarks[9]) < palmScale * 0.65,
      distance3D(landmarks[16], landmarks[13]) < palmScale * 0.65,
      distance3D(landmarks[20], landmarks[17]) < palmScale * 0.65,
    ].filter(Boolean).length;

    if (curledCount >= 3) {
      move = 'rock';
      confidence = 0.85;
    }
  }

  // 3. PAPER: All 4 main fingers extended, or 3+ fingers fully open
  if (!move) {
    if (indexExt && middleExt && ringExt && pinkyExt) {
      move = 'paper';
      confidence = thumbExt ? 0.99 : 0.94;
    } else if (extendedCount >= 3 && (thumbExt || indexExt)) {
      move = 'paper';
      confidence = 0.86;
    }
  }

  if (!move) {
    confidence = 0.35;
    reason = 'Ambiguous hand pose — show clear Rock ✊, Paper ✋, or Scissors ✌️';
  }

  return {
    move,
    confidence,
    fingersExtended,
    reason,
  };
}
