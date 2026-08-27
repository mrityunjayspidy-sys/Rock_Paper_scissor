import React, { useEffect, useRef, useState, useCallback } from 'react';
import { FilesetResolver, HandLandmarker } from '@mediapipe/tasks-vision';
import { Move, HandClassificationResult, classifyHandGesture } from '@rps/core';
import { RefreshCw, AlertCircle, Zap, ShieldCheck, Play, Sparkles } from 'lucide-react';
import { sounds } from '../sound';

interface CameraGameProps {
  onPlayMove: (move: Move) => void;
  disabled?: boolean;
}

export type TriggerMode = 'instant' | '1s' | '3s';

export const CameraGame: React.FC<CameraGameProps> = ({ onPlayMove, disabled = false }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const landmarkerRef = useRef<HandLandmarker | null>(null);

  const [cameraLoading, setCameraLoading] = useState(true);
  const [cameraError, setCameraError] = useState<string | null>(null);
  const [modelLoading, setModelLoading] = useState(true);

  const [triggerMode, setTriggerMode] = useState<TriggerMode>('instant');
  const [currentGesture, setCurrentGesture] = useState<HandClassificationResult | null>(null);
  const [countdown, setCountdown] = useState<number | null>(null);
  const [repositionWarning, setRepositionWarning] = useState<string | null>(null);
  const [isShootingFlash, setIsShootingFlash] = useState(false);

  // Auto-Detect Stabilization State
  const [autoLockProgress, setAutoLockProgress] = useState(0);
  const stableMoveRef = useRef<Move | null>(null);
  const stableFramesCountRef = useRef(0);
  const isTriggeringRef = useRef(false);

  const latestGestureRef = useRef<HandClassificationResult | null>(null);
  const recentHistoryRef = useRef<HandClassificationResult[]>([]);

  // Initialize MediaPipe Tasks Vision HandLandmarker
  useEffect(() => {
    let isCancelled = false;

    async function initMediaPipe() {
      try {
        setModelLoading(true);
        const vision = await FilesetResolver.forVisionTasks(
          'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.18/wasm'
        );
        const handLandmarker = await HandLandmarker.createFromOptions(vision, {
          baseOptions: {
            modelAssetPath:
              'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task',
            delegate: 'GPU',
          },
          runningMode: 'VIDEO',
          numHands: 1,
        });

        if (!isCancelled) {
          landmarkerRef.current = handLandmarker;
          setModelLoading(false);
        }
      } catch (err: unknown) {
        console.error('Failed to load MediaPipe HandLandmarker:', err);
        if (!isCancelled) {
          setModelLoading(false);
          setCameraError('Failed to initialize Vision AI model. Please check network connection or switch to No Camera mode.');
        }
      }
    }

    initMediaPipe();

    return () => {
      isCancelled = true;
      if (landmarkerRef.current) {
        landmarkerRef.current.close();
      }
    };
  }, []);

  // Initialize Webcam Stream
  useEffect(() => {
    let stream: MediaStream | null = null;

    async function setupCamera() {
      try {
        setCameraLoading(true);
        setCameraError(null);
        stream = await navigator.mediaDevices.getUserMedia({
          video: {
            width: { ideal: 640 },
            height: { ideal: 480 },
            frameRate: { ideal: 60, min: 30 },
            facingMode: 'user',
          },
          audio: false,
        });

        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          videoRef.current.onloadedmetadata = () => {
            videoRef.current?.play();
            setCameraLoading(false);
          };
        }
      } catch (err: unknown) {
        console.error('Camera access error:', err);
        setCameraLoading(false);
        setCameraError('Camera access denied or unavailable. Please grant webcam permission or switch to No Camera mode.');
      }
    }

    setupCamera();

    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  // Instant Snapshot Evaluation
  const evaluateAndDispatchMove = useCallback((targetMove?: Move) => {
    if (disabled || isTriggeringRef.current) return;
    isTriggeringRef.current = true;
    setIsShootingFlash(true);
    sounds.playShoot();

    let candidateMove: Move | null = targetMove || null;

    if (!candidateMove) {
      const candidate = latestGestureRef.current;
      if (candidate && candidate.move && candidate.confidence >= 0.75) {
        candidateMove = candidate.move;
      } else {
        const validRecent = recentHistoryRef.current.filter((g) => g.move && g.confidence >= 0.75);
        if (validRecent.length > 0) {
          candidateMove = validRecent[validRecent.length - 1].move;
        }
      }
    }

    if (candidateMove) {
      onPlayMove(candidateMove);
      setRepositionWarning(null);
    } else {
      setRepositionWarning(
        'Hand pose not recognized clearly. Please show clear Rock ✊, Paper ✋, or Scissors ✌️ in camera view.'
      );
    }

    setTimeout(() => {
      setIsShootingFlash(false);
      isTriggeringRef.current = false;
    }, 250);
    setCountdown(null);
    setAutoLockProgress(0);
    stableFramesCountRef.current = 0;
  }, [disabled, onPlayMove]);

  // Real-time High-FPS Detection Loop
  useEffect(() => {
    let animId: number;
    const REQUIRED_STABLE_FRAMES = 14;

    const renderLoop = () => {
      if (
        videoRef.current &&
        videoRef.current.readyState >= 2 &&
        landmarkerRef.current &&
        canvasRef.current
      ) {
        const video = videoRef.current;
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');

        if (ctx) {
          canvas.width = video.videoWidth || 640;
          canvas.height = video.videoHeight || 480;
          ctx.clearRect(0, 0, canvas.width, canvas.height);

          const startTimeMs = performance.now();
          const results = landmarkerRef.current.detectForVideo(video, startTimeMs);

          if (results.landmarks && results.landmarks.length > 0) {
            const landmarks = results.landmarks[0];
            const classification = classifyHandGesture(landmarks);

            latestGestureRef.current = classification;
            recentHistoryRef.current.push(classification);
            if (recentHistoryRef.current.length > 5) {
              recentHistoryRef.current.shift();
            }

            setCurrentGesture(classification);

            // Auto Instant Mode Tracking Logic
            if (
              triggerMode === 'instant' &&
              !disabled &&
              !isTriggeringRef.current &&
              countdown === null &&
              classification.move &&
              classification.confidence >= 0.85
            ) {
              if (stableMoveRef.current === classification.move) {
                stableFramesCountRef.current += 1;
              } else {
                stableMoveRef.current = classification.move;
                stableFramesCountRef.current = 1;
              }

              const progress = Math.min(1.0, stableFramesCountRef.current / REQUIRED_STABLE_FRAMES);
              setAutoLockProgress(progress);

              if (stableFramesCountRef.current >= REQUIRED_STABLE_FRAMES) {
                evaluateAndDispatchMove(classification.move);
              }
            } else if (triggerMode === 'instant' && (!classification.move || classification.confidence < 0.7)) {
              stableFramesCountRef.current = Math.max(0, stableFramesCountRef.current - 2);
              setAutoLockProgress(stableFramesCountRef.current / REQUIRED_STABLE_FRAMES);
            }

            // Draw Monochrome Hand Skeleton Overlay
            ctx.save();
            ctx.strokeStyle = classification.move ? '#ffffff' : '#71717a';
            ctx.lineWidth = 3;
            ctx.fillStyle = '#ffffff';

            const connections = [
              [0, 1], [1, 2], [2, 3], [3, 4],       // Thumb
              [0, 5], [5, 6], [6, 7], [7, 8],       // Index
              [0, 9], [9, 10], [10, 11], [11, 12],  // Middle
              [0, 13], [13, 14], [14, 15], [15, 16],// Ring
              [0, 17], [17, 18], [18, 19], [19, 20],// Pinky
              [5, 9], [9, 13], [13, 17]              // Base
            ];

            ctx.beginPath();
            for (const [start, end] of connections) {
              const p1 = landmarks[start];
              const p2 = landmarks[end];
              ctx.moveTo(p1.x * canvas.width, p1.y * canvas.height);
              ctx.lineTo(p2.x * canvas.width, p2.y * canvas.height);
            }
            ctx.stroke();

            for (const lm of landmarks) {
              const x = lm.x * canvas.width;
              const y = lm.y * canvas.height;
              ctx.beginPath();
              ctx.arc(x, y, 4, 0, 2 * Math.PI);
              ctx.fill();
            }
            ctx.restore();
          } else {
            latestGestureRef.current = null;
            setCurrentGesture(null);
            stableFramesCountRef.current = 0;
            setAutoLockProgress(0);
          }
        }
      }
      animId = requestAnimationFrame(renderLoop);
    };

    animId = requestAnimationFrame(renderLoop);
    return () => cancelAnimationFrame(animId);
  }, [triggerMode, disabled, countdown, evaluateAndDispatchMove]);

  // Handle 3-2-1 / 1s Shoot Countdown
  const startShootCountdown = useCallback(() => {
    if (disabled || countdown !== null || isTriggeringRef.current) return;
    setRepositionWarning(null);

    if (triggerMode === '1s') {
      setCountdown(1);
      sounds.playTick(600);
      setTimeout(() => {
        setCountdown(0);
        evaluateAndDispatchMove();
      }, 700);
      return;
    }

    setCountdown(3);
    sounds.playTick(440);

    const timer3 = setTimeout(() => {
      setCountdown(2);
      sounds.playTick(550);
    }, 850);

    const timer2 = setTimeout(() => {
      setCountdown(1);
      sounds.playTick(660);
    }, 1700);

    const timer1 = setTimeout(() => {
      setCountdown(0);
      evaluateAndDispatchMove();
    }, 2550);

    return () => {
      clearTimeout(timer3);
      clearTimeout(timer2);
      clearTimeout(timer1);
    };
  }, [disabled, countdown, triggerMode, evaluateAndDispatchMove]);

  // Keyboard shortcut Space
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.code === 'Space') {
        e.preventDefault();
        if (triggerMode === 'instant') {
          evaluateAndDispatchMove();
        } else {
          startShootCountdown();
        }
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [triggerMode, evaluateAndDispatchMove, startShootCountdown]);

  const getMoveEmoji = (move: Move | null) => {
    switch (move) {
      case 'rock':
        return '✊ Rock';
      case 'paper':
        return '✋ Paper';
      case 'scissors':
        return '✌️ Scissors';
      default:
        return '❓ Show hand...';
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto px-4 py-6 flex flex-col items-center">
      {/* Top Controls Bar */}
      <div className="w-full max-w-2xl flex flex-wrap items-center justify-between gap-3 mb-3">
        <div className="flex items-center gap-2 text-xs text-neutral-400">
          <ShieldCheck className="w-4 h-4 text-white" />
          <span>High-Speed 60fps Detection</span>
        </div>

        {/* Mode Selector Tabs */}
        <div className="flex items-center gap-1 bg-neutral-900 p-1 rounded-2xl border border-white/10 text-xs">
          <button
            onClick={() => setTriggerMode('instant')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
              triggerMode === 'instant'
                ? 'bg-white text-black shadow-md'
                : 'text-neutral-400 hover:text-white'
            }`}
          >
            <Zap className="w-3.5 h-3.5 text-current" />
            <span>Instant Auto-Detect</span>
          </button>

          <button
            onClick={() => setTriggerMode('1s')}
            className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-all ${
              triggerMode === '1s'
                ? 'bg-white/15 text-white border border-white/20 font-bold'
                : 'text-neutral-400 hover:text-white'
            }`}
          >
            ⚡ 1s Quick
          </button>

          <button
            onClick={() => setTriggerMode('3s')}
            className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-all ${
              triggerMode === '3s'
                ? 'bg-white/15 text-white border border-white/20 font-bold'
                : 'text-neutral-400 hover:text-white'
            }`}
          >
            ⏱ 3s Countdown
          </button>
        </div>
      </div>

      {/* Video Container */}
      <div
        className={`relative w-full max-w-2xl aspect-[4/3] bg-black rounded-3xl overflow-hidden border-2 shadow-2xl flex items-center justify-center transition-all duration-150 ${
          isShootingFlash
            ? 'border-white ring-8 ring-white/30'
            : autoLockProgress > 0.4
            ? 'border-white shadow-white/10'
            : currentGesture?.move
            ? 'border-white/50 shadow-white/5'
            : 'border-white/10'
        }`}
      >
        {cameraError ? (
          <div className="p-8 text-center max-w-md">
            <AlertCircle className="w-12 h-12 text-white mx-auto mb-4" />
            <p className="text-neutral-200 text-sm font-medium mb-4">{cameraError}</p>
          </div>
        ) : cameraLoading || modelLoading ? (
          <div className="flex flex-col items-center gap-3 text-neutral-300">
            <RefreshCw className="w-8 h-8 animate-spin text-white" />
            <span className="text-sm font-medium">
              {modelLoading ? 'Initializing Vision AI Engine...' : 'Accessing Camera Feed...'}
            </span>
          </div>
        ) : null}

        <video
          ref={videoRef}
          playsInline
          muted
          className={`w-full h-full object-cover transform -scale-x-100 ${
            cameraLoading || modelLoading ? 'hidden' : 'block'
          }`}
        />

        <canvas
          ref={canvasRef}
          className="absolute inset-0 w-full h-full pointer-events-none transform -scale-x-100"
        />

        {/* Live Detected Gesture & Finger Status HUD */}
        {!cameraLoading && !modelLoading && !cameraError && (
          <div className="absolute top-4 left-4 right-4 flex items-center justify-between pointer-events-none">
            {/* Gesture Badge */}
            <div className="bg-black/90 backdrop-blur-xl px-3.5 py-1.5 rounded-xl border border-white/20 flex items-center gap-2 shadow-lg">
              <span className={`w-2.5 h-2.5 rounded-full ${currentGesture?.move ? 'bg-white animate-pulse' : 'bg-neutral-600'}`} />
              <span className="text-xs text-neutral-400 font-medium">Pose:</span>
              <span className="text-xs font-bold text-white font-mono">
                {getMoveEmoji(currentGesture?.move || null)}
              </span>
              {currentGesture?.confidence ? (
                <span className="text-[10px] text-neutral-400 font-mono font-bold">
                  ({(currentGesture.confidence * 100).toFixed(0)}%)
                </span>
              ) : null}
            </div>

            {/* Finger Extension Indicators */}
            {currentGesture?.fingersExtended && (
              <div className="bg-black/90 backdrop-blur-xl px-3 py-1.5 rounded-xl border border-white/20 flex items-center gap-2 text-[10px] font-mono">
                <span className={currentGesture.fingersExtended.thumb ? 'text-white font-bold' : 'text-neutral-600'}>T</span>
                <span className={currentGesture.fingersExtended.index ? 'text-white font-bold' : 'text-neutral-600'}>I</span>
                <span className={currentGesture.fingersExtended.middle ? 'text-white font-bold' : 'text-neutral-600'}>M</span>
                <span className={currentGesture.fingersExtended.ring ? 'text-white font-bold' : 'text-neutral-600'}>R</span>
                <span className={currentGesture.fingersExtended.pinky ? 'text-white font-bold' : 'text-neutral-600'}>P</span>
              </div>
            )}
          </div>
        )}

        {/* Auto-Lock Progress Ring Overlay */}
        {triggerMode === 'instant' && autoLockProgress > 0 && (
          <div className="absolute bottom-4 left-4 right-4 bg-black/90 backdrop-blur-xl p-3.5 rounded-2xl border border-white/30 flex items-center gap-3 animate-pop-in pointer-events-none">
            <Sparkles className="w-5 h-5 text-white animate-spin" />
            <div className="flex-1">
              <div className="flex justify-between text-xs font-bold mb-1.5">
                <span className="text-white">Auto-Triggering: {getMoveEmoji(currentGesture?.move || null)}</span>
                <span className="text-white font-mono">{(autoLockProgress * 100).toFixed(0)}%</span>
              </div>
              <div className="w-full h-2 rounded-full bg-neutral-800 overflow-hidden">
                <div
                  className="h-full bg-white rounded-full transition-all duration-75"
                  style={{ width: `${autoLockProgress * 100}%` }}
                />
              </div>
            </div>
          </div>
        )}

        {/* 3-2-1 Shoot Overlay */}
        {countdown !== null && (
          <div className="absolute inset-0 bg-black/80 backdrop-blur-sm flex flex-col items-center justify-center animate-pop-in pointer-events-none z-30">
            <span className="text-8xl sm:text-9xl font-black font-heading text-white animate-pulse drop-shadow-[0_0_35px_rgba(255,255,255,0.4)]">
              {countdown === 0 ? 'SHOOT!' : countdown}
            </span>
            <span className="text-sm text-neutral-300 mt-2 font-medium tracking-wide">
              {countdown === 0 ? 'Analyzing Live Pose...' : 'Prepare Gesture!'}
            </span>
          </div>
        )}
      </div>

      {/* Reposition Warning Notification */}
      {repositionWarning && (
        <div className="mt-4 p-4 rounded-2xl bg-neutral-900 border border-white/20 flex items-center gap-3 text-neutral-300 text-xs sm:text-sm max-w-xl animate-pop-in">
          <AlertCircle className="w-5 h-5 text-white shrink-0" />
          <div className="flex-1">
            <span className="font-semibold block text-white">Pose Not Recognized</span>
            <span>{repositionWarning}</span>
          </div>
          <button
            onClick={() => setRepositionWarning(null)}
            className="text-white font-bold text-xs underline"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Action Controls */}
      <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
        {triggerMode === 'instant' ? (
          <div className="flex flex-col items-center gap-2">
            <div className="px-6 py-3 rounded-2xl bg-neutral-900 border border-white/15 text-neutral-200 text-sm font-medium flex items-center gap-2 shadow-lg">
              <span className="w-2 h-2 rounded-full bg-white animate-ping" />
              <span>Show Rock ✊, Paper ✋, or Scissors ✌️ in camera to auto-play!</span>
            </div>
            <button
              onClick={() => evaluateAndDispatchMove()}
              disabled={disabled || cameraLoading || modelLoading || !currentGesture?.move}
              className="px-6 py-2.5 rounded-xl bg-neutral-900 hover:bg-neutral-800 border border-white/20 text-neutral-300 hover:text-white text-xs font-semibold transition-all disabled:opacity-40 disabled:pointer-events-none"
            >
              Manual Force Trigger (Space)
            </button>
          </div>
        ) : (
          <button
            onClick={startShootCountdown}
            disabled={disabled || countdown !== null || cameraLoading || modelLoading}
            className="px-8 py-4 rounded-2xl bg-white text-black font-bold text-lg font-heading shadow-xl shadow-white/10 hover:bg-neutral-200 hover:-translate-y-0.5 active:scale-95 transition-all disabled:opacity-50 disabled:pointer-events-none flex items-center gap-2"
          >
            <Play className="w-5 h-5 text-black fill-current" />
            <span>Start {triggerMode === '1s' ? '1s Quick' : '3s'} Countdown</span>
          </button>
        )}
      </div>
    </div>
  );
};
