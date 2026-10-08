import React from 'react';
import { Barrier } from '../types';
import { AlertCircle, AlertTriangle, XCircle, Info, CheckCircle2, ArrowRight } from 'lucide-react';

interface BarrierCardProps {
  barrier: Barrier;
  index: number;
}

export const BarrierCard: React.FC<BarrierCardProps> = ({ barrier, index }) => {
  const [expanded, setExpanded] = React.useState(true);

  // Severity styling
  let severityBadge = 'bg-amber-100 text-amber-800 border-amber-300';
  let SeverityIcon = AlertTriangle;

  if (barrier.severity === 'critical') {
    severityBadge = 'bg-rose-100 text-rose-800 border-rose-300';
    SeverityIcon = XCircle;
  } else if (barrier.severity === 'major') {
    severityBadge = 'bg-orange-100 text-orange-800 border-orange-300';
    SeverityIcon = AlertCircle;
  } else if (barrier.severity === 'minor') {
    severityBadge = 'bg-slate-100 text-slate-700 border-slate-300';
    SeverityIcon = Info;
  }

  // Type badge styling
  let typeBadge = 'bg-indigo-50 text-indigo-700 border-indigo-200';
  if (barrier.type === 'Dead End') {
    typeBadge = 'bg-rose-50 text-rose-700 border-rose-200';
  } else if (barrier.type === 'Accessibility') {
    typeBadge = 'bg-purple-50 text-purple-700 border-purple-200';
  } else if (barrier.type === 'Language') {
    typeBadge = 'bg-blue-50 text-blue-700 border-blue-200';
  }

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden transition hover:shadow-sm">
      {/* Header bar */}
      <div
        onClick={() => setExpanded(!expanded)}
        className="p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 cursor-pointer bg-slate-50/50 hover:bg-slate-50 transition border-b border-slate-100"
      >
        <div className="flex items-center gap-3">
          <span className="w-6 h-6 rounded-md bg-slate-200 text-slate-700 font-bold text-xs flex items-center justify-center shrink-0">
            {index + 1}
          </span>
          <div className="flex flex-wrap items-center gap-2">
            <span className={`text-[11px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full border ${typeBadge}`}>
              {barrier.type}
            </span>
            <span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full border flex items-center gap-1 ${severityBadge}`}>
              <SeverityIcon className="w-3 h-3" />
              <span className="capitalize">{barrier.severity}</span>
            </span>
            {barrier.stepNumber && (
              <span className="text-xs text-slate-400 font-medium">
                Step {barrier.stepNumber}
              </span>
            )}
          </div>
        </div>

        <h4 className="font-bold text-sm text-slate-900 flex-1 sm:text-right">
          {barrier.title}
        </h4>
      </div>

      {/* Expanded Content: What happened, Why it matters, Evidence, Recommended Fix */}
      {expanded && (
        <div className="p-6 space-y-4 text-xs">
          {/* 1. What happened */}
          <div>
            <div className="font-bold text-slate-900 uppercase tracking-wider text-[11px] mb-1 text-indigo-700">
              What Happened?
            </div>
            <p className="text-slate-700 leading-relaxed text-sm">
              {barrier.description}
            </p>
          </div>

          {/* 2. Why it matters (User impact) */}
          {barrier.userImpact && (
            <div className="p-3 bg-amber-50/60 rounded-lg border border-amber-200/80">
              <div className="font-bold text-amber-900 uppercase tracking-wider text-[10px] mb-0.5">
                Why it Matters (User Impact):
              </div>
              <p className="text-amber-800 leading-relaxed font-medium">
                {barrier.userImpact}
              </p>
            </div>
          )}

          {/* 3. Evidence */}
          {barrier.evidence && (
            <div>
              <div className="font-bold text-slate-900 uppercase tracking-wider text-[11px] mb-1 text-slate-500">
                Agent Observed Evidence:
              </div>
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 font-mono text-[11px] text-slate-700 leading-relaxed">
                {barrier.evidence}
              </div>
            </div>
          )}

          {/* 4. Concrete Recommendation */}
          {barrier.recommendation && (
            <div className="p-3.5 bg-emerald-50 rounded-lg border border-emerald-200">
              <div className="font-bold text-emerald-900 uppercase tracking-wider text-[10px] mb-1 flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-700" />
                <span>Recommended Concrete Fix:</span>
              </div>
              <p className="text-emerald-800 leading-relaxed font-medium">
                {barrier.recommendation}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
