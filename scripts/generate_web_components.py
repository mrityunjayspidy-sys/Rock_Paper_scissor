import os

def write_file(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

# 1. apps/web/src/components/Header.tsx
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
    <header className="w-full border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md sticky top-0 z-40 px-4 py-3">
      <div className="max-w-6xl mx-auto flex flex-wrap items-center justify-between gap-4">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-500 to-violet-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
              RPS Adaptive AI
              <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
                Markov v2
              </span>
            </h1>
            <p className="text-xs text-slate-400">Order-1 & Order-2 Opponent Modeling</p>
          </div>
        </div>

        {/* Live HUD Quick Stats */}
        <div className="flex items-center gap-3 bg-slate-900/90 px-4 py-1.5 rounded-xl border border-slate-800 text-xs">
          <div className="flex items-center gap-1.5">
            <span className="text-slate-400">Rounds:</span>
            <span className="font-mono font-semibold text-white">{stats.totalRounds}</span>
          </div>
          <span className="text-slate-700">|</span>
          <div className="flex items-center gap-1.5">
            <span className="text-emerald-400">You:</span>
            <span className="font-mono font-semibold text-emerald-300">
              {stats.humanWins} ({(stats.humanWinRate * 100).toFixed(0)}%)
            </span>
          </div>
          <span className="text-slate-700">|</span>
          <div className="flex items-center gap-1.5">
            <span className="text-rose-400">Bot:</span>
            <span className="font-mono font-semibold text-rose-300">
              {stats.botWins} ({(stats.botWinRate * 100).toFixed(0)}%)
            </span>
          </div>
          <span className="text-slate-700">|</span>
          <div className="flex items-center gap-1.5">
            <span className="text-amber-400">Ties:</span>
            <span className="font-mono font-semibold text-amber-300">{stats.ties}</span>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2">
          <button
            onClick={onSwitchMode}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700/60 transition-colors"
            title="Switch input mode"
          >
            {mode === 'camera' ? (
              <>
                <Video className="w-3.5 h-3.5 text-cyan-400" />
                <span>Camera</span>
              </>
            ) : (
              <>
                <Keyboard className="w-3.5 h-3.5 text-violet-400" />
                <span>No Camera</span>
              </>
            )}
          </button>

          <button
            onClick={onOpenStats}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-cyan-600/10 hover:bg-cyan-600/20 text-cyan-400 border border-cyan-500/30 transition-colors"
          >
            <BarChart3 className="w-3.5 h-3.5" />
            <span>Stats & Export</span>
          </button>

          <button
            onClick={onReset}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
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

# 2. apps/web/src/components/ModeSelector.tsx
modeselector_tsx = """import React from 'react';
import { Camera, Keyboard, Sparkles, Brain, Cpu, ShieldCheck } from 'lucide-react';

interface ModeSelectorProps {
  onSelectMode: (mode: 'camera' | 'nocamera') => void;
}

export const ModeSelector: React.FC<ModeSelectorProps> = ({ onSelectMode }) => {
  return (
    <div className="max-w-4xl mx-auto px-4 py-12 flex flex-col items-center justify-center min-h-[80vh] text-center">
      {/* Title Badge */}
      <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-gradient-to-r from-cyan-500/10 to-violet-500/10 border border-cyan-500/20 text-cyan-400 text-xs font-mono font-medium mb-6">
        <Sparkles className="w-3.5 h-3.5" />
        Opponent-Modeling Adaptive Markov AI
      </div>

      <h1 className="text-4xl sm:text-5xl font-black text-white tracking-tight mb-4 font-heading">
        Beat the <span className="bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 via-teal-300 to-violet-400">Adaptive AI</span>
      </h1>
      <p className="text-base sm:text-lg text-slate-400 max-w-2xl mb-12">
        The bot analyzes your past move patterns using Order-1 & Order-2 Markov frequency tables with exponential decay (γ=0.94) to predict and counter your next move. Choose your play mode:
      </p>

      {/* Mode Selection Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-3xl">
        {/* Camera Mode */}
        <button
          onClick={() => onSelectMode('camera')}
          className="group relative p-8 rounded-2xl bg-gradient-to-b from-slate-900/90 to-slate-950/90 border border-cyan-500/20 hover:border-cyan-400/60 transition-all duration-300 text-left hover:shadow-2xl hover:shadow-cyan-500/10 hover:-translate-y-1 flex flex-col justify-between"
        >
          <div className="absolute top-0 right-0 w-32 h-32 bg-cyan-500/5 rounded-full blur-2xl group-hover:bg-cyan-500/10 transition-colors pointer-events-none" />
          <div>
            <div className="w-14 h-14 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center mb-6 group-hover:scale-110 group-hover:bg-cyan-500/20 transition-all">
              <Camera className="w-7 h-7 text-cyan-400" />
            </div>
            <div className="flex items-center gap-2 mb-2">
              <h2 className="text-2xl font-bold text-white font-heading">Camera Mode</h2>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-cyan-500/20 text-cyan-300 border border-cyan-500/40">
                AI Vision
              </span>
            </div>
            <p className="text-sm text-slate-400 mb-6">
              Play using live hand gestures detected via MediaPipe HandLandmarker. Geometric finger-curl classifier triggers at 3-2-1 shoot.
            </p>
          </div>

          <div className="space-y-2 border-t border-slate-800/80 pt-4 text-xs text-slate-300">
            <div className="flex items-center gap-2">
              <Cpu className="w-3.5 h-3.5 text-cyan-400" />
              <span>Real-time 21-point hand landmark tracking</span>
            </div>
            <div className="flex items-center gap-2">
              <ShieldCheck className="w-3.5 h-3.5 text-cyan-400" />
              <span>100% Client-side, no video transmitted</span>
            </div>
          </div>
        </button>

        {/* No Camera Mode */}
        <button
          onClick={() => onSelectMode('nocamera')}
          className="group relative p-8 rounded-2xl bg-gradient-to-b from-slate-900/90 to-slate-950/90 border border-violet-500/20 hover:border-violet-400/60 transition-all duration-300 text-left hover:shadow-2xl hover:shadow-violet-500/10 hover:-translate-y-1 flex flex-col justify-between"
        >
          <div className="absolute top-0 right-0 w-32 h-32 bg-violet-500/5 rounded-full blur-2xl group-hover:bg-violet-500/10 transition-colors pointer-events-none" />
          <div>
            <div className="w-14 h-14 rounded-2xl bg-violet-500/10 border border-violet-500/30 flex items-center justify-center mb-6 group-hover:scale-110 group-hover:bg-violet-500/20 transition-all">
              <Keyboard className="w-7 h-7 text-violet-400" />
            </div>
            <div className="flex items-center gap-2 mb-2">
              <h2 className="text-2xl font-bold text-white font-heading">No Camera</h2>
              <span className="px-2 py-0.5 rounded text-[10px] font-mono font-semibold bg-violet-500/20 text-violet-300 border border-violet-500/40">
                Tap & Hotkeys
              </span>
            </div>
            <p className="text-sm text-slate-400 mb-6">
              Instant play using tactile on-screen tap targets or keyboard shortcuts (R for Rock, P for Paper, S for Scissors).
            </p>
          </div>

          <div className="space-y-2 border-t border-slate-800/80 pt-4 text-xs text-slate-300">
            <div className="flex items-center gap-2">
              <Brain className="w-3.5 h-3.5 text-violet-400" />
              <span>Full Order-1 & Order-2 Markov AI engine</span>
            </div>
            <div className="flex items-center gap-2">
              <Sparkles className="w-3.5 h-3.5 text-violet-400" />
              <span>Rapid testing & instant showdown</span>
            </div>
          </div>
        </button>
      </div>
    </div>
  );
};
"""
write_file("apps/web/src/components/ModeSelector.tsx", modeselector_tsx)

# 3. apps/web/src/components/NoCameraGame.tsx
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
  accentClass: string;
  borderClass: string;
  glowClass: string;
}

