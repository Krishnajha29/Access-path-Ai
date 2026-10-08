import React from 'react';
import { Barrier } from '../types';
import { Search, ShieldAlert, ArrowDown, Sparkles, Layers } from 'lucide-react';

interface EvidencePanelProps {
  barriers: Barrier[];
}

export const EvidencePanel: React.FC<EvidencePanelProps> = ({ barriers }) => {
  if (barriers.length === 0) {
    return (
      <div className="bg-emerald-50 border border-emerald-200 rounded-2xl p-6 text-center text-emerald-900">
        <Sparkles className="w-8 h-8 text-emerald-600 mx-auto mb-2" />
        <h4 className="font-bold text-base">Zero Task Blockers Detected!</h4>
        <p className="text-xs text-emerald-700 mt-1 max-w-md mx-auto">
          The tested persona completed the entire journey without being impeded by unclear labels, missing documents, or confusing navigation.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 sm:p-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <span className="text-xs font-bold uppercase tracking-wider text-indigo-600">Verification Protocol</span>
          <h3 className="text-lg font-bold text-slate-900 mt-0.5">Evidence-First Barrier Diagnostic</h3>
          <p className="text-xs text-slate-500 mt-1">
            Every barrier is substantiated through the 4-stage validation chain: Observation &rarr; Evidence &rarr; Impact &rarr; Recommendation.
          </p>
        </div>
        <div className="hidden sm:flex items-center gap-2 text-xs font-semibold px-3 py-1.5 rounded-lg bg-indigo-50 text-indigo-700 border border-indigo-200">
          <Layers className="w-4 h-4" />
          <span>{barriers.length} Verified Barriers</span>
        </div>
      </div>

      <div className="space-y-6">
        {barriers.map((barrier, idx) => (
          <div key={idx} className="border border-slate-200 rounded-xl p-5 bg-slate-50/40 hover:bg-white transition shadow-xs">
            {/* Header */}
            <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-slate-200">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-slate-400">#{idx + 1}</span>
                <span className="font-bold text-sm text-slate-900">{barrier.title}</span>
              </div>
              <div className="flex items-center gap-2 text-xs">
                <span className="px-2 py-0.5 rounded font-semibold bg-slate-100 text-slate-700 border border-slate-200">
                  {barrier.type}
                </span>
                <span className="px-2 py-0.5 rounded font-semibold capitalize bg-amber-100 text-amber-800 border border-amber-200">
                  {barrier.severity}
                </span>
              </div>
            </div>

            {/* 4-Stage Evidence Pipeline */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 pt-4 text-xs">
              {/* 1. Observation */}
              <div className="bg-white p-3.5 rounded-lg border border-slate-200">
                <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">
                  1. Observation
                </div>
                <p className="text-slate-800 font-medium leading-relaxed">
                  {barrier.description}
                </p>
              </div>

              {/* 2. Evidence */}
              <div className="bg-white p-3.5 rounded-lg border border-slate-200">
                <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">
                  2. Evidence
                </div>
                <p className="text-slate-600 font-mono text-[11px] leading-relaxed">
                  {barrier.evidence || 'Recorded in agent DOM trace'}
                </p>
              </div>

              {/* 3. Impact */}
              <div className="bg-amber-50/70 p-3.5 rounded-lg border border-amber-200">
                <div className="text-[10px] font-bold text-amber-900 uppercase tracking-wider mb-1">
                  3. User Impact
                </div>
                <p className="text-amber-800 font-medium leading-relaxed">
                  {barrier.userImpact || 'Causes hesitation and potential workflow drop-off'}
                </p>
              </div>

              {/* 4. Recommendation */}
              <div className="bg-emerald-50 p-3.5 rounded-lg border border-emerald-200">
                <div className="text-[10px] font-bold text-emerald-900 uppercase tracking-wider mb-1">
                  4. Recommendation
                </div>
                <p className="text-emerald-800 font-medium leading-relaxed">
                  {barrier.recommendation || 'Provide explicit user guidance'}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
