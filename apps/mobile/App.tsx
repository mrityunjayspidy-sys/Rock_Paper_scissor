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
  createAdaptiveAI,
  chooseMove,
  updateModel,
  resolveOutcome,
  RoundLogger,
  AdaptiveAIState,
} from '@rps/core';

export default function App() {
  const [mode, setMode] = useState<'nocamera' | 'camera'>('nocamera');
  const [view, setView] = useState<'mode-select' | 'play' | 'reveal' | 'stats'>('mode-select');

  const [aiState, setAiState] = useState<AdaptiveAIState>(() =>
    createAdaptiveAI({ gamma: 0.94, epsilon: 0.08, coldStartRounds: 10 })
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

  const handleExportCSV = async () => {
    const csvStr = loggerRef.current.exportCSV();
    try {
      await Share.share({
        message: csvStr,
        title: 'RPS Round Logs CSV',
      });
    } catch (e) {
      Alert.alert('Export error', String(e));
    }
  };

  const handleExportJSON = async () => {
    const jsonStr = loggerRef.current.exportJSON();
    try {
      await Share.share({
        message: jsonStr,
        title: 'RPS Round Logs JSON',
      });
    } catch (e) {
      Alert.alert('Export error', String(e));
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="light" />

      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>RPS Adaptive AI</Text>
        <View style={styles.statsBadge}>
          <Text style={styles.statsBadgeText}>
            You: {stats.humanWins} | Bot: {stats.botWins} | Ties: {stats.ties}
          </Text>
        </View>
      </View>

      {/* View: Mode Selection */}
      {view === 'mode-select' && (
        <View style={styles.centerContainer}>
          <Text style={styles.heroTitle}>Adaptive Markov AI</Text>
          <Text style={styles.heroSubtitle}>
            Order-1 & Order-2 frequency tracking with exponential decay (γ=0.94)
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
            <Text style={styles.cardTitle}>Camera Gesture Mode</Text>
            <Text style={styles.cardDesc}>Vision camera landmark gesture classification</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.statsButton}
            onPress={() => setView('stats')}
          >
            <Text style={styles.statsButtonText}>View Stats & Exports</Text>
          </TouchableOpacity>
        </View>
      )}

      {/* View: Play (No Camera) */}
      {view === 'play' && (
        <View style={styles.centerContainer}>
          <Text style={styles.sectionTitle}>Choose Your Move</Text>

          <View style={styles.moveButtonsContainer}>
            <TouchableOpacity
              style={[styles.moveButton, styles.cyanBorder]}
              onPress={() => handlePlayMove('rock')}
            >
              <Text style={styles.moveEmoji}>✊</Text>
              <Text style={styles.moveLabel}>Rock</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[styles.moveButton, styles.violetBorder]}
              onPress={() => handlePlayMove('paper')}
            >
              <Text style={styles.moveEmoji}>✋</Text>
              <Text style={styles.moveLabel}>Paper</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[styles.moveButton, styles.emeraldBorder]}
              onPress={() => handlePlayMove('scissors')}
            >
              <Text style={styles.moveEmoji}>✌️</Text>
              <Text style={styles.moveLabel}>Scissors</Text>
            </TouchableOpacity>
          </View>

          <TouchableOpacity
            style={styles.secondaryButton}
            onPress={() => setView('mode-select')}
          >
            <Text style={styles.secondaryButtonText}>Back to Modes</Text>
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
                ? styles.winBanner
                : lastRound.outcome === 'lose'
                ? styles.loseBanner
                : styles.tieBanner,
            ]}
          >
            <Text style={styles.outcomeTitle}>
              {lastRound.outcome === 'win'
                ? 'VICTORY!'
                : lastRound.outcome === 'lose'
                ? 'DEFEAT!'
                : 'DRAW!'}
            </Text>
          </View>

          <View style={styles.versusRow}>
            <View style={styles.versusCard}>
              <Text style={styles.versusHeader}>YOU</Text>
              <Text style={styles.versusEmoji}>
                {lastRound.playerMove === 'rock' ? '✊' : lastRound.playerMove === 'paper' ? '✋' : '✌️'}
              </Text>
              <Text style={styles.versusLabel}>{lastRound.playerMove.toUpperCase()}</Text>
            </View>

            <Text style={styles.versusText}>VS</Text>

            <View style={styles.versusCard}>
              <Text style={styles.versusHeader}>BOT</Text>
              <Text style={styles.versusEmoji}>
                {lastRound.botMove === 'rock' ? '✊' : lastRound.botMove === 'paper' ? '✋' : '✌️'}
              </Text>
              <Text style={styles.versusLabel}>{lastRound.botMove.toUpperCase()}</Text>
            </View>
          </View>

          <View style={styles.aiInsightBox}>
            <Text style={styles.aiInsightText}>
              Predicted: {lastRound.predictedMove.toUpperCase()} | Model: {lastRound.modelUsed}
            </Text>
            <Text style={styles.aiInsightText}>
              Latency: {lastRound.latencyMs.toFixed(3)} ms
            </Text>
          </View>

          <TouchableOpacity
            style={styles.primaryActionButton}
            onPress={() => setView('play')}
          >
            <Text style={styles.primaryActionButtonText}>Next Round</Text>
          </TouchableOpacity>
        </View>
      )}

      {/* View: Stats & Export */}
      {view === 'stats' && (
        <ScrollView style={styles.statsContainer}>
          <Text style={styles.sectionTitle}>Model Analytics</Text>

          <View style={styles.statGrid}>
            <View style={styles.statBox}>
              <Text style={styles.statLabel}>Total Rounds</Text>
              <Text style={styles.statValue}>{stats.totalRounds}</Text>
            </View>
            <View style={styles.statBox}>
              <Text style={styles.statLabel}>AI Accuracy</Text>
              <Text style={styles.statValue}>{(stats.overallPredictionAccuracy * 100).toFixed(1)}%</Text>
            </View>
            <View style={styles.statBox}>
              <Text style={styles.statLabel}>Bot Win Rate</Text>
              <Text style={styles.statValue}>{(stats.botWinRate * 100).toFixed(1)}%</Text>
            </View>
            <View style={styles.statBox}>
              <Text style={styles.statLabel}>Order-1 Acc</Text>
              <Text style={styles.statValue}>{(stats.modelStats.order1RollingAccuracy * 100).toFixed(1)}%</Text>
            </View>
          </View>

          <View style={styles.exportRow}>
            <TouchableOpacity style={styles.exportButton} onPress={handleExportJSON}>
              <Text style={styles.exportButtonText}>Export JSON</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.exportButton} onPress={handleExportCSV}>
              <Text style={styles.exportButtonText}>Export CSV</Text>
            </TouchableOpacity>
          </View>

          <TouchableOpacity
            style={[styles.secondaryButton, { marginTop: 24, marginBottom: 40 }]}
            onPress={() => setView('mode-select')}
          >
            <Text style={styles.secondaryButtonText}>Back to Game</Text>
          </TouchableOpacity>
        </ScrollView>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#070a13',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 14,
    borderBottomWidth: 1,
    borderBottomColor: '#1e293b',
  },
  headerTitle: {
    color: '#38bdf8',
    fontSize: 18,
    fontWeight: 'bold',
  },
  statsBadge: {
    backgroundColor: '#0f172a',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#334155',
  },
  statsBadgeText: {
    color: '#cbd5e1',
    fontSize: 11,
    fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace',
  },
  centerContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  heroTitle: {
    fontSize: 28,
    fontWeight: '900',
    color: '#ffffff',
    textAlign: 'center',
    marginBottom: 8,
  },
  heroSubtitle: {
    fontSize: 14,
    color: '#94a3b8',
    textAlign: 'center',
    marginBottom: 32,
    maxWidth: 300,
  },
  card: {
    width: '100%',
    maxWidth: 320,
    padding: 20,
    borderRadius: 16,
    borderWidth: 1,
    backgroundColor: '#0f172a',
    marginBottom: 16,
  },
  cyanCard: {
    borderColor: 'rgba(6, 182, 212, 0.4)',
  },
  violetCard: {
    borderColor: 'rgba(139, 92, 246, 0.4)',
  },
  cardTitle: {
    color: '#ffffff',
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  cardDesc: {
    color: '#94a3b8',
    fontSize: 12,
  },
  statsButton: {
    marginTop: 12,
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#334155',
    backgroundColor: '#0f172a',
  },
  statsButtonText: {
    color: '#38bdf8',
    fontSize: 13,
    fontWeight: '600',
  },
  sectionTitle: {
    color: '#ffffff',
    fontSize: 22,
    fontWeight: 'bold',
    marginBottom: 24,
    textAlign: 'center',
  },
  moveButtonsContainer: {
    flexDirection: 'row',
    gap: 16,
    marginBottom: 32,
  },
  moveButton: {
    width: 90,
    height: 120,
    borderRadius: 16,
    backgroundColor: '#0f172a',
    borderWidth: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  cyanBorder: { borderColor: '#06b6d4' },
  violetBorder: { borderColor: '#8b5cf6' },
  emeraldBorder: { borderColor: '#10b981' },
  moveEmoji: { fontSize: 36, marginBottom: 8 },
  moveLabel: { color: '#ffffff', fontSize: 14, fontWeight: 'bold' },
  secondaryButton: {
    paddingVertical: 10,
    paddingHorizontal: 18,
    borderRadius: 10,
    backgroundColor: '#1e293b',
  },
  secondaryButtonText: {
    color: '#cbd5e1',
    fontSize: 13,
    fontWeight: '500',
  },
  outcomeBanner: {
    paddingVertical: 12,
    paddingHorizontal: 28,
    borderRadius: 16,
    marginBottom: 24,
    borderWidth: 1,
  },
  winBanner: { backgroundColor: 'rgba(16, 185, 129, 0.15)', borderColor: '#10b981' },
  loseBanner: { backgroundColor: 'rgba(244, 63, 94, 0.15)', borderColor: '#f43f5e' },
  tieBanner: { backgroundColor: 'rgba(245, 158, 11, 0.15)', borderColor: '#f59e0b' },
  outcomeTitle: { color: '#ffffff', fontSize: 24, fontWeight: '900' },
  versusRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 20,
    marginBottom: 24,
  },
  versusCard: {
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#0f172a',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#334155',
    minWidth: 100,
  },
  versusHeader: { color: '#94a3b8', fontSize: 11, fontWeight: 'bold', marginBottom: 6 },
  versusEmoji: { fontSize: 40, marginBottom: 6 },
  versusLabel: { color: '#ffffff', fontSize: 13, fontWeight: 'bold' },
  versusText: { color: '#64748b', fontSize: 16, fontWeight: 'bold' },
  aiInsightBox: {
    padding: 12,
    borderRadius: 12,
    backgroundColor: '#0f172a',
    borderWidth: 1,
    borderColor: '#1e293b',
    alignItems: 'center',
    marginBottom: 24,
  },
  aiInsightText: { color: '#94a3b8', fontSize: 12, marginBottom: 2 },
  primaryActionButton: {
    backgroundColor: '#06b6d4',
    paddingVertical: 14,
    paddingHorizontal: 36,
    borderRadius: 14,
  },
  primaryActionButtonText: { color: '#070a13', fontSize: 16, fontWeight: 'bold' },
  statsContainer: { flex: 1, padding: 20 },
  statGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
    marginBottom: 24,
  },
  statBox: {
    flex: 1,
    minWidth: '45%',
    backgroundColor: '#0f172a',
    padding: 16,
    borderRadius: 14,
    borderWidth: 1,
    borderColor: '#1e293b',
  },
  statLabel: { color: '#94a3b8', fontSize: 12, marginBottom: 4 },
  statValue: { color: '#ffffff', fontSize: 22, fontWeight: 'bold' },
  exportRow: { flexDirection: 'row', gap: 12, marginTop: 8 },
  exportButton: {
    flex: 1,
    backgroundColor: '#1e293b',
    paddingVertical: 12,
    borderRadius: 12,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#334155',
  },
  exportButtonText: { color: '#38bdf8', fontSize: 13, fontWeight: '600' },
});
