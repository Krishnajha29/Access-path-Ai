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
  personaInsights?: {
    personaName: string;
    evaluationFocus: string;
    personaBarriers: string[];
  };
}

export const PRESET_PERSONAS: Persona[] = [
  {
    id: 'first-time-user',
    name: 'First-Time User',
    description: 'Limited familiarity with complex institutional portals and multi-step government/academic workflows.',
    constraints: [
      'Relies heavily on visual hierarchy and obvious next-step cues',
      'Easily distracted by unrelated announcements or circulars',
      'Needs explicit clarity before clicking irreversible actions'
    ],
    badge: 'Beginner'
  },
  {
    id: 'mobile-first-user',
    name: 'Mobile-First User',
    description: 'Interacts primarily through smartphone browser on high-latency mobile networks.',
    constraints: [
      'Small viewport interaction (touch targets, no hover states)',
      'High friction with large horizontal tables or tiny tap buttons',
      'Struggles with desktop-optimized PDF or document upload controls'
    ],
    badge: 'Mobile'
  },
  {
    id: 'hindi-speaking-student',
    name: 'Hindi-Speaking Student',
    description: 'Comfortable with conversational vernacular; encounters language barriers with dense legalistic English.',
    constraints: [
      'Struggles with archaic bureaucratic jargon',
      'Needs bilingual tooltips or plain English explanations',
      'Requires clear translation of statutory eligibility thresholds'
    ],
    badge: 'Vernacular'
  },
  {
    id: 'low-digital-literacy',
    name: 'Low Digital-Literacy User',
    description: 'Needs direct, linear, and obvious paths; easily bewildered by modal overlays and hidden collapsibles.',
    constraints: [
      'Cannot discover collapsed accordions or buried links',
      'Confused when "Reset" looks more prominent than "Submit"',
      'Requires explicit error recovery guidance instead of technical error codes'
    ],
    badge: 'Essential UI'
  },
  {
    id: 'screen-reader-user',
    name: 'Screen-Reader User',
    description: 'Relies on non-visual navigation, ARIA semantics, meaningful labels, and keyboard order.',
    constraints: [
      'Form controls must have accessible names and semantic labels',
      'Interactive elements must be keyboard reachable and announce state',
      'Contrast and focus indicators must be unambiguous'
    ],
    badge: 'Assistive Tech'
  }
];