const MOVE_CARDS: MoveCardDef[] = [
  {
    move: 'rock',
    title: 'Rock',
    emoji: '✊',
    hotkey: 'R',
    accentClass: 'text-cyan-400',
    borderClass: 'hover:border-cyan-500/60',
    glowClass: 'hover:shadow-cyan-500/20',
  },
  {
    move: 'paper',
    title: 'Paper',
    emoji: '✋',
    hotkey: 'P',
    accentClass: 'text-violet-400',
    borderClass: 'hover:border-violet-500/60',
    glowClass: 'hover:shadow-violet-500/20',
  },
  {
    move: 'scissors',
    title: 'Scissors',
    emoji: '✌️',
    hotkey: 'S',
    accentClass: 'text-emerald-400',
    borderClass: 'hover:border-emerald-500/60',
    glowClass: 'hover:shadow-emerald-500/20',
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
    <div className="w-full max-w-4xl mx-auto px-4 py-8 flex flex-col items-center">
      <div className="text-center mb-8">
        <h2 className="text-2xl sm:text-3xl font-bold text-white font-heading mb-2">
          Make Your Move
        </h2>
        <p className="text-sm text-slate-400">
          Tap a card or press the corresponding keyboard shortcut <span className="font-mono text-cyan-400 font-semibold">(R, P, S)</span>
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 w-full max-w-3xl">
        {MOVE_CARDS.map((card) => (
          <button
            key={card.move}
            onClick={() => handleCardClick(card.move)}
            disabled={disabled}
            className={`group relative p-8 rounded-2xl bg-slate-900/80 border border-slate-800 ${card.borderClass} ${card.glowClass} transition-all duration-200 flex flex-col items-center justify-center text-center shadow-lg hover:shadow-2xl hover:-translate-y-1.5 active:scale-95 disabled:opacity-50 disabled:pointer-events-none`}
          >
            {/* Hotkey Pill */}
            <span className="absolute top-3.5 right-3.5 px-2 py-0.5 rounded-md bg-slate-800/80 border border-slate-700 text-[11px] font-mono font-bold text-slate-400 group-hover:text-white group-hover:border-slate-600 transition-colors">
              {card.hotkey}
            </span>

            {/* Emoji */}
            <span className="text-6xl mb-4 transform group-hover:scale-115 transition-transform duration-200 select-none">
              {card.emoji}
            </span>

            {/* Title */}
            <span className={`text-xl font-bold font-heading ${card.accentClass}`}>
              {card.title}
            </span>

            <span className="text-xs text-slate-500 mt-1">
              Press {card.hotkey}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
};
"""
write_file("apps/web/src/components/NoCameraGame.tsx", nocameragame_tsx)

# 4. apps/web/src/components/CameraGame.tsx
cameragame_tsx = """import React, { useEffect, useRef, useState } from 'react';
import { FilesetResolver, HandLandmarker } from '@mediapipe/tasks-vision';
import { Move, HandClassificationResult, classifyHandGesture } from '@rps/core';
import { Camera, RefreshCw, AlertCircle, Sparkles } from 'lucide-react';
import { sounds } from '../sound';

interface CameraGameProps {
  onPlayMove: (move: Move) => void;
  disabled?: boolean;
}

export const CameraGame: React.FC<CameraGameProps> = ({ onPlayMove, disabled = false }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const landmarkerRef = useRef<HandLandmarker | null>(null);

  const [cameraLoading, setCameraLoading] = useState(true);
  const [cameraError, setCameraError] = useState<string | null>(null);
  const [modelLoading, setModelLoading] = useState(true);

  const [currentGesture, setCurrentGesture] = useState<HandClassificationResult | null>(null);
  const [countdown, setCountdown] = useState<number | null>(null);
  const [repositionWarning, setRepositionWarning] = useState<string | null>(null);

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
          setCameraError('Failed to initialize Vision AI model. Please check network connection or use No Camera mode.');
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

  // Real-time Landmark Detection Loop
  useEffect(() => {
    let animId: number;

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
            setCurrentGesture(classification);

            // Draw Hand Skeleton
            ctx.save();
            ctx.strokeStyle = classification.move ? '#06b6d4' : '#94a3b8';
            ctx.lineWidth = 3;
            ctx.fillStyle = '#38bdf8';

            for (const lm of landmarks) {
              const x = lm.x * canvas.width;
              const y = lm.y * canvas.height;
              ctx.beginPath();
              ctx.arc(x, y, 4, 0, 2 * Math.PI);
              ctx.fill();
            }
            ctx.restore();
          } else {
            setCurrentGesture(null);
          }
        }
      }
      animId = requestAnimationFrame(renderLoop);
    };

    animId = requestAnimationFrame(renderLoop);
    return () => cancelAnimationFrame(animId);
  }, []);

  // Handle 3-2-1 Shoot Countdown
  const startShootCountdown = () => {
    if (disabled || countdown !== null) return;
    setRepositionWarning(null);
    setCountdown(3);
    sounds.playTick(440);

    const timer3 = setTimeout(() => {
      setCountdown(2);
      sounds.playTick(550);
    }, 1000);

    const timer2 = setTimeout(() => {
      setCountdown(1);
      sounds.playTick(660);
    }, 2000);

    const timer1 = setTimeout(() => {
      setCountdown(0); // Shoot!
      sounds.playShoot();

      // Snapshot gesture at Shoot!
      setTimeout(() => {
        if (currentGesture && currentGesture.move && currentGesture.confidence > 0.6) {
          onPlayMove(currentGesture.move);
        } else {
          setRepositionWarning(
            currentGesture?.reason || 'Hand not recognized clearly. Please position your hand in the center of the frame.'
          );
        }
        setCountdown(null);
      }, 400);
    }, 3000);

    return () => {
      clearTimeout(timer3);
      clearTimeout(timer2);
      clearTimeout(timer1);
    };
  };

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
      {/* Real-time Video Canvas Container */}
      <div className="relative w-full max-w-2xl aspect-[4/3] bg-slate-900 rounded-3xl overflow-hidden border-2 border-slate-800 shadow-2xl flex items-center justify-center">
        {cameraError ? (
          <div className="p-8 text-center max-w-md">
            <AlertCircle className="w-12 h-12 text-rose-400 mx-auto mb-4" />
            <p className="text-rose-200 text-sm font-medium mb-4">{cameraError}</p>
          </div>
        ) : cameraLoading || modelLoading ? (
          <div className="flex flex-col items-center gap-3 text-cyan-400">
            <RefreshCw className="w-8 h-8 animate-spin" />
            <span className="text-sm font-medium">
              {modelLoading ? 'Loading MediaPipe Tasks Vision AI...' : 'Accessing Camera Stream...'}
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

        {/* Live Detected Gesture Preview HUD */}
        {!cameraLoading && !modelLoading && !cameraError && (
          <div className="absolute top-4 left-4 right-4 flex items-center justify-between pointer-events-none">
            <div className="bg-slate-950/85 backdrop-blur-md px-3.5 py-1.5 rounded-xl border border-slate-700/60 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
              <span className="text-xs text-slate-300 font-medium">Live Pose:</span>
              <span className="text-xs font-bold text-white font-mono">
                {getMoveEmoji(currentGesture?.move || null)}
              </span>
              {currentGesture?.confidence ? (
                <span className="text-[10px] text-cyan-400 font-mono">
                  ({(currentGesture.confidence * 100).toFixed(0)}%)
                </span>
              ) : null}
            </div>
          </div>
        )}

        {/* 3-2-1 Shoot Overlay */}
        {countdown !== null && (
          <div className="absolute inset-0 bg-slate-950/70 backdrop-blur-sm flex flex-col items-center justify-center animate-pop-in pointer-events-none z-30">
            <span className="text-8xl sm:text-9xl font-black font-heading text-cyan-400 animate-pulse">
              {countdown === 0 ? 'SHOOT!' : countdown}
            </span>
            <span className="text-sm text-slate-300 mt-2 font-medium tracking-wide">
              {countdown === 0 ? 'Capturing Gesture...' : 'Get Ready!'}
            </span>
          </div>
        )}
      </div>

      {/* Reposition Warning Notification */}
      {repositionWarning && (
        <div className="mt-4 p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 flex items-center gap-3 text-rose-300 text-xs sm:text-sm max-w-xl animate-pop-in">
          <AlertCircle className="w-5 h-5 text-rose-400 shrink-0" />
          <div className="flex-1">
            <span className="font-semibold block text-white">Pose Not Recognized</span>
            <span>{repositionWarning}</span>
          </div>
          <button
            onClick={() => setRepositionWarning(null)}
            className="text-rose-400 hover:text-white font-bold text-xs"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Action Controls */}
      <div className="mt-6 flex flex-col items-center gap-3">
        <button
          onClick={startShootCountdown}
          disabled={disabled || countdown !== null || cameraLoading || modelLoading}
          className="px-8 py-4 rounded-2xl bg-gradient-to-r from-cyan-500 to-teal-500 hover:from-cyan-400 hover:to-teal-400 text-slate-950 font-bold text-lg font-heading shadow-xl shadow-cyan-500/25 hover:shadow-cyan-500/40 hover:-translate-y-0.5 active:scale-95 transition-all disabled:opacity-50 disabled:pointer-events-none flex items-center gap-2"
        >
          <Sparkles className="w-5 h-5 text-slate-950" />
          <span>Start 3-2-1 Shoot Countdown</span>
        </button>
        <span className="text-xs text-slate-500">
          Form Rock ✊, Paper ✋, or Scissors ✌️ in camera view at "SHOOT!"
        </span>
      </div>
    </div>
  );
};
"""
write_file("apps/web/src/components/CameraGame.tsx", cameragame_tsx)

# 5. apps/web/src/components/RevealArena.tsx
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
        particleCount: 80,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#06b6d4', '#10b981', '#f59e0b', '#8b5cf6'],
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
          title: 'VICTORY!',
          subtitle: 'You outsmarted the AI model this round',
          icon: <Trophy className="w-8 h-8 text-emerald-400" />,
          badgeClass: 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30',
          containerClass: 'shadow-emerald-500/10 border-emerald-500/40',
        };
      case 'lose':
        return {
          title: 'DEFEAT!',
          subtitle: 'The AI accurately anticipated your move',
          icon: <XCircle className="w-8 h-8 text-rose-400" />,
          badgeClass: 'bg-rose-500/10 text-rose-300 border-rose-500/30',
          containerClass: 'shadow-rose-500/10 border-rose-500/40',
        };
      case 'tie':
        return {
          title: 'DRAW!',
          subtitle: 'Both chose the exact same move',
          icon: <MinusCircle className="w-8 h-8 text-amber-400" />,
          badgeClass: 'bg-amber-500/10 text-amber-300 border-amber-500/30',
          containerClass: 'shadow-amber-500/10 border-amber-500/40',
        };
    }
  };

  const banner = getOutcomeBanner();

  return (
    <div className="w-full max-w-4xl mx-auto px-4 py-8 flex flex-col items-center animate-pop-in">
      {/* Outcome Banner */}
      <div
        className={`w-full max-w-2xl p-6 rounded-3xl bg-slate-900/90 border backdrop-blur-md text-center mb-8 shadow-2xl flex flex-col items-center ${banner.containerClass}`}
      >
        <div className="mb-2">{banner.icon}</div>
        <h2 className="text-3xl sm:text-4xl font-black font-heading text-white tracking-tight mb-1">
          {banner.title}
        </h2>
        <p className="text-sm text-slate-400">{banner.subtitle}</p>
      </div>

      {/* Showdown Move Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-8 w-full max-w-2xl mb-8">
        {/* Player Card */}
        <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800 flex flex-col items-center text-center shadow-lg">
          <span className="text-xs uppercase tracking-widest text-slate-400 font-bold mb-4">
            Your Move
          </span>
          <span className="text-7xl mb-4 select-none animate-float">
            {MOVE_DATA[playerMove].emoji}
          </span>
          <span className="text-xl font-bold font-heading text-white">
            {MOVE_DATA[playerMove].name}
          </span>
        </div>

        {/* Bot Card */}
        <div className="p-6 rounded-2xl bg-slate-900/70 border border-cyan-500/30 flex flex-col items-center text-center shadow-lg shadow-cyan-500/5">
          <span className="text-xs uppercase tracking-widest text-cyan-400 font-bold mb-4 flex items-center gap-1">
            <Brain className="w-3.5 h-3.5" /> Bot Move
          </span>
          <span className="text-7xl mb-4 select-none animate-float">
            {MOVE_DATA[botMove].emoji}
          </span>
          <span className="text-xl font-bold font-heading text-cyan-300">
            {MOVE_DATA[botMove].name}
          </span>
        </div>
      </div>

      {/* AI Decision Breakdown Insight Card */}
      <div className="w-full max-w-2xl p-4 rounded-2xl bg-slate-900/50 border border-slate-800 mb-8 text-xs text-slate-300 grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div className="flex items-center gap-2">
          <Zap className="w-4 h-4 text-cyan-400 shrink-0" />
          <div>
            <span className="text-slate-500 block">AI Predicted:</span>
            <span className="font-mono font-bold text-white uppercase">
              {predictedMove} {predictedMove === playerMove ? '✅ Hit' : '❌ Miss'}
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Brain className="w-4 h-4 text-violet-400 shrink-0" />
          <div>
            <span className="text-slate-500 block">Active Model:</span>
            <span className="font-mono font-bold text-violet-300 uppercase">
              {modelUsed}
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="font-mono text-cyan-400 font-bold text-sm">⏱</span>
          <div>
            <span className="text-slate-500 block">Latency:</span>
            <span className="font-mono font-bold text-cyan-300">
              {latencyMs.toFixed(3)} ms
            </span>
          </div>
        </div>
      </div>

      {/* Next Round Button */}
      <button
        onClick={onNextRound}
        className="px-8 py-4 rounded-2xl bg-gradient-to-r from-cyan-500 to-violet-600 hover:from-cyan-400 hover:to-violet-500 text-white font-bold text-lg font-heading shadow-xl shadow-cyan-500/25 hover:shadow-cyan-500/40 hover:-translate-y-0.5 active:scale-95 transition-all flex items-center gap-2"
      >
        <span>Play Next Round</span>
        <ArrowRight className="w-5 h-5" />
      </button>
      <span className="text-xs text-slate-500 mt-2">Press Space or Enter to continue</span>
    </div>
  );
};
"""
write_file("apps/web/src/components/RevealArena.tsx", revealarena_tsx)

# 6. apps/web/src/components/StatsView.tsx
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
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 text-sm font-medium transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Game</span>
        </button>

        <div className="flex items-center gap-2">
          <button
            onClick={onDownloadJSON}
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-cyan-600/10 hover:bg-cyan-600/20 text-cyan-400 border border-cyan-500/30 text-xs font-semibold transition-colors"
          >
            <Download className="w-4 h-4" />
            <span>Export JSON</span>
          </button>
          <button
            onClick={onDownloadCSV}
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-violet-600/10 hover:bg-violet-600/20 text-violet-400 border border-violet-500/30 text-xs font-semibold transition-colors"
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
        <p className="text-sm text-slate-400">
          In-depth diagnostics on Markov Order-1 and Order-2 prediction accuracy and win rates.
        </p>
      </div>

      {/* Summary KPI Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
        <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800">
          <span className="text-xs text-slate-400 block mb-1">Total Rounds</span>
          <span className="text-3xl font-bold font-mono text-white">{stats.totalRounds}</span>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/80 border border-cyan-500/30">
          <span className="text-xs text-cyan-400 block mb-1">Overall AI Accuracy</span>
          <span className="text-3xl font-bold font-mono text-cyan-300">
            {(stats.overallPredictionAccuracy * 100).toFixed(1)}%
          </span>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/80 border border-rose-500/30">
          <span className="text-xs text-rose-400 block mb-1">Bot Win Rate</span>
          <span className="text-3xl font-bold font-mono text-rose-300">
            {(stats.botWinRate * 100).toFixed(1)}%
          </span>
          <span className="text-[10px] text-slate-500 block mt-1">vs 33.3% Baseline</span>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800">
          <span className="text-xs text-slate-400 block mb-1">Avg Latency</span>
          <span className="text-3xl font-bold font-mono text-slate-200">
            {stats.averageLatencyMs.toFixed(3)} ms
          </span>
        </div>
      </div>

      {/* Model Breakdown Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800">
          <h3 className="text-base font-bold text-white font-heading mb-4 flex items-center gap-2">
            <Brain className="w-4 h-4 text-cyan-400" />
            Model Accuracy Metrics (Rolling Window)
          </h3>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-slate-300">Markov Order-1 P(m_t | m_t-1)</span>
                <span className="font-mono text-cyan-400 font-bold">
                  {(stats.modelStats.order1RollingAccuracy * 100).toFixed(1)}%
                </span>
              </div>
              <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-cyan-500 to-teal-400 rounded-full"
                  style={{ width: `${Math.min(100, stats.modelStats.order1RollingAccuracy * 100)}%` }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-slate-300">Markov Order-2 P(m_t | m_t-2, m_t-1)</span>
                <span className="font-mono text-violet-400 font-bold">
                  {(stats.modelStats.order2RollingAccuracy * 100).toFixed(1)}%
                </span>
              </div>
              <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-violet-500 to-fuchsia-400 rounded-full"
                  style={{ width: `${Math.min(100, stats.modelStats.order2RollingAccuracy * 100)}%` }}
                />
              </div>
            </div>
          </div>
        </div>

        <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800">
          <h3 className="text-base font-bold text-white font-heading mb-4 flex items-center gap-2">
            <BarChart2 className="w-4 h-4 text-violet-400" />
            Model Selection Usage Counts
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
            <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
              <span className="text-[11px] text-slate-400 block mb-1">Order-1</span>
              <span className="text-lg font-bold font-mono text-cyan-400">
                {stats.modelStats.modelUsageCounts['order-1'] || 0}
              </span>
            </div>
            <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
              <span className="text-[11px] text-slate-400 block mb-1">Order-2</span>
              <span className="text-lg font-bold font-mono text-violet-400">
                {stats.modelStats.modelUsageCounts['order-2'] || 0}
              </span>
            </div>
            <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
              <span className="text-[11px] text-slate-400 block mb-1">Cold Start</span>
              <span className="text-lg font-bold font-mono text-amber-400">
                {stats.modelStats.modelUsageCounts['cold-start'] || 0}
              </span>
            </div>
            <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
              <span className="text-[11px] text-slate-400 block mb-1">Random (ε)</span>
              <span className="text-lg font-bold font-mono text-emerald-400">
                {stats.modelStats.modelUsageCounts.random || 0}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Round-by-Round History Table */}
      <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800">
        <div className="flex flex-wrap items-center justify-between gap-4 mb-4">
          <h3 className="text-lg font-bold text-white font-heading">
            Full Round History ({filteredLogs.length})
          </h3>

          <div className="flex items-center gap-1.5 bg-slate-950 p-1 rounded-xl border border-slate-800 text-xs">
            {(['all', 'win', 'lose', 'tie'] as const).map((opt) => (
              <button
                key={opt}
                onClick={() => setFilter(opt)}
                className={`px-3 py-1 rounded-lg capitalize font-medium transition-colors ${
                  filter === opt ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40' : 'text-slate-400 hover:text-slate-200'
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
              <tr className="border-b border-slate-800 text-slate-400 font-mono">
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
            <tbody className="divide-y divide-slate-800/60 font-mono">
              {filteredLogs.length === 0 ? (
                <tr>
                  <td colSpan={8} className="py-8 text-center text-slate-500">
                    No rounds recorded yet.
                  </td>
                </tr>
              ) : (
                filteredLogs.slice().reverse().map((log) => (
                  <tr key={log.roundNumber} className="hover:bg-slate-800/30 transition-colors">
                    <td className="py-2.5 px-3 text-slate-500">{log.roundNumber}</td>
                    <td className="py-2.5 px-3 font-semibold text-white uppercase">{log.opponentMove}</td>
                    <td className="py-2.5 px-3 text-cyan-300 uppercase">{log.predictedMove}</td>
                    <td className="py-2.5 px-3 text-violet-300 uppercase">{log.botMove}</td>
                    <td className="py-2.5 px-3">
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                          log.result === 'win'
                            ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                            : log.result === 'lose'
                            ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                            : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                        }`}
                      >
                        {log.result}
                      </span>
                    </td>
                    <td className="py-2.5 px-3 text-slate-400">{log.modelUsed}</td>
                    <td className="py-2.5 px-3">
                      {log.predictionCorrect ? (
                        <span className="text-emerald-400 font-bold">Hit</span>
                      ) : (
                        <span className="text-slate-500">Miss</span>
                      )}
                    </td>
                    <td className="py-2.5 px-3 text-slate-400">{log.decisionLatencyMs.toFixed(2)}ms</td>
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

# 7. apps/web/src/App.tsx
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
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100 selection:bg-cyan-500 selection:text-black">
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

      <footer className="py-4 border-t border-slate-900 text-center text-xs text-slate-500">
        Rock-Paper-Scissors Adaptive AI Engine &copy; 2026 • Markov Order-1 & Order-2 Opponent Modeling
      </footer>
    </div>
  );
};

export default App;
"""
write_file("apps/web/src/App.tsx", app_tsx)

print("Web application React components scaffolded successfully!")
