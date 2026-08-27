import os

def fix_file(path, old_str, new_str):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if old_str in content:
        content = content.replace(old_str, new_str, 1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Fixed in {path}")
    else:
        print(f"Pattern not found in {path}")

# 1. packages/core/src/ai.ts
fix_file(
    "packages/core/src/ai.ts",
    "export function updateModel(\n  state: AdaptiveAIState,\n  actualMove: Move,\n  predictedMove?: Move,\n  modelUsed?: ModelType,\n  historyBeforeMove: readonly Move[] = []\n): AdaptiveAIState {",
    "export function updateModel(\n  state: AdaptiveAIState,\n  actualMove: Move,\n  _predictedMove?: Move,\n  _modelUsed?: ModelType,\n  historyBeforeMove: readonly Move[] = []\n): AdaptiveAIState {"
)

# 2. packages/core/src/classifier.ts
fix_file(
    "packages/core/src/classifier.ts",
    "import { Move, Landmark3D, HandClassificationResult } from './types';",
    "import { Landmark3D, HandClassificationResult } from './types';"
)

# 3. packages/core/src/logger.ts
fix_file(
    "packages/core/src/logger.ts",
    "import { RoundLog, SummaryStats, ModelAccuracyStats, ModelType, Outcome } from './types';",
    "import { RoundLog, SummaryStats, ModelType } from './types';"
)

# 4. apps/web/src/components/CameraGame.tsx
fix_file(
    "apps/web/src/components/CameraGame.tsx",
    "import { Camera, RefreshCw, AlertCircle, Sparkles } from 'lucide-react';",
    "import { RefreshCw, AlertCircle, Sparkles } from 'lucide-react';"
)
