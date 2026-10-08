import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getTest, triggerRetest } from '../api';
import { TestRecord } from '../types';
import { ScoreCard } from '../components/ScoreCard';
import { JourneyTimeline } from '../components/JourneyTimeline';
import { BarrierCard } from '../components/BarrierCard';
import { EvidencePanel } from '../components/EvidencePanel';
import {
  RotateCcw,
  Sparkles,
  ArrowRight,
  User,
  CheckCircle2,
  AlertTriangle,
  Lightbulb,
  TrendingUp,
  Globe,
  Loader2,
  ExternalLink
} from 'lucide-react';

export const ResultsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [test, setTest] = useState<TestRecord | null>(null);
  const [previousTest, setPreviousTest] = useState<TestRecord | null>(null);
  const [retestLoading, setRetestLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    getTest(id)
      .then((data) => {
        setTest(data);
        if (data.retestedFromId) {
          getTest(data.retestedFromId).then(setPreviousTest).catch(() => {});
        }
      })
      .catch((err) => setError(err.message));
  }, [id]);

  const handleRetest = async () => {
    if (!test) return;
    try {
      setRetestLoading(true);
      const retestRecord = await triggerRetest(test.id);
      navigate(`/test/${retestRecord.id}`);
    } catch (err: any) {
      alert(`Could not start retest: ${err.message}`);
      setRetestLoading(false);
    }
  };

  if (error || !test) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-16 text-center">
        {error ? (
          <div className="text-rose-600 text-sm font-medium">{error}</div>
        ) : (
          <div className="flex flex-col items-center justify-center text-slate-500">
            <Loader2 className="w-8 h-8 animate-spin text-indigo-600 mb-3" />
            <span className="text-xs">Loading test report...</span>
          </div>
        )}
      </div>
    );
  }

  // Calculate comparison if retest
  const hasComparison = previousTest && previousTest.score !== undefined && test.score !== undefined;
  const scoreDelta = hasComparison ? test.score! - previousTest.score! : 0;

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-10">
      {/* Top Breadcrumb & Actions Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <div className="flex items-center gap-2 text-xs text-slate-500">
            <Link to="/history" className="hover:text-slate-800 transition">Test History</Link>
            <span>/</span>
            <span className="font-mono text-slate-600">{test.id}</span>
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900 mt-1">
            Task-Level Usability &amp; Accessibility Report
          </h1>
          <div className="flex flex-wrap items-center gap-3 text-xs text-slate-500 mt-1 font-mono">
            <span className="flex items-center gap-1">
              <Globe className="w-3.5 h-3.5 text-slate-400" />
              <span>{test.url}</span>
            </span>
            <span className="text-slate-300">&bull;</span>
            <span>Tested on {new Date(test.createdAt).toLocaleDateString()}</span>
          </div>
        </div>

        {/* Retest CTA Button */}
        <div className="flex items-center gap-3 self-start sm:self-auto">
          <button
            onClick={handleRetest}
            disabled={retestLoading}
            className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 text-white font-semibold text-xs shadow-sm transition flex items-center gap-2"
          >
            {retestLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <RotateCcw className="w-4 h-4" />
            )}
            <span>Re-test After Fix</span>
          </button>
        </div>
      </div>

      {/* Retest Comparison Banner (Section 26 & 34) */}
      {hasComparison ? (
        <div className="bg-gradient-to-r from-emerald-500 to-teal-600 text-white rounded-2xl p-6 shadow-sm flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="space-y-1 text-center md:text-left">
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/20 text-xs font-bold uppercase tracking-wider backdrop-blur-xs">
              <TrendingUp className="w-3.5 h-3.5" />
              <span>Verified Retest Improvement</span>
            </div>
            <h3 className="text-xl font-bold">
              Task Feasibility Score Increased by +{scoreDelta} Points!
            </h3>
            <p className="text-xs text-emerald-100 max-w-xl">
              User journey retested with identical goal and persona constraints following interface improvements.
            </p>
          </div>

          <div className="flex items-center gap-4 bg-white/10 p-4 rounded-xl border border-white/20 backdrop-blur-xs">
            <div className="text-center px-4 border-r border-white/20">
              <div className="text-[10px] uppercase font-semibold text-emerald-200">Before Fix</div>
              <div className="text-2xl font-bold font-mono">{previousTest.score} / 100</div>
            </div>
            <div className="text-center px-4">
              <div className="text-[10px] uppercase font-semibold text-emerald-200">After Fix</div>
              <div className="text-2xl font-bold font-mono text-emerald-200">{test.score} / 100</div>
            </div>
            <div className="text-center px-3 bg-white text-emerald-800 rounded-lg py-2 font-bold text-sm shadow-xs">
              +{scoreDelta}
            </div>
          </div>
        </div>
      ) : (
        <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 text-xs text-slate-600 flex items-center justify-between">
          <span className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-indigo-600" />
            <span>Make improvements to the website, then click <strong>&ldquo;Re-test After Fix&rdquo;</strong> to generate a before/after comparison.</span>
          </span>
        </div>
      )}

      {/* Section 1: Main Task Success Score Card */}
      <ScoreCard test={test} />

      {/* Section 2: Persona Insight Panel (Section 24) */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-8 h-8 rounded-lg bg-indigo-50 text-indigo-700 flex items-center justify-center">
            <User className="w-4 h-4" />
          </div>
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Tested Persona Profile</span>
            <h3 className="text-base font-bold text-slate-900">{test.persona.name}</h3>
          </div>
        </div>

        <p className="text-xs text-slate-600 leading-relaxed max-w-3xl">
          {test.personaInsights?.evaluationFocus || `This test evaluates whether a ${test.persona.name.toLowerCase()} can complete the workflow without outside guidance.`}
        </p>

        {test.personaInsights?.personaBarriers && test.personaInsights.personaBarriers.length > 0 && (
          <div className="mt-4 pt-4 border-t border-slate-100">
            <span className="text-[11px] font-bold text-slate-700 uppercase tracking-wider block mb-2">
              Persona-Specific Vulnerabilities Observed:
            </span>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {test.personaInsights.personaBarriers.map((pb, i) => (
                <div key={i} className="text-xs bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-slate-700 flex items-start gap-2">
                  <span className="text-amber-500 font-bold">&bull;</span>
                  <span>{pb}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Section 3: User Journey Timeline (Section 20) */}
      <JourneyTimeline steps={test.steps} />

      {/* Section 4: Evidence-First Barrier Diagnostics (Section 23) */}
      <EvidencePanel barriers={test.barriers} />

      {/* Section 5: Concrete Fix Recommendations (Section 25) */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 shadow-sm">
        <div className="flex items-center gap-2 mb-2">
          <Lightbulb className="w-5 h-5 text-indigo-600" />
          <h3 className="text-lg font-bold text-slate-900">Recommended Concrete Improvements</h3>
        </div>
        <p className="text-xs text-slate-500 mb-6">
          Actionable engineering and UX fixes prioritized by severity to unblock user journeys.
        </p>

        {test.barriers.length > 0 ? (
          <div className="space-y-3">
            {test.barriers.map((barrier, idx) => (
              <div key={idx} className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 flex items-start gap-4">
                <span className="w-7 h-7 rounded-lg bg-indigo-600 text-white font-bold text-xs flex items-center justify-center shrink-0">
                  {String(idx + 1).padStart(2, '0')}
                </span>
                <div className="flex-1 text-xs">
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-bold text-sm text-slate-900">{barrier.title}</span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-semibold uppercase bg-amber-100 text-amber-800 border border-amber-200">
                      {barrier.severity}
                    </span>
                  </div>
                  <p className="text-slate-700 font-medium mt-1 leading-relaxed">
                    {barrier.recommendation || 'Clarify instructions and improve interaction cues.'}
                  </p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-800">
            All user steps passed without actionable recommendations required.
          </div>
        )}
      </div>

      {/* Section 6: Barrier Detail Classifications (Section 21-22) */}
      {test.barriers.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-bold text-slate-900">Comprehensive Barrier Breakdown</h3>
            <span className="text-xs text-slate-500">{test.barriers.length} barriers identified</span>
          </div>
          <div className="space-y-3">
            {test.barriers.map((barrier, idx) => (
              <BarrierCard key={idx} barrier={barrier} index={idx} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
