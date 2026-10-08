import { Barrier, TaskCompletionStatus, TestStep } from '../types.js';

export interface ScoreCalculationResult {
  score: number;
  completionStatus: TaskCompletionStatus;
  scoreBreakdown: {
    baseScore: number;
    deductions: {
      type: string;
      reason: string;
      points: number;
    }[];
  };
}

export function calculateTaskSuccessScore(
  overallTaskSuccess: boolean,
  steps: TestStep[],
  barriers: Barrier[]
): ScoreCalculationResult {
  const baseScore = 100;
  const deductions: { type: string; reason: string; points: number }[] = [];

  let currentScore = baseScore;

  // Deductions based on observed barriers
  for (const barrier of barriers) {
    let penalty = 0;
    const severity = barrier.severity;

    switch (severity) {
      case 'critical':
        penalty = 25;
        break;
      case 'major':
        penalty = 15;
        break;
      case 'moderate':
        // If it's a language/jargon barrier, deduct 8 pts, otherwise 10 pts
        penalty = barrier.type === 'Language' ? 8 : 10;
        break;
      case 'minor':
        penalty = 5;
        break;
    }

    if (penalty > 0) {
      deductions.push({
        type: `${barrier.type} (${severity})`,
        reason: barrier.title,
        points: penalty
      });
      currentScore -= penalty;
    }
  }

  // Deductions for blocked steps if not already captured
  const blockedSteps = steps.filter(s => !s.success);
  if (!overallTaskSuccess && blockedSteps.length > 0 && deductions.length === 0) {
    deductions.push({
      type: 'Task Failure',
      reason: 'Agent could not reach terminal completion state',
      points: 35
    });
    currentScore -= 35;
  }

  // Clamp score between 0 and 100
  const finalScore = Math.max(0, Math.min(100, currentScore));

  // Determine Task Completion Status
  let completionStatus: TaskCompletionStatus;
  const criticalCount = barriers.filter(b => b.severity === 'critical').length;
  const majorCount = barriers.filter(b => b.severity === 'major').length;

  if (criticalCount > 0 || (!overallTaskSuccess && finalScore < 40)) {
    completionStatus = 'Blocked';
  } else if (!overallTaskSuccess && finalScore < 65) {
    completionStatus = 'Completed with barriers';
  } else if (!overallTaskSuccess) {
    completionStatus = 'Partially completed';
  } else if (majorCount > 0 || barriers.length >= 2) {
    completionStatus = 'Completed with barriers';
  } else {
    completionStatus = 'Successfully completed';
  }

  return {
    score: finalScore,
    completionStatus,
    scoreBreakdown: {
      baseScore,
      deductions
    }
  };
}
