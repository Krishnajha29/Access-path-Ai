export type PersonaId =
  | 'first-time-user'
  | 'mobile-first-user'
  | 'hindi-speaking-student'
  | 'low-digital-literacy'
  | 'screen-reader-user';

export interface Persona {
  id: PersonaId;
  name: string;
  description: string;
  constraints: string[];
  icon?: string;
  badge?: string;
}

export type BarrierSeverity = 'minor' | 'moderate' | 'major' | 'critical';

export type BarrierType =
  | 'Navigation'
  | 'Language'
  | 'Form Usability'
  | 'Accessibility'
  | 'Mobile Usability'
  | 'Information Architecture'
  | 'Error Recovery'
  | 'Dead End';

export interface TestStep {
  id?: string;
  stepNumber: number;
  action: string;
  context?: string;
  result: string;
  success: boolean;
  barrierDetected: boolean;
  barrierType?: BarrierType | string;
  severity?: BarrierSeverity;
  evidence?: string;
  recommendation?: string;
}

export interface Barrier {
  id?: string;
  stepNumber: number;
  type: BarrierType | string;
  severity: BarrierSeverity;
  title: string;
  description: string;
  evidence?: string;
  recommendation?: string;
  userImpact?: string;
}

export type TestStatus =
  | 'pending'
  | 'running'
  | 'analyzing'
  | 'completed'
  | 'failed';

export type TaskCompletionStatus =
  | 'Successfully completed'
  | 'Completed with barriers'
  | 'Partially completed'
  | 'Blocked';

export interface AccessPathResult {
  overallTaskSuccess: boolean;
  confidence: number;
  summary: string;
  steps: {
    stepNumber: number;
    action: string;
    context?: string;
    result: string;
    success: boolean;
    barrierDetected: boolean;
    barrierType?: string;
    severity?: BarrierSeverity;
    evidence?: string;
    recommendation?: string;
  }[];
  barriers: {
    stepNumber: number;
    type: string;
    severity: BarrierSeverity;
    title: string;
    description: string;
    evidence?: string;
    recommendation?: string;
  }[];
}

export interface TestRecord {
  id: string;
  url: string;
  task: string;
  persona: Persona;
  status: TestStatus;
  completionStatus?: TaskCompletionStatus;
  score?: number;
  scoreBreakdown?: {
    baseScore: number;
    deductions: {
      type: string;
      reason: string;
      points: number;
    }[];
  };
  overallTaskSuccess?: boolean;
  confidence?: number;
  summary?: string;
  steps: TestStep[];
  barriers: Barrier[];
  streamingUrl?: string;
  runUrl?: string;
  runId?: string;
  createdAt: string;
  updatedAt: string;
  retestedFromId?: string;
  retestId?: string;
  isImprovedDemo?: boolean;
}

export interface RetestComparison {
  beforeTestId: string;
  afterTestId: string;
  beforeScore: number;
  afterScore: number;
  scoreDelta: number;
  barriersResolved: number;
  remainingBarriers: number;
}
