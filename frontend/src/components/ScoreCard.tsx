import React from 'react';
import { TestRecord } from '../types';
import { AlertTriangle, CheckCircle2, XCircle, Info, ChevronDown, ChevronUp } from 'lucide-react';

interface ScoreCardProps {
  test: TestRecord;
}

export const ScoreCard: React.FC<ScoreCardProps> = ({ test }) => {
  const [showBreakdown, setShowBreakdown] = React.useState(false);

  const score = test.score ?? 0;
  const status = test.completionStatus ?? 'Completed with barriers';
  const totalSteps = test.steps.length;
  const completedSteps = test.steps.filter(s => s.success).length;
  const blockedSteps = test.steps.filter(s => !s.success).length;
  const barrierCount = test.barriers.length;

  // Determine score color
  let scoreColorClass = 'text-emerald-600 border-emerald-500 bg-emerald-50';
  let badgeClass = 'bg-emerald-100 text-emerald-800 border-emerald-300';
  let StatusIcon = CheckCircle2;

  if (score < 50 || status === 'Blocked') {
    scoreColorClass = 'text-rose-600 border-rose-500 bg-rose-50';
    badgeClass = 'bg-rose-100 text-rose-800 border-rose-300';
    StatusIcon = XCircle;
  } else if (score < 80 || status === 'Completed with barriers' || status === 'Partially completed') {
    scoreColorClass = 'text-amber-600 border-amber-500 bg-amber-50';
    badgeClass = 'bg-amber-100 text-amber-800 border-amber-300';
    StatusIcon = AlertTriangle;
  }

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 sm:p-8">
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 pb-6 border-b border-slate-100">
        <div>
          <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Task Test Result</span>
          <h2 className="text-2xl font-bold text-slate-900 mt-1">AccessPath Task Success Score</h2>
          <p className="text-sm text-slate-500 mt-1">
            Evaluates whether the specified persona can reach the end goal without being blocked or misled.
          </p>
        </div>

        {/* Completion status pill */}
        <div className={`inline-flex items-center space-x-2 px-4 py-2 rounded-xl border text-sm font-semibold self-start lg:self-auto ${badgeClass}`}>
          <StatusIcon className="w-4 h-4" />
          <span>{status}</span>
        </div>
      </div>

      {/* Main Score Display & Journey Stats */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-center pt-6">
        {/* Score Number Circle / Block */}
        <div className="md:col-span-5 flex items-center gap-5">
          <div className={`w-28 h-28 rounded-2xl flex flex-col items-center justify-center border-2 shadow-xs shrink-0 ${scoreColorClass}`}>
            <span className="text-4xl font-extrabold tracking-tight">{score}</span>
            <span className="text-xs font-semibold uppercase opacity-75">/ 100</span>
          </div>

          <div>
            <div className="text-sm font-bold text-slate-800">
              {score >= 85 ? 'High Task Feasibility' : score >= 60 ? 'Moderate Task Friction' : 'Severe Task Barriers'}
            </div>
            <p className="text-xs text-slate-500 mt-1 leading-relaxed">
              Calculated deterministically from actual observed barriers during the live browser agent execution.
            </p>
            <button
              onClick={() => setShowBreakdown(!showBreakdown)}
              className="mt-2 text-xs font-medium text-indigo-600 hover:text-indigo-800 inline-flex items-center gap-1"
            >
              <span>{showBreakdown ? 'Hide score breakdown' : 'View score breakdown'}</span>
              {showBreakdown ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
            </button>
          </div>
        </div>

        {/* Journey Statistics Grid */}
        <div className="md:col-span-7 grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-50 p-4 rounded-xl border border-slate-100">
          <div className="p-3 bg-white rounded-lg border border-slate-200">
            <div className="text-xs text-slate-400 font-medium">Total Steps</div>
            <div className="text-xl font-bold text-slate-800 mt-0.5">{totalSteps}</div>
          </div>
          <div className="p-3 bg-white rounded-lg border border-slate-200">
            <div className="text-xs text-slate-400 font-medium">Completed</div>
            <div className="text-xl font-bold text-emerald-600 mt-0.5">{completedSteps}</div>
          </div>
          <div className="p-3 bg-white rounded-lg border border-slate-200">
            <div className="text-xs text-slate-400 font-medium">Blocked</div>
            <div className="text-xl font-bold text-rose-600 mt-0.5">{blockedSteps}</div>
          </div>
          <div className="p-3 bg-white rounded-lg border border-slate-200">
            <div className="text-xs text-slate-400 font-medium">Barriers</div>
            <div className="text-xl font-bold text-amber-600 mt-0.5">{barrierCount}</div>
          </div>
        </div>
      </div>

      {/* Transparent Deduction Breakdown Drawer */}
      {showBreakdown && test.scoreBreakdown && (
        <div className="mt-6 pt-6 border-t border-slate-100 bg-slate-50 -mx-6 sm:-mx-8 -mb-6 sm:-mb-8 p-6 sm:p-8 rounded-b-2xl">
          <div className="flex items-center gap-2 mb-3">
            <Info className="w-4 h-4 text-indigo-600" />
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700">Deduction Rulebook Breakdown</h4>
          </div>
          <div className="space-y-2 text-xs">
            <div className="flex justify-between py-1 border-b border-slate-200 text-slate-600 font-medium">
              <span>Baseline Ideal Score</span>
              <span className="font-bold text-slate-800">100 pts</span>
            </div>
            {test.scoreBreakdown.deductions.map((d, i) => (
              <div key={i} className="flex justify-between py-1 text-slate-600">
                <div>
                  <span className="font-semibold text-slate-800">{d.type}: </span>
                  <span className="text-slate-500">{d.reason}</span>
                </div>
                <span className="font-bold text-rose-600">-{d.points} pts</span>
              </div>
            ))}
            <div className="flex justify-between pt-2 border-t border-slate-200 text-sm font-bold text-slate-900">
              <span>Final Task Success Score</span>
              <span>{score} / 100</span>
            </div>
          </div>
          <p className="text-[11px] text-slate-400 mt-3 italic">
            * Note: This is an internal AccessPath task completion metric, not a standardized regulatory certification.
          </p>
        </div>
      )}
    </div>
  );
};
