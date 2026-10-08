import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getTest, subscribeToTestEvents } from '../api';
import { TestRecord } from '../types';
import { LiveBrowserView } from '../components/LiveBrowserView';
import { Globe, Users, ArrowRight, Loader2, CheckCircle2, AlertTriangle, ShieldCheck } from 'lucide-react';

const LIFECYCLE_STAGES = [
  'Agent started',
  'Agent running',
  'Agent analyzing page',
  'Agent completed',
  'Analyzing results',
  'Report ready'
];

export const LiveTestPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [test, setTest] = useState<TestRecord | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [currentAction, setCurrentAction] = useState<string>('Initializing live browser environment...');
  const [currentStageIndex, setCurrentStageIndex] = useState<number>(1);
  const [streamingUrl, setStreamingUrl] = useState<string | undefined>(undefined);

  useEffect(() => {
    if (!id) return;

    // Fetch initial test record
    getTest(id)
      .then((data) => {
        setTest(data);
        if (data.streamingUrl) setStreamingUrl(data.streamingUrl);
        if (data.status === 'completed') {
          setCurrentStageIndex(5);
        }
      })
      .catch((err) => setError(err.message));

    // Subscribe to live SSE events
    const unsubscribe = subscribeToTestEvents(
      id,
      (event) => {
        if (event.streamingUrl) {
          setStreamingUrl(event.streamingUrl);
          setCurrentStageIndex(2); // Agent running
        }
        if (event.purpose) {
          setCurrentAction(event.purpose);
          setCurrentStageIndex(2); // Agent analyzing page
        }
        if (event.type === 'COMPLETE') {
          setCurrentStageIndex(4); // Analyzing results
          setTimeout(() => {
            setCurrentStageIndex(5); // Report ready
            navigate(`/results/${id}`);
          }, 1200);
        }
        if (event.type === 'ERROR') {
          setError(event.error || 'Agent encountered an error during task execution.');
        }
      },
      (err) => {
        // SSE error, poll fallback
        getTest(id).then((t) => {
          if (t.status === 'completed') {
            navigate(`/results/${id}`);
          }
        });
      }
    );

    return () => {
      unsubscribe();
    };
  }, [id, navigate]);

  if (error) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-16 text-center">
        <div className="w-12 h-12 rounded-full bg-rose-100 text-rose-600 flex items-center justify-center mx-auto mb-4">
          <AlertTriangle className="w-6 h-6" />
        </div>
        <h2 className="text-xl font-bold text-slate-900">Task Simulation Notice</h2>
        <p className="text-sm text-slate-600 mt-2 max-w-md mx-auto">{error}</p>
        <button
          onClick={() => navigate('/new-test')}
          className="mt-6 px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-semibold shadow-sm transition"
        >
          Return to Test Configuration
        </button>
      </div>
    );
  }

  if (!test) {
    return (
      <div className="min-h-[50vh] flex flex-col items-center justify-center text-slate-500">
        <Loader2 className="w-8 h-8 animate-spin text-indigo-600 mb-3" />
        <span className="text-xs font-medium">Connecting to test harness...</span>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Configuration Header */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="space-y-1.5 flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-xs font-bold uppercase tracking-wider text-indigo-600">
              Live Test Execution Active
            </span>
          </div>
          <h1 className="text-xl font-extrabold text-slate-900 truncate">
            {test.task}
          </h1>
          <div className="flex flex-wrap items-center gap-4 text-xs text-slate-500 pt-1">
            <span className="flex items-center gap-1.5 font-mono">
              <Globe className="w-3.5 h-3.5 text-slate-400" />
              <span className="truncate max-w-xs">{test.url}</span>
            </span>
            <span className="flex items-center gap-1.5">
              <Users className="w-3.5 h-3.5 text-slate-400" />
              <span className="font-semibold text-slate-700">{test.persona.name}</span>
            </span>
          </div>
        </div>

        {currentStageIndex === 5 && (
          <button
            onClick={() => navigate(`/results/${test.id}`)}
            className="px-6 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs shadow-sm transition flex items-center gap-2 shrink-0 self-start md:self-auto"
          >
            <span>View Full Report</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        )}
      </div>

      {/* Lifecycle Progress Pipeline */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs">
        <div className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-4">
          Agent Execution Pipeline
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2">
          {LIFECYCLE_STAGES.map((stage, idx) => {
            const isPassed = idx < currentStageIndex;
            const isCurrent = idx === currentStageIndex;
            return (
              <div
                key={idx}
                className={`p-3 rounded-xl border text-xs flex flex-col justify-center transition-all ${
                  isCurrent
                    ? 'border-indigo-600 bg-indigo-50/70 text-indigo-900 font-bold ring-1 ring-indigo-500'
                    : isPassed
                    ? 'border-emerald-200 bg-emerald-50/50 text-emerald-900 font-medium'
                    : 'border-slate-200 bg-slate-50/40 text-slate-400'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-[10px] font-mono opacity-70">0{idx + 1}</span>
                  {isPassed ? (
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                  ) : isCurrent ? (
                    <Loader2 className="w-3.5 h-3.5 text-indigo-600 animate-spin" />
                  ) : null}
                </div>
                <span className="truncate">{stage}</span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Prominent Live Browser View Panel (Section 16) */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <span className="font-bold text-sm text-slate-900">Live Agent View</span>
            <span className="text-[11px] text-slate-500 font-medium">(Watch TinyFish interact with live web elements)</span>
          </div>
          <div className="flex items-center gap-1 text-xs text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Real Browser Sandbox</span>
          </div>
        </div>

        <LiveBrowserView
          streamingUrl={streamingUrl}
          targetUrl={test.url}
          currentAction={currentAction}
          status={LIFECYCLE_STAGES[currentStageIndex] || 'Agent running'}
        />
      </div>
    </div>
  );
};
