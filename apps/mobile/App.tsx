import React, { useState, useRef } from 'react';
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  Share,
  Platform,
  Alert,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import {
  Move,
  Outcome,
  ModelType,
  Difficulty,
  DIFFICULTY_CONFIGS,
  createAdaptiveAI,
  chooseMove,
  updateModel,
  resolveOutcome,
  RoundLogger,
  AdaptiveAIState,
} from '@rps/core';

export default function App() {
  const [mode, setMode] = useState<'nocamera' | 'camera'>('nocamera');
  const [difficulty, setDifficulty] = useState<Difficulty>('normal');
  const [view, setView] = useState<'mode-select' | 'play' | 'reveal' | 'stats'>('mode-select');

  const [aiState, setAiState] = useState<AdaptiveAIState>(() =>
    createAdaptiveAI('normal')
  );
  const loggerRef = useRef<RoundLogger>(new RoundLogger());
  const [history, setHistory] = useState<Move[]>([]);

  const [lastRound, setLastRound] = useState<{
    playerMove: Move;
    botMove: Move;
    predictedMove: Move;
    modelUsed: ModelType;
    outcome: Outcome;
    latencyMs: number;
  } | null>(null);

  const stats = loggerRef.current.getStats();

  const handleSelectDifficulty = (d: Difficulty) => {
    setDifficulty(d);
    setAiState((prev) => ({
      ...prev,
      config: { ...DIFFICULTY_CONFIGS[d] },
    }));
  };

  const handlePlayMove = (playerMove: Move) => {
    const decision = chooseMove(aiState, history);
    const outcome = resolveOutcome(playerMove, decision.botMove);
    const predictionCorrect = decision.predictedMove === playerMove;

    loggerRef.current.recordRound({
      opponentMove: playerMove,
      predictedMove: decision.predictedMove,
      botMove: decision.botMove,
      result: outcome,
      modelUsed: decision.modelUsed,
      predictionCorrect,
      decisionLatencyMs: decision.decisionLatencyMs,
    });

    const newAiState = updateModel(
      aiState,
      playerMove,
      decision.predictedMove,
      decision.modelUsed,
      history
    );
    setAiState(newAiState);
    setHistory((prev) => [...prev, playerMove]);

    setLastRound({
      playerMove,
      botMove: decision.botMove,
      predictedMove: decision.predictedMove,
      modelUsed: decision.modelUsed,
      outcome,
      latencyMs: decision.decisionLatencyMs,
    });

    setView('reveal');
  };

  const handleReset = () => {
    setAiState(createAdaptiveAI(difficulty));
    loggerRef.current.clear();
    setHistory([]);
    setLastRound(null);
    setView('mode-select');
  };

  const handleExportJSON = async () => {
    try {
      const jsonStr = loggerRef.current.exportJSON();
      if (Platform.OS === 'web') {
        const blob = new Blob([jsonStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `rps_mobile_logs_${Date.now()}.json`;
        a.click();
      } else {
        await Share.share({
          title: 'Rock-Paper-Scissors Game Logs',
          message: jsonStr,
        });
      }
    } catch {
      Alert.alert('Export Error', 'Could not export logs.');
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="light" />

      {/* Header */}
      <View style={styles.header}>
        <View>
          <Text style={styles.headerTitle}>RPS Adaptive AI</Text>
          <Text style={styles.headerSubtitle}>AI: {difficulty.toUpperCase()}</Text>
        </View>
        <View style={styles.statsBadge}>
          <Text style={styles.statsBadgeText}>
            You: {stats.humanWins} | Bot: {stats.botWins}
          </Text>
        </View>
      </View>

      {/* Difficulty Level Switcher */}
      <View style={styles.difficultyRow}>
        {(['easy', 'normal', 'hard'] as const).map((lvl) => (
          <TouchableOpacity
            key={lvl}
            style={[
              styles.diffBtn,
              difficulty === lvl && styles.diffBtnActive,
            ]}
            onPress={() => handleSelectDifficulty(lvl)}
          >
            <Text
              style={[
                styles.diffBtnText,
                difficulty === lvl && styles.diffBtnTextActive,
              ]}
            >
              {lvl.toUpperCase()}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* View: Mode Selection */}
      {view === 'mode-select' && (
        <View style={styles.centerContainer}>
          <Text style={styles.heroTitle}>Adaptive Markov AI</Text>
          <Text style={styles.heroSubtitle}>
            Order-1 & Order-2 frequency tracking with exponential decay
          </Text>

          <TouchableOpacity
            style={[styles.card, styles.cyanCard]}
            onPress={() => {
              setMode('nocamera');
              setView('play');
            }}
          >
            <Text style={styles.cardTitle}>No Camera Mode</Text>
            <Text style={styles.cardDesc}>Large tactile buttons for Rock, Paper, Scissors</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.card, styles.violetCard]}
            onPress={() => {
              setMode('camera');
              setView('play');
            }}
          >
            <Text style={styles.cardTitle}>Vision AI Gesture Mode</Text>
            <Text style={styles.cardDesc}>Instant gesture recognition & auto shoot</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.actionBtn, styles.statsBtn]}
            onPress={() => setView('stats')}
          >
            <Text style={styles.actionBtnText}>View Statistics & Export</Text>
          </TouchableOpacity>
        </View>
      )}

      {/* View: Gameplay */}
      {view === 'play' && (
        <View style={styles.centerContainer}>
          <Text style={styles.sectionTitle}>Make Your Move</Text>
          <Text style={styles.sectionSubtitle}>
            Tap a card to showdown with the Adaptive AI
          </Text>

          <View style={styles.movesGrid}>
            <TouchableOpacity
              style={styles.moveCard}
              onPress={() => handlePlayMove('rock')}
            >
              <Text style={styles.moveEmoji}>✊</Text>
              <Text style={styles.moveTitle}>Rock</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.moveCard}
              onPress={() => handlePlayMove('paper')}
            >
              <Text style={styles.moveEmoji}>✋</Text>
              <Text style={styles.moveTitle}>Paper</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.moveCard}
              onPress={() => handlePlayMove('scissors')}
            >
              <Text style={styles.moveEmoji}>✌️</Text>
              <Text style={styles.moveTitle}>Scissors</Text>
            </TouchableOpacity>
          </View>

          <TouchableOpacity
            style={[styles.actionBtn, styles.secondaryBtn, { marginTop: 24 }]}
            onPress={() => setView('mode-select')}
          >
            <Text style={styles.actionBtnText}>Change Mode</Text>
          </TouchableOpacity>
        </View>
      )}

      {/* View: Reveal Arena */}
      {view === 'reveal' && lastRound && (
        <View style={styles.centerContainer}>
          <View
            style={[
              styles.outcomeBanner,
              lastRound.outcome === 'win'
                ? styles.bannerWin
                : lastRound.outcome === 'lose'
                ? styles.bannerLose
                : styles.bannerTie,
            ]}
          >
            <Text style={styles.outcomeTitle}>
              {lastRound.outcome === 'win'
                ? 'VICTORY'
                : lastRound.outcome === 'lose'
                ? 'DEFEAT'
                : 'DRAW'}
            </Text>
            <Text style={styles.outcomeSubtitle}>
              {lastRound.outcome === 'win'
                ? 'You beat the adaptive model!'
                : lastRound.outcome === 'lose'
                ? 'AI anticipated your move'
                : 'Both made the same move'}
            </Text>
          </View>

          <View style={styles.showdownRow}>
            <View style={styles.showdownCard}>
              <Text style={styles.showdownLabel}>You</Text>
              <Text style={styles.showdownEmoji}>
                {lastRound.playerMove === 'rock'
                  ? '✊'
                  : lastRound.playerMove === 'paper'
                  ? '✋'
                  : '✌️'}
              </Text>
              <Text style={styles.showdownMoveName}>{lastRound.playerMove}</Text>
            </View>

            <View style={styles.showdownCard}>
              <Text style={styles.showdownLabel}>Bot ({difficulty.toUpperCase()})</Text>
              <Text style={styles.showdownEmoji}>
                {lastRound.botMove === 'rock'
                  ? '✊'
                  : lastRound.botMove === 'paper'
                  ? '✋'
                  : '✌️'}
              </Text>
              <Text style={styles.showdownMoveName}>{lastRound.botMove}</Text>
            </View>
          </View>

          <View style={styles.insightBox}>
            <Text style={styles.insightText}>
              Model: {lastRound.modelUsed} | Latency: {lastRound.latencyMs.toFixed(2)}ms
            </Text>
          </View>

          <TouchableOpacity
            style={[styles.actionBtn, styles.primaryBtn]}
            onPress={() => setView('play')}
          >
            <Text style={styles.primaryBtnText}>Play Next Round</Text>
          </TouchableOpacity>
        </View>
      )}

      {/* View: Statistics */}
      {view === 'stats' && (
        <ScrollView style={styles.scrollContainer} contentContainerStyle={{ paddingBottom: 40 }}>
          <Text style={styles.sectionTitle}>Game Statistics</Text>

          <View style={styles.kpiGrid}>
            <View style={styles.kpiCard}>
              <Text style={styles.kpiValue}>{stats.totalRounds}</Text>
              <Text style={styles.kpiLabel}>Total Rounds</Text>
            </View>
            <View style={styles.kpiCard}>
              <Text style={styles.kpiValue}>
                {(stats.overallPredictionAccuracy * 100).toFixed(0)}%
              </Text>
              <Text style={styles.kpiLabel}>AI Accuracy</Text>
            </View>
            <View style={styles.kpiCard}>
              <Text style={styles.kpiValue}>{(stats.botWinRate * 100).toFixed(0)}%</Text>
              <Text style={styles.kpiLabel}>Bot Win Rate</Text>
            </View>
            <View style={styles.kpiCard}>
              <Text style={styles.kpiValue}>{stats.averageLatencyMs.toFixed(2)}ms</Text>
              <Text style={styles.kpiLabel}>Avg Latency</Text>
            </View>
          </View>

          <TouchableOpacity
            style={[styles.actionBtn, styles.primaryBtn, { marginVertical: 12 }]}
            onPress={handleExportJSON}
          >
            <Text style={styles.primaryBtnText}>Export JSON Logs</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.actionBtn, styles.secondaryBtn, { marginBottom: 12 }]}
            onPress={handleReset}
          >
            <Text style={styles.actionBtnText}>Reset Game Data</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.actionBtn, styles.secondaryBtn]}
            onPress={() => setView('play')}
          >
            <Text style={styles.actionBtnText}>Back to Game</Text>
          </TouchableOpacity>
        </ScrollView>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#050505',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 14,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(255,255,255,0.1)',
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  headerSubtitle: {
    fontSize: 11,
    color: '#a1a1aa',
    fontFamily: Platform.OS === 'ios' ? 'Courier' : 'monospace',
  },
  statsBadge: {
    backgroundColor: 'rgba(255,255,255,0.1)',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
  },
  statsBadgeText: {
    color: '#ffffff',
    fontSize: 11,
    fontWeight: '600',
  },
  difficultyRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    paddingVertical: 8,
    gap: 8,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(255,255,255,0.06)',
  },
  diffBtn: {
    paddingHorizontal: 16,
    paddingVertical: 6,
    borderRadius: 8,
    backgroundColor: 'rgba(255,255,255,0.05)',
  },
  diffBtnActive: {
    backgroundColor: '#ffffff',
  },
  diffBtnText: {
    fontSize: 11,
    fontWeight: 'bold',
    color: '#a1a1aa',
  },
  diffBtnTextActive: {
    color: '#000000',
  },
  centerContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 20,
  },
  scrollContainer: {
    flex: 1,
    paddingHorizontal: 20,
    paddingTop: 20,
  },
  heroTitle: {
    fontSize: 32,
    fontWeight: '900',
    color: '#ffffff',
    marginBottom: 8,
    textAlign: 'center',
  },
  heroSubtitle: {
    fontSize: 14,
    color: '#a1a1aa',
    textAlign: 'center',
    marginBottom: 32,
  },
  card: {
    width: '100%',
    padding: 20,
    borderRadius: 16,
    borderWidth: 1,
    marginBottom: 16,
  },
  cyanCard: {
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    borderColor: 'rgba(255, 255, 255, 0.15)',
  },
  violetCard: {
    backgroundColor: 'rgba(255, 255, 255, 0.03)',
    borderColor: 'rgba(255, 255, 255, 0.1)',
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 4,
  },
  cardDesc: {
    fontSize: 13,
    color: '#a1a1aa',
  },
  sectionTitle: {
    fontSize: 26,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 6,
    textAlign: 'center',
  },
  sectionSubtitle: {
    fontSize: 13,
    color: '#a1a1aa',
    marginBottom: 30,
    textAlign: 'center',
  },
  movesGrid: {
    flexDirection: 'row',
    gap: 12,
    justifyContent: 'center',
  },
  moveCard: {
    width: 100,
    paddingVertical: 24,
    alignItems: 'center',
    borderRadius: 16,
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.15)',
  },
  moveEmoji: {
    fontSize: 44,
    marginBottom: 10,
  },
  moveTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  actionBtn: {
    width: '100%',
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: 'center',
  },
  primaryBtn: {
    backgroundColor: '#ffffff',
  },
  primaryBtnText: {
    color: '#000000',
    fontSize: 16,
    fontWeight: 'bold',
  },
  secondaryBtn: {
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
  },
  statsBtn: {
    backgroundColor: 'rgba(255, 255, 255, 0.08)',
    marginTop: 8,
  },
  actionBtnText: {
    color: '#ffffff',
    fontSize: 14,
    fontWeight: '600',
  },
  outcomeBanner: {
    width: '100%',
    padding: 20,
    borderRadius: 16,
    alignItems: 'center',
    marginBottom: 24,
    borderWidth: 1,
  },
  bannerWin: {
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    borderColor: 'rgba(255, 255, 255, 0.3)',
  },
  bannerLose: {
    backgroundColor: 'rgba(255, 255, 255, 0.04)',
    borderColor: 'rgba(255, 255, 255, 0.15)',
  },
  bannerTie: {
    backgroundColor: 'rgba(255, 255, 255, 0.06)',
    borderColor: 'rgba(255, 255, 255, 0.2)',
  },
  outcomeTitle: {
    fontSize: 28,
    fontWeight: '900',
    color: '#ffffff',
    marginBottom: 4,
  },
  outcomeSubtitle: {
    fontSize: 13,
    color: '#d4d4d8',
  },
  showdownRow: {
    flexDirection: 'row',
    gap: 16,
    marginBottom: 20,
  },
  showdownCard: {
    width: 140,
    padding: 20,
    borderRadius: 16,
    alignItems: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.15)',
  },
  showdownLabel: {
    fontSize: 12,
    color: '#a1a1aa',
    marginBottom: 8,
    textTransform: 'uppercase',
  },
  showdownEmoji: {
    fontSize: 48,
    marginBottom: 8,
  },
  showdownMoveName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#ffffff',
    textTransform: 'capitalize',
  },
  insightBox: {
    padding: 12,
    borderRadius: 8,
    backgroundColor: 'rgba(255, 255, 255, 0.04)',
    marginBottom: 24,
  },
  insightText: {
    color: '#a1a1aa',
    fontSize: 12,
    fontFamily: Platform.OS === 'ios' ? 'Courier' : 'monospace',
  },
  kpiGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
    marginBottom: 20,
  },
  kpiCard: {
    width: '47%',
    padding: 16,
    borderRadius: 12,
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.1)',
  },
  kpiValue: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 2,
  },
  kpiLabel: {
    fontSize: 12,
    color: '#a1a1aa',
  },
});
