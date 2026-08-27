import os

def write_file(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Updated: {path}")

# 1. apps/web/src/index.css
index_css = """:root {
  --bg-primary: #050505;
  --bg-secondary: #0a0a0a;
  --bg-card: rgba(18, 18, 18, 0.85);
  --border-card: rgba(255, 255, 255, 0.12);
  --accent-white: #ffffff;
  --accent-white-glow: rgba(255, 255, 255, 0.2);
  --text-main: #ffffff;
  --text-muted: #a1a1aa;
  --text-dim: #71717a;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  background-color: #000000;
  color: #f4f4f5;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  min-height: 100vh;
  overflow-x: hidden;
  background-image: 
    radial-gradient(circle at 50% 0%, rgba(255, 255, 255, 0.08) 0px, transparent 65%),
    radial-gradient(circle at 100% 100%, rgba(255, 255, 255, 0.03) 0px, transparent 50%),
    radial-gradient(circle at 0% 100%, rgba(255, 255, 255, 0.03) 0px, transparent 50%);
  background-attachment: fixed;
}

h1, h2, h3, .font-heading {
  font-family: 'Outfit', sans-serif;
}

.font-mono {
  font-family: 'JetBrains Mono', monospace;
}

/* Luxury Glassmorphism */
.glass-panel {
  background: var(--bg-card);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--border-card);
  border-radius: 1.25rem;
}

.glass-panel-glow {
  box-shadow: 0 0 30px -5px rgba(255, 255, 255, 0.1);
}

/* Animations */
@keyframes pulse-ring {
  0% { transform: scale(0.96); opacity: 0.9; }
  50% { transform: scale(1.04); opacity: 0.4; }
  100% { transform: scale(0.96); opacity: 0.9; }
}

.animate-pulse-ring {
  animation: pulse-ring 2.4s infinite ease-in-out;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

.animate-float {
  animation: float 3.5s ease-in-out infinite;
}

@keyframes pop-in {
  0% { transform: scale(0.94); opacity: 0; }
  70% { transform: scale(1.02); opacity: 1; }
  100% { transform: scale(1); opacity: 1; }
}

.animate-pop-in {
  animation: pop-in 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* Custom Luxury Scrollbar */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: #050505;
}
::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.4);
}
"""
write_file("apps/web/src/index.css", index_css)

# 2. apps/web/src/components/Header.tsx
header_tsx = """import React from 'react';
import { Sparkles, BarChart3, RotateCcw, Video, Keyboard } from 'lucide-react';
import { SummaryStats } from '@rps/core';

interface HeaderProps {
  mode: 'camera' | 'nocamera';
  stats: SummaryStats;
  onSwitchMode: () => void;
  onOpenStats: () => void;
  onReset: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  mode,
  stats,
  onSwitchMode,
  onOpenStats,
  onReset,
}) => {
  return (
    <header className="w-full border-b border-white/10 bg-black/85 backdrop-blur-xl sticky top-0 z-40 px-4 py-3.5">
      <div className="max-w-6xl mx-auto flex flex-wrap items-center justify-between gap-4">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-white text-black flex items-center justify-center shadow-lg shadow-white/10">
            <Sparkles className="w-5 h-5 text-black" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
              RPS Adaptive AI
              <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded-full bg-white/10 text-white border border-white/20">
                Markov v2
              </span>
            </h1>
            <p className="text-xs text-neutral-400">Order-1 & Order-2 Opponent Modeling</p>
          </div>
        </div>

        {/* Live HUD Quick Stats */}
        <div className="flex items-center gap-3 bg-neutral-900/90 px-4 py-1.5 rounded-xl border border-white/10 text-xs">
          <div className="flex items-center gap-1.5">
            <span className="text-neutral-400">Rounds:</span>
            <span className="font-mono font-semibold text-white">{stats.totalRounds}</span>
          </div>
          <span className="text-neutral-700">|</span>
          <div className="flex items-center gap-1.5">
            <span className="text-neutral-300">You:</span>
            <span className="font-mono font-semibold text-white">
              {stats.humanWins} ({(stats.humanWinRate * 100).toFixed(0)}%)
            </span>
          </div>
          <span className="text-neutral-700">|</span>
          <div className="flex items-center gap-1.5">
            <span className="text-neutral-400">Bot:</span>
            <span className="font-mono font-semibold text-neutral-200">
              {stats.botWins} ({(stats.botWinRate * 100).toFixed(0)}%)
            </span>
          </div>
          <span className="text-neutral-700">|</span>
          <div className="flex items-center gap-1.5">
            <span className="text-neutral-500">Ties:</span>
            <span className="font-mono font-semibold text-neutral-300">{stats.ties}</span>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2">
          <button
            onClick={onSwitchMode}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium bg-neutral-900 hover:bg-neutral-800 text-neutral-200 border border-white/15 transition-all hover:border-white/30"
            title="Switch input mode"
          >
            {mode === 'camera' ? (
              <>
                <Video className="w-3.5 h-3.5 text-white" />
                <span>Camera</span>
              </>
            ) : (
              <>
                <Keyboard className="w-3.5 h-3.5 text-white" />
                <span>No Camera</span>
              </>
            )}
          </button>

          <button
            onClick={onOpenStats}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold bg-white text-black hover:bg-neutral-200 shadow-md shadow-white/10 transition-all"
          >
            <BarChart3 className="w-3.5 h-3.5" />
            <span>Stats & Export</span>
          </button>

          <button
            onClick={onReset}
            className="p-2 rounded-xl text-neutral-400 hover:text-white hover:bg-neutral-900 border border-transparent hover:border-white/10 transition-colors"
            title="Reset game state"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
};
"""
write_file("apps/web/src/components/Header.tsx", header_tsx)

# 3. apps/web/src/components/ModeSelector.tsx
modeselector_tsx = """import React from 'react';
import { Camera, Keyboard, Sparkles, Brain, Cpu, ShieldCheck, ArrowRight } from 'lucide-react';

interface ModeSelectorProps {
  onSelectMode: (mode: 'camera' | 'nocamera') => void;
}

export const ModeSelector: React.FC<ModeSelectorProps> = ({ onSelectMode }) => {
  return (
    <div className="max-w-4xl mx-auto px-4 py-16 flex flex-col items-center justify-center min-h-[80vh] text-center">
      {/* Title Badge */}
      <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/5 border border-white/15 text-white text-xs font-mono font-medium mb-6 backdrop-blur-md">
        <Sparkles className="w-3.5 h-3.5 text-white" />
        Opponent-Modeling Adaptive Markov AI
      </div>

      <h1 className="text-4xl sm:text-6xl font-black text-white tracking-tight mb-4 font-heading">
        Beat the <span className="underline decoration-white/30 underline-offset-8">Adaptive AI</span>
      </h1>
      <p className="text-base sm:text-lg text-neutral-400 max-w-2xl mb-12">
        The bot analyzes your past move sequences using Order-1 & Order-2 Markov frequency tables with exponential decay (γ=0.94) to predict and counter your next move.
      </p>

      {/* Mode Selection Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-3xl">
        {/* Camera Mode */}
        <button
          onClick={() => onSelectMode('camera')}
          className="group relative p-8 rounded-3xl bg-neutral-950/80 border border-white/10 hover:border-white/40 transition-all duration-300 text-left hover:shadow-2xl hover:shadow-white/5 hover:-translate-y-1 flex flex-col justify-between"
        >
          <div>
            <div className="w-14 h-14 rounded-2xl bg-white/10 border border-white/20 flex items-center justify-center mb-6 group-hover:scale-105 group-hover:bg-white group-hover:text-black transition-all">
              <Camera className="w-7 h-7 text-white group-hover:text-black transition-colors" />
            </div>
            <div className="flex items-center justify-between mb-2">
              <h2 className="text-2xl font-bold text-white font-heading">Camera Mode</h2>
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-white text-black">
                Vision AI
              </span>
            </div>
            <p className="text-sm text-neutral-400 mb-6 leading-relaxed">
              Instant hand gesture detection via MediaPipe Vision. Features instant auto-trigger and 3-2-1 countdown.
            </p>
          </div>

          <div className="space-y-2.5 border-t border-white/10 pt-4 text-xs text-neutral-300">
            <div className="flex items-center gap-2">
              <Cpu className="w-3.5 h-3.5 text-white" />
              <span>Real-time 21-point hand landmark tracking</span>
            </div>
            <div className="flex items-center gap-2">
              <ShieldCheck className="w-3.5 h-3.5 text-white" />
              <span>100% Client-side, zero video upload</span>
            </div>
          </div>
        </button>

        {/* No Camera Mode */}
        <button
          onClick={() => onSelectMode('nocamera')}
          className="group relative p-8 rounded-3xl bg-neutral-950/80 border border-white/10 hover:border-white/40 transition-all duration-300 text-left hover:shadow-2xl hover:shadow-white/5 hover:-translate-y-1 flex flex-col justify-between"
        >
          <div>
            <div className="w-14 h-14 rounded-2xl bg-white/10 border border-white/20 flex items-center justify-center mb-6 group-hover:scale-105 group-hover:bg-white group-hover:text-black transition-all">
              <Keyboard className="w-7 h-7 text-white group-hover:text-black transition-colors" />
            </div>
            <div className="flex items-center justify-between mb-2">
              <h2 className="text-2xl font-bold text-white font-heading">No Camera</h2>
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-neutral-800 text-neutral-200 border border-white/15">
                Keyboard & Tap
              </span>
            </div>
            <p className="text-sm text-neutral-400 mb-6 leading-relaxed">
              Play using large tactile targets or keyboard shortcuts (R for Rock, P for Paper, S for Scissors).
            </p>
          </div>

          <div className="space-y-2.5 border-t border-white/10 pt-4 text-xs text-neutral-300">
            <div className="flex items-center gap-2">
              <Brain className="w-3.5 h-3.5 text-white" />
              <span>Full Order-1 & Order-2 Markov AI engine</span>
            </div>
            <div className="flex items-center gap-2">
              <ArrowRight className="w-3.5 h-3.5 text-white" />
              <span>Instant showdown & decision latency logs</span>
            </div>
          </div>
        </button>
      </div>
    </div>
  );
};
"""
write_file("apps/web/src/components/ModeSelector.tsx", modeselector_tsx)

# 4. apps/web/src/components/NoCameraGame.tsx
nocameragame_tsx = """import React, { useEffect } from 'react';
import { Move } from '@rps/core';
import { sounds } from '../sound';

interface NoCameraGameProps {
  onPlayMove: (move: Move) => void;
  disabled?: boolean;
}

interface MoveCardDef {
  move: Move;
  title: string;
  emoji: string;
  hotkey: string;
}

const MOVE_CARDS: MoveCardDef[] = [
  {
    move: 'rock',
    title: 'Rock',
    emoji: '✊',
    hotkey: 'R',
  },
  {
    move: 'paper',
    title: 'Paper',
    emoji: '✋',
    hotkey: 'P',
  },
  {
    move: 'scissors',
    title: 'Scissors',
    emoji: '✌️',
    hotkey: 'S',
  },
];

export const NoCameraGame: React.FC<NoCameraGameProps> = ({ onPlayMove, disabled = false }) => {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (disabled) return;
      const key = e.key.toLowerCase();
      if (key === 'r') {
        sounds.playTick(500);
        onPlayMove('rock');
      } else if (key === 'p') {
        sounds.playTick(600);
        onPlayMove('paper');
      } else if (key === 's') {
        sounds.playTick(700);
        onPlayMove('scissors');
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [disabled, onPlayMove]);

  const handleCardClick = (move: Move) => {
    if (disabled) return;
    sounds.playTick(550);
    onPlayMove(move);
  };

  return (
    <div className="w-full max-w-4xl mx-auto px-4 py-12 flex flex-col items-center">
      <div className="text-center mb-10">
        <h2 className="text-3xl sm:text-4xl font-bold text-white font-heading mb-2">
          Make Your Move
        </h2>
        <p className="text-sm text-neutral-400">
          Tap a card or press the corresponding shortcut key <span className="font-mono text-white font-bold">(R, P, S)</span>
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 w-full max-w-3xl">
        {MOVE_CARDS.map((card) => (
          <button
            key={card.move}
            onClick={() => handleCardClick(card.move)}
            disabled={disabled}
            className="group relative p-10 rounded-3xl bg-neutral-950/80 border border-white/10 hover:border-white/50 transition-all duration-200 flex flex-col items-center justify-center text-center shadow-xl hover:shadow-2xl hover:shadow-white/5 hover:-translate-y-1.5 active:scale-95 disabled:opacity-50 disabled:pointer-events-none"
          >
            {/* Hotkey Pill */}
            <span className="absolute top-4 right-4 px-2.5 py-1 rounded-lg bg-neutral-900 border border-white/15 text-xs font-mono font-bold text-neutral-300 group-hover:text-white group-hover:border-white/40 transition-colors">
              {card.hotkey}
            </span>

            {/* Emoji */}
            <span className="text-7xl mb-5 transform group-hover:scale-110 transition-transform duration-200 select-none">
              {card.emoji}
            </span>

            {/* Title */}
            <span className="text-2xl font-bold font-heading text-white mb-1">
              {card.title}
            </span>

            <span className="text-xs text-neutral-500 font-mono">
              [ {card.hotkey} ]
            </span>
          </button>
        ))}
      </div>
    </div>
  );
};
"""
write_file("apps/web/src/components/NoCameraGame.tsx", nocameragame_tsx)

# 5. apps/web/src/components/CameraGame.tsx
cameragame_tsx = """import React, { useEffect, useRef, useState, useCallback } from 'react';
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
"""
write_file("apps/web/src/components/CameraGame.tsx", cameragame_tsx)

# 6. apps/web/src/components/RevealArena.tsx
revealarena_tsx = """import React, { useEffect } from 'react';
import { Move, Outcome, ModelType } from '@rps/core';
import confetti from 'canvas-confetti';
import { Trophy, XCircle, MinusCircle, ArrowRight, Zap, Brain } from 'lucide-react';
import { sounds } from '../sound';

interface RevealArenaProps {
  playerMove: Move;
  botMove: Move;
  predictedMove: Move;
  modelUsed: ModelType;
  outcome: Outcome;
  latencyMs: number;
  onNextRound: () => void;
}

const MOVE_DATA: Record<Move, { emoji: string; name: string }> = {
  rock: { emoji: '✊', name: 'Rock' },
  paper: { emoji: '✋', name: 'Paper' },
  scissors: { emoji: '✌️', name: 'Scissors' },
};

export const RevealArena: React.FC<RevealArenaProps> = ({
  playerMove,
  botMove,
  predictedMove,
  modelUsed,
  outcome,
  latencyMs,
  onNextRound,
}) => {
  useEffect(() => {
    if (outcome === 'win') {
      sounds.playWin();
      confetti({
        particleCount: 70,
        spread: 65,
        origin: { y: 0.6 },
        colors: ['#ffffff', '#a1a1aa', '#71717a', '#d4d4d8'],
      });
    } else if (outcome === 'lose') {
      sounds.playLose();
    } else {
      sounds.playTie();
    }

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.code === 'Space' || e.code === 'Enter') {
        onNextRound();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [outcome, onNextRound]);

  const getOutcomeBanner = () => {
    switch (outcome) {
      case 'win':
        return {
          title: 'VICTORY',
          subtitle: 'You outsmarted the adaptive model this round',
          icon: <Trophy className="w-8 h-8 text-white" />,
          containerClass: 'border-white/30 bg-neutral-950/90 shadow-white/10',
        };
      case 'lose':
        return {
          title: 'DEFEAT',
          subtitle: 'The AI model anticipated your pattern',
          icon: <XCircle className="w-8 h-8 text-neutral-400" />,
          containerClass: 'border-white/15 bg-neutral-950/80',
        };
      case 'tie':
        return {
          title: 'DRAW',
          subtitle: 'Both chose the exact same move',
          icon: <MinusCircle className="w-8 h-8 text-neutral-300" />,
          containerClass: 'border-white/20 bg-neutral-950/80',
        };
    }
  };

  const banner = getOutcomeBanner();

  return (
    <div className="w-full max-w-4xl mx-auto px-4 py-8 flex flex-col items-center animate-pop-in">
      {/* Outcome Banner */}
      <div
        className={`w-full max-w-2xl p-7 rounded-3xl border backdrop-blur-xl text-center mb-8 shadow-2xl flex flex-col items-center ${banner.containerClass}`}
      >
        <div className="mb-2.5">{banner.icon}</div>
        <h2 className="text-3xl sm:text-5xl font-black font-heading text-white tracking-wider mb-1">
          {banner.title}
        </h2>
        <p className="text-sm text-neutral-400">{banner.subtitle}</p>
      </div>

      {/* Showdown Move Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-8 w-full max-w-2xl mb-8">
        {/* Player Card */}
        <div className="p-8 rounded-3xl bg-neutral-950/80 border border-white/15 flex flex-col items-center text-center shadow-xl">
          <span className="text-xs uppercase tracking-widest text-neutral-400 font-bold mb-4 font-mono">
            Your Move
          </span>
          <span className="text-7xl mb-4 select-none animate-float">
            {MOVE_DATA[playerMove].emoji}
          </span>
          <span className="text-2xl font-bold font-heading text-white">
            {MOVE_DATA[playerMove].name}
          </span>
        </div>

        {/* Bot Card */}
        <div className="p-8 rounded-3xl bg-neutral-950/80 border border-white/30 flex flex-col items-center text-center shadow-xl shadow-white/5">
          <span className="text-xs uppercase tracking-widest text-white font-bold mb-4 flex items-center gap-1 font-mono">
            <Brain className="w-3.5 h-3.5" /> Bot Move
          </span>
          <span className="text-7xl mb-4 select-none animate-float">
            {MOVE_DATA[botMove].emoji}
          </span>
          <span className="text-2xl font-bold font-heading text-white">
            {MOVE_DATA[botMove].name}
          </span>
        </div>
      </div>

      {/* AI Decision Breakdown Insight Card */}
      <div className="w-full max-w-2xl p-4.5 rounded-2xl bg-neutral-950/60 border border-white/10 mb-8 text-xs text-neutral-300 grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div className="flex items-center gap-2.5">
          <Zap className="w-4 h-4 text-white shrink-0" />
          <div>
            <span className="text-neutral-500 block">AI Predicted:</span>
            <span className="font-mono font-bold text-white uppercase">
              {predictedMove} {predictedMove === playerMove ? '✅ Hit' : '❌ Miss'}
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2.5">
          <Brain className="w-4 h-4 text-neutral-300 shrink-0" />
          <div>
            <span className="text-neutral-500 block">Active Model:</span>
            <span className="font-mono font-bold text-white uppercase">
              {modelUsed}
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2.5">
          <span className="font-mono text-white font-bold text-sm">⏱</span>
          <div>
            <span className="text-neutral-500 block">Latency:</span>
            <span className="font-mono font-bold text-white">
              {latencyMs.toFixed(3)} ms
            </span>
          </div>
        </div>
      </div>

      {/* Next Round Button */}
      <button
        onClick={onNextRound}
        className="px-10 py-4 rounded-2xl bg-white text-black hover:bg-neutral-200 font-bold text-lg font-heading shadow-xl shadow-white/10 hover:-translate-y-0.5 active:scale-95 transition-all flex items-center gap-2.5"
      >
        <span>Play Next Round</span>
        <ArrowRight className="w-5 h-5 text-black" />
      </button>
      <span className="text-xs text-neutral-500 mt-2.5 font-mono">Press Space or Enter</span>
    </div>
  );
};
"""
write_file("apps/web/src/components/RevealArena.tsx", revealarena_tsx)

# 7. apps/web/src/components/StatsView.tsx
statsview_tsx = """import React, { useState } from 'react';
import { RoundLog, SummaryStats } from '@rps/core';
import { Download, ArrowLeft, BarChart2, Brain } from 'lucide-react';

interface StatsViewProps {
  logs: readonly RoundLog[];
  stats: SummaryStats;
  onBack: () => void;
  onDownloadJSON: () => void;
  onDownloadCSV: () => void;
}

export const StatsView: React.FC<StatsViewProps> = ({
  logs,
  stats,
  onBack,
  onDownloadJSON,
  onDownloadCSV,
}) => {
  const [filter, setFilter] = useState<'all' | 'win' | 'lose' | 'tie'>('all');

  const filteredLogs = logs.filter((l) => (filter === 'all' ? true : l.result === filter));

  return (
    <div className="w-full max-w-6xl mx-auto px-4 py-8 animate-pop-in">
      {/* Top Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 mb-8">
        <button
          onClick={onBack}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-neutral-900 hover:bg-neutral-800 text-neutral-200 border border-white/10 text-sm font-medium transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Game</span>
        </button>

        <div className="flex items-center gap-2">
          <button
            onClick={onDownloadJSON}
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-neutral-900 hover:bg-neutral-800 text-white border border-white/20 text-xs font-semibold transition-colors"
          >
            <Download className="w-4 h-4" />
            <span>Export JSON</span>
          </button>
          <button
            onClick={onDownloadCSV}
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-white text-black hover:bg-neutral-200 text-xs font-bold transition-colors shadow-md shadow-white/10"
          >
            <Download className="w-4 h-4" />
            <span>Export CSV</span>
          </button>
        </div>
      </div>

      <div className="mb-8">
        <h2 className="text-3xl font-black font-heading text-white tracking-tight mb-2">
          Performance & Model Statistics
        </h2>
        <p className="text-sm text-neutral-400">
          In-depth diagnostics on Markov Order-1 and Order-2 prediction accuracy and win rates.
        </p>
      </div>

      {/* Summary KPI Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
        <div className="p-5 rounded-2xl bg-neutral-950/80 border border-white/10">
          <span className="text-xs text-neutral-400 block mb-1">Total Rounds</span>
          <span className="text-3xl font-bold font-mono text-white">{stats.totalRounds}</span>
        </div>

        <div className="p-5 rounded-2xl bg-neutral-950/80 border border-white/25">
          <span className="text-xs text-white block mb-1">Overall AI Accuracy</span>
          <span className="text-3xl font-bold font-mono text-white">
            {(stats.overallPredictionAccuracy * 100).toFixed(1)}%
          </span>
        </div>

        <div className="p-5 rounded-2xl bg-neutral-950/80 border border-white/15">
          <span className="text-xs text-neutral-300 block mb-1">Bot Win Rate</span>
          <span className="text-3xl font-bold font-mono text-white">
            {(stats.botWinRate * 100).toFixed(1)}%
          </span>
          <span className="text-[10px] text-neutral-500 block mt-1">vs 33.3% Baseline</span>
        </div>

        <div className="p-5 rounded-2xl bg-neutral-950/80 border border-white/10">
          <span className="text-xs text-neutral-400 block mb-1">Avg Latency</span>
          <span className="text-3xl font-bold font-mono text-white">
            {stats.averageLatencyMs.toFixed(3)} ms
          </span>
        </div>
      </div>

      {/* Model Breakdown Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="p-6 rounded-2xl bg-neutral-950/80 border border-white/10">
          <h3 className="text-base font-bold text-white font-heading mb-4 flex items-center gap-2">
            <Brain className="w-4 h-4 text-white" />
            Model Accuracy Metrics (Rolling Window)
          </h3>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-neutral-300">Markov Order-1 P(m_t | m_t-1)</span>
                <span className="font-mono text-white font-bold">
                  {(stats.modelStats.order1RollingAccuracy * 100).toFixed(1)}%
                </span>
              </div>
              <div className="w-full h-2 rounded-full bg-neutral-800 overflow-hidden">
                <div
                  className="h-full bg-white rounded-full"
                  style={{ width: `${Math.min(100, stats.modelStats.order1RollingAccuracy * 100)}%` }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-neutral-300">Markov Order-2 P(m_t | m_t-2, m_t-1)</span>
                <span className="font-mono text-white font-bold">
                  {(stats.modelStats.order2RollingAccuracy * 100).toFixed(1)}%
                </span>
              </div>
              <div className="w-full h-2 rounded-full bg-neutral-800 overflow-hidden">
                <div
                  className="h-full bg-neutral-300 rounded-full"
                  style={{ width: `${Math.min(100, stats.modelStats.order2RollingAccuracy * 100)}%` }}
                />
              </div>
            </div>
          </div>
        </div>

        <div className="p-6 rounded-2xl bg-neutral-950/80 border border-white/10">
          <h3 className="text-base font-bold text-white font-heading mb-4 flex items-center gap-2">
            <BarChart2 className="w-4 h-4 text-white" />
            Model Selection Usage Counts
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
            <div className="p-3 rounded-xl bg-black border border-white/10">
              <span className="text-[11px] text-neutral-400 block mb-1">Order-1</span>
              <span className="text-lg font-bold font-mono text-white">
                {stats.modelStats.modelUsageCounts['order-1'] || 0}
              </span>
            </div>
            <div className="p-3 rounded-xl bg-black border border-white/10">
              <span className="text-[11px] text-neutral-400 block mb-1">Order-2</span>
              <span className="text-lg font-bold font-mono text-white">
                {stats.modelStats.modelUsageCounts['order-2'] || 0}
              </span>
            </div>
            <div className="p-3 rounded-xl bg-black border border-white/10">
              <span className="text-[11px] text-neutral-400 block mb-1">Cold Start</span>
              <span className="text-lg font-bold font-mono text-neutral-300">
                {stats.modelStats.modelUsageCounts['cold-start'] || 0}
              </span>
            </div>
            <div className="p-3 rounded-xl bg-black border border-white/10">
              <span className="text-[11px] text-neutral-400 block mb-1">Random (ε)</span>
              <span className="text-lg font-bold font-mono text-neutral-400">
                {stats.modelStats.modelUsageCounts.random || 0}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Round-by-Round History Table */}
      <div className="p-6 rounded-2xl bg-neutral-950/80 border border-white/10">
        <div className="flex flex-wrap items-center justify-between gap-4 mb-4">
          <h3 className="text-lg font-bold text-white font-heading">
            Full Round History ({filteredLogs.length})
          </h3>

          <div className="flex items-center gap-1 bg-black p-1 rounded-xl border border-white/10 text-xs">
            {(['all', 'win', 'lose', 'tie'] as const).map((opt) => (
              <button
                key={opt}
                onClick={() => setFilter(opt)}
                className={`px-3 py-1 rounded-lg capitalize font-medium transition-colors ${
                  filter === opt ? 'bg-white text-black font-bold' : 'text-neutral-400 hover:text-white'
                }`}
              >
                {opt}
              </button>
            ))}
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-white/10 text-neutral-400 font-mono">
                <th className="py-3 px-3">#</th>
                <th className="py-3 px-3">Your Move</th>
                <th className="py-3 px-3">Predicted Move</th>
                <th className="py-3 px-3">Bot Move</th>
                <th className="py-3 px-3">Result</th>
                <th className="py-3 px-3">Model</th>
                <th className="py-3 px-3">Prediction</th>
                <th className="py-3 px-3">Latency</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5 font-mono">
              {filteredLogs.length === 0 ? (
                <tr>
                  <td colSpan={8} className="py-8 text-center text-neutral-500">
                    No rounds recorded yet.
                  </td>
                </tr>
              ) : (
                filteredLogs.slice().reverse().map((log) => (
                  <tr key={log.roundNumber} className="hover:bg-white/5 transition-colors">
                    <td className="py-2.5 px-3 text-neutral-500">{log.roundNumber}</td>
                    <td className="py-2.5 px-3 font-semibold text-white uppercase">{log.opponentMove}</td>
                    <td className="py-2.5 px-3 text-neutral-300 uppercase">{log.predictedMove}</td>
                    <td className="py-2.5 px-3 text-white uppercase">{log.botMove}</td>
                    <td className="py-2.5 px-3">
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                          log.result === 'win'
                            ? 'bg-white text-black'
                            : log.result === 'lose'
                            ? 'bg-neutral-800 text-neutral-300 border border-white/10'
                            : 'bg-neutral-900 text-neutral-400 border border-white/5'
                        }`}
                      >
                        {log.result}
                      </span>
                    </td>
                    <td className="py-2.5 px-3 text-neutral-400">{log.modelUsed}</td>
                    <td className="py-2.5 px-3">
                      {log.predictionCorrect ? (
                        <span className="text-white font-bold">Hit</span>
                      ) : (
                        <span className="text-neutral-600">Miss</span>
                      )}
                    </td>
                    <td className="py-2.5 px-3 text-neutral-400">{log.decisionLatencyMs.toFixed(2)}ms</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
"""
write_file("apps/web/src/components/StatsView.tsx", statsview_tsx)

# 8. apps/web/src/App.tsx
app_tsx = """import React, { useState, useRef } from 'react';
import {
  Move,
  Outcome,
  ModelType,
  createAdaptiveAI,
  chooseMove,
  updateModel,
  resolveOutcome,
  RoundLogger,
  AdaptiveAIState,
} from '@rps/core';
import { Header } from './components/Header';
import { ModeSelector } from './components/ModeSelector';
import { NoCameraGame } from './components/NoCameraGame';
import { CameraGame } from './components/CameraGame';
import { RevealArena } from './components/RevealArena';
import { StatsView } from './components/StatsView';

type AppView = 'mode-select' | 'play' | 'reveal' | 'stats';

export const App: React.FC = () => {
  const [mode, setMode] = useState<'camera' | 'nocamera'>('nocamera');
  const [view, setView] = useState<AppView>('mode-select');

  const [aiState, setAiState] = useState<AdaptiveAIState>(() =>
    createAdaptiveAI({ gamma: 0.94, epsilon: 0.08, coldStartRounds: 10 })
  );
  const loggerRef = useRef<RoundLogger>(new RoundLogger());
  const [history, setHistory] = useState<Move[]>([]);

  // Last round outcome details for Reveal Arena
  const [lastRoundDetails, setLastRoundDetails] = useState<{
    playerMove: Move;
    botMove: Move;
    predictedMove: Move;
    modelUsed: ModelType;
    outcome: Outcome;
    latencyMs: number;
  } | null>(null);

  const stats = loggerRef.current.getStats();

  const handleSelectMode = (selectedMode: 'camera' | 'nocamera') => {
    setMode(selectedMode);
    setView('play');
  };

  const handlePlayMove = (playerMove: Move) => {
    // 1. AI decides bot move based on opponent history
    const decision = chooseMove(aiState, history);

    // 2. Resolve outcome
    const outcome = resolveOutcome(playerMove, decision.botMove);
    const predictionCorrect = decision.predictedMove === playerMove;

    // 3. Record in RoundLogger
    loggerRef.current.recordRound({
      opponentMove: playerMove,
      predictedMove: decision.predictedMove,
      botMove: decision.botMove,
      result: outcome,
      modelUsed: decision.modelUsed,
      predictionCorrect,
      decisionLatencyMs: decision.decisionLatencyMs,
    });

    // 4. Update Markov AI model
    const newAiState = updateModel(
      aiState,
      playerMove,
      decision.predictedMove,
      decision.modelUsed,
      history
    );
    setAiState(newAiState);
    setHistory((prev) => [...prev, playerMove]);

    // 5. Store for Reveal Arena
    setLastRoundDetails({
      playerMove,
      botMove: decision.botMove,
      predictedMove: decision.predictedMove,
      modelUsed: decision.modelUsed,
      outcome,
      latencyMs: decision.decisionLatencyMs,
    });

    setView('reveal');
  };

  const handleNextRound = () => {
    setView('play');
  };

  const handleReset = () => {
    setAiState(createAdaptiveAI({ gamma: 0.94, epsilon: 0.08, coldStartRounds: 10 }));
    loggerRef.current.clear();
    setHistory([]);
    setLastRoundDetails(null);
    setView('mode-select');
  };

  const handleDownloadJSON = () => {
    const jsonStr = loggerRef.current.exportJSON();
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `rps_game_logs_${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleDownloadCSV = () => {
    const csvStr = loggerRef.current.exportCSV();
    const blob = new Blob([csvStr], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `rps_game_logs_${Date.now()}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen flex flex-col bg-black text-white selection:bg-white selection:text-black">
      {view !== 'mode-select' && (
        <Header
          mode={mode}
          stats={stats}
          onSwitchMode={() => setView('mode-select')}
          onOpenStats={() => setView('stats')}
          onReset={handleReset}
        />
      )}

      <main className="flex-1 flex flex-col justify-center">
        {view === 'mode-select' && <ModeSelector onSelectMode={handleSelectMode} />}

        {view === 'play' && mode === 'nocamera' && <NoCameraGame onPlayMove={handlePlayMove} />}

        {view === 'play' && mode === 'camera' && <CameraGame onPlayMove={handlePlayMove} />}

        {view === 'reveal' && lastRoundDetails && (
          <RevealArena
            playerMove={lastRoundDetails.playerMove}
            botMove={lastRoundDetails.botMove}
            predictedMove={lastRoundDetails.predictedMove}
            modelUsed={lastRoundDetails.modelUsed}
            outcome={lastRoundDetails.outcome}
            latencyMs={lastRoundDetails.latencyMs}
            onNextRound={handleNextRound}
          />
        )}

        {view === 'stats' && (
          <StatsView
            logs={loggerRef.current.getLogs()}
            stats={stats}
            onBack={() => setView('play')}
            onDownloadJSON={handleDownloadJSON}
            onDownloadCSV={handleDownloadCSV}
          />
        )}
      </main>

      <footer className="py-5 border-t border-white/10 text-center text-xs text-neutral-500 font-mono">
        Rock-Paper-Scissors Adaptive AI &copy; 2026 • Markov Order-1 & Order-2 Opponent Modeling
      </footer>
    </div>
  );
};

export default App;
"""
write_file("apps/web/src/App.tsx", app_tsx)

print("Monochrome premium theme applied!")
