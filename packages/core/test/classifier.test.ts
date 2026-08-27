import { describe, it, expect } from 'vitest';
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
