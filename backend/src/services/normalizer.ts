import { AccessPathResult, BarrierSeverity } from '../types.js';

export function normalizeTinyFishResult(raw: any): AccessPathResult {
  if (!raw || typeof raw !== 'object') {
    return {
      overallTaskSuccess: false,
      confidence: 0.1,
      summary: 'No valid data returned from TinyFish Web Agent.',
      steps: [
        {
          stepNumber: 1,
          action: 'Initialize browser session',
          result: 'Failed to obtain structured response',
          success: false,
          barrierDetected: true,
          barrierType: 'Dead End',
          severity: 'critical',
          evidence: 'Agent did not produce output data',
          recommendation: 'Check URL accessibility and agent connectivity'
        }
      ],
      barriers: [
        {
          stepNumber: 1,
          type: 'Dead End',
          severity: 'critical',
          title: 'Agent Execution Interrupted',
          description: 'The automated agent was unable to execute the requested user journey.',
          evidence: 'Empty or malformed agent result payload',
          recommendation: 'Verify that the target URL is accessible and accepts browser connections.'
        }
      ]
    };
  }

  // Handle nested result if TinyFish wraps in { result: ... } or { resultJson: ... }
  const payload = raw.resultJson || raw.result || raw;

  const overallTaskSuccess = Boolean(
    payload.overallTaskSuccess !== undefined ? payload.overallTaskSuccess : payload.success ?? false
  );

  const confidence = typeof payload.confidence === 'number'
    ? Math.max(0, Math.min(1, payload.confidence))
    : 0.85;

  const summary = typeof payload.summary === 'string'
    ? payload.summary
    : 'Agent journey analyzed.';

  // Normalize steps
  const rawSteps = Array.isArray(payload.steps) ? payload.steps : [];
  const steps = rawSteps.map((s: any, idx: number) => {
    const stepNumber = typeof s.stepNumber === 'number' ? s.stepNumber : idx + 1;
    const action = String(s.action || `Step ${stepNumber}`);
    const context = s.context ? String(s.context) : undefined;
    const result = String(s.result || (s.success ? 'Step passed' : 'Step blocked'));
    const success = Boolean(s.success ?? !s.barrierDetected);
    const barrierDetected = Boolean(s.barrierDetected ?? !success);

    let severity: BarrierSeverity | undefined = undefined;
    if (s.severity && ['minor', 'moderate', 'major', 'critical'].includes(s.severity.toLowerCase())) {
      severity = s.severity.toLowerCase() as BarrierSeverity;
    } else if (barrierDetected) {
      severity = 'moderate';
    }

    return {
      stepNumber,
      action,
      context,
      result,
      success,
      barrierDetected,
      barrierType: s.barrierType ? String(s.barrierType) : (barrierDetected ? 'Navigation' : undefined),
      severity,
      evidence: s.evidence ? String(s.evidence) : undefined,
      recommendation: s.recommendation ? String(s.recommendation) : undefined
    };
  });

  // Normalize barriers
  const rawBarriers = Array.isArray(payload.barriers) ? payload.barriers : [];
  const barriers = rawBarriers.map((b: any, idx: number) => {
    const stepNumber = typeof b.stepNumber === 'number' ? b.stepNumber : idx + 1;
    const type = String(b.type || 'Navigation');
    let severity: BarrierSeverity = 'moderate';
    if (b.severity && ['minor', 'moderate', 'major', 'critical'].includes(b.severity.toLowerCase())) {
      severity = b.severity.toLowerCase() as BarrierSeverity;
    }

    return {
      stepNumber,
      type,
      severity,
      title: String(b.title || `${type} Barrier at Step ${stepNumber}`),
      description: String(b.description || 'User was impeded or confused during this action.'),
      evidence: b.evidence ? String(b.evidence) : undefined,
      recommendation: b.recommendation ? String(b.recommendation) : undefined
    };
  });

  return {
    overallTaskSuccess,
    confidence,
    summary,
    steps,
    barriers
  };
}
