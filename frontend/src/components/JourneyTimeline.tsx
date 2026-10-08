import React from 'react';
import { TestStep } from '../types';
import { CheckCircle2, AlertTriangle, XCircle, ArrowRight, Lightbulb, FileText } from 'lucide-react';

interface JourneyTimelineProps {
  steps: TestStep[];
}

export const JourneyTimeline: React.FC<JourneyTimelineProps> = ({ steps }) => {
  const [selectedStep, setSelectedStep] = React.useState<TestStep | null>(
    steps.length > 0 ? steps[0] : null
  );

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 sm:p-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-6">
        <div>
          <h3 className="text-lg font-bold text-slate-900">User Journey Timeline</h3>
          <p className="text-xs text-slate-500">
            Step-by-step trace of the user persona navigating the website. Click any step for detailed evidence.
          </p>
        </div>
        <div className="flex items-center gap-4 text-xs font-medium text-slate-500">
          <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-emerald-500" /> Succeeded</span>
          <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-amber-500" /> Barrier</span>
          <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-rose-500" /> Blocked</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Timeline Steps Column */}
        <div className="lg:col-span-7 space-y-3">
          {steps.map((step) => {
            const isSelected = selectedStep?.stepNumber === step.stepNumber;
            const isBlocked = !step.success;
            const hasBarrier = step.barrierDetected;

            let iconNode = <CheckCircle2 className="w-4 h-4 text-emerald-600" />;
            let statusPillClass = 'text-emerald-700 bg-emerald-50 border-emerald-200';
            let stepBorderClass = isSelected ? 'border-indigo-600 ring-2 ring-indigo-100 bg-indigo-50/20' : 'border-slate-200 hover:border-slate-300';

            if (isBlocked) {
              iconNode = <XCircle className="w-4 h-4 text-rose-600" />;
              statusPillClass = 'text-rose-700 bg-rose-50 border-rose-200';
            } else if (hasBarrier) {
              iconNode = <AlertTriangle className="w-4 h-4 text-amber-600" />;
              statusPillClass = 'text-amber-700 bg-amber-50 border-amber-200';
            }

            return (
              <button
                key={step.stepNumber}
                type="button"
                onClick={() => setSelectedStep(step)}
                className={`w-full text-left p-4 rounded-xl border transition flex items-center justify-between gap-4 bg-white ${stepBorderClass}`}
              >
                <div className="flex items-center gap-3.5 min-w-0">
                  <div className="w-8 h-8 rounded-lg bg-slate-100 text-slate-700 font-bold text-xs flex items-center justify-center shrink-0">
                    {String(step.stepNumber).padStart(2, '0')}
                  </div>
                  <div className="min-w-0">
                    <div className="font-semibold text-sm text-slate-900 truncate">
                      {step.action}
                    </div>
                    {step.context && (
                      <div className="text-[11px] text-slate-500 truncate mt-0.5">
                        {step.context}
                      </div>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-3 shrink-0">
                  <div className={`px-2 py-0.5 rounded text-[11px] font-semibold border flex items-center gap-1 ${statusPillClass}`}>
                    {iconNode}
                    <span>{isBlocked ? 'Blocked' : hasBarrier ? 'Barrier' : 'Passed'}</span>
                  </div>
                  <ArrowRight className={`w-4 h-4 transition ${isSelected ? 'text-indigo-600 translate-x-0.5' : 'text-slate-300'}`} />
                </div>
              </button>
            );
          })}
        </div>

        {/* Detail Panel Column */}
        <div className="lg:col-span-5 bg-slate-50 rounded-xl p-5 border border-slate-200 sticky top-24">
          {selectedStep ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between border-b border-slate-200 pb-3">
                <span className="text-xs font-bold text-indigo-700 uppercase tracking-wider">
                  Step {selectedStep.stepNumber} Detail
                </span>
                <span className={`px-2 py-0.5 rounded text-xs font-semibold ${
                  !selectedStep.success
                    ? 'bg-rose-100 text-rose-800'
                    : selectedStep.barrierDetected
                    ? 'bg-amber-100 text-amber-800'
                    : 'bg-emerald-100 text-emerald-800'
                }`}>
                  {!selectedStep.success ? 'Blocked Step' : selectedStep.barrierDetected ? 'Usability Barrier' : 'Step Succeeded'}
                </span>
              </div>

              <div>
                <h4 className="font-bold text-slate-900 text-sm">{selectedStep.action}</h4>
                {selectedStep.context && (
                  <p className="text-xs text-slate-500 mt-0.5 font-medium">{selectedStep.context}</p>
                )}
              </div>

              <div className="p-3 bg-white rounded-lg border border-slate-200 text-xs text-slate-700">
                <div className="font-semibold text-slate-900 mb-1 flex items-center gap-1.5">
                  <FileText className="w-3.5 h-3.5 text-indigo-600" />
                  <span>Agent Observation</span>
                </div>
                <p className="leading-relaxed">{selectedStep.result}</p>
              </div>

              {selectedStep.evidence && (
                <div className="p-3 bg-amber-50/70 border border-amber-200 rounded-lg text-xs text-amber-900">
                  <div className="font-semibold mb-1">Observed Evidence:</div>
                  <p className="leading-relaxed font-mono text-[11px] bg-white p-2 rounded border border-amber-200">
                    {selectedStep.evidence}
                  </p>
                </div>
              )}

              {selectedStep.recommendation && (
                <div className="p-3 bg-indigo-50 border border-indigo-200 rounded-lg text-xs text-indigo-900">
                  <div className="font-semibold mb-1 flex items-center gap-1.5">
                    <Lightbulb className="w-3.5 h-3.5 text-indigo-700" />
                    <span>Recommended Improvement:</span>
                  </div>
                  <p className="leading-relaxed">{selectedStep.recommendation}</p>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-12 text-slate-400 text-xs">
              Select a step to inspect observed details and evidence.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
