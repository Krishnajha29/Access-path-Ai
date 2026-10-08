import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { getAllTests } from '../api';
import { TestRecord } from '../types';
import { History, Play, Globe, ExternalLink, Loader2, Compass, AlertCircle, CheckCircle2, AlertTriangle, XCircle } from 'lucide-react';

export const HistoryPage: React.FC = () => {
  const navigate = useNavigate();
  const [tests, setTests] = useState<TestRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getAllTests()
      .then((data) => {
        setTests(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const getStatusBadge = (status?: string, score?: number) => {
    if (score !== undefined) {
      if (score >= 80) {
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200">
            <CheckCircle2 className="w-3 h-3" />
            <span>{score} / 100</span>
          </span>
        );
      }
      if (score >= 50) {
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 border border-amber-200">
            <AlertTriangle className="w-3 h-3" />
            <span>{score} / 100</span>
          </span>
        );
      }
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-100 text-rose-800 border border-rose-200">
          <XCircle className="w-3 h-3" />
          <span>{score} / 100</span>
        </span>
      );
    }

    return (
      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-700">
        <span>In Progress</span>
      </span>
    );
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <div>
          <span className="text-xs font-bold uppercase tracking-wider text-indigo-600">Audit Trail</span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-1">Previous Test Executions</h1>
          <p className="text-sm text-slate-500 mt-1">
            Review historical task simulation runs, scores, and verified user journeys.
          </p>
        </div>

        <Link
          to="/new-test"
          className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs shadow-sm transition flex items-center gap-2 self-start sm:self-auto"
        >
          <Play className="w-3.5 h-3.5 fill-white" />
          <span>New Test</span>
        </Link>
      </div>

      {loading ? (
        <div className="min-h-[40vh] flex flex-col items-center justify-center text-slate-500">
          <Loader2 className="w-8 h-8 animate-spin text-indigo-600 mb-3" />
          <span className="text-xs">Loading test history...</span>
        </div>
      ) : error ? (
        <div className="p-6 bg-rose-50 border border-rose-200 rounded-2xl text-rose-800 text-sm">
          Failed to load history: {error}
        </div>
      ) : tests.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center max-w-lg mx-auto shadow-sm">
          <div className="w-12 h-12 rounded-full bg-indigo-50 text-indigo-600 flex items-center justify-center mx-auto mb-4">
            <Compass className="w-6 h-6" />
          </div>
          <h3 className="font-bold text-base text-slate-900">No Tests Found</h3>
          <p className="text-xs text-slate-500 mt-1 mb-6 leading-relaxed">
            Run your first task-level usability simulation against a live site or our controlled demo portal.
          </p>
          <Link
            to="/new-test?demo=true"
            className="px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs transition inline-flex items-center gap-2"
          >
            <Play className="w-3.5 h-3.5 fill-white" />
            <span>Launch Scholarship Demo Test</span>
          </Link>
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-600">
              <thead className="bg-slate-50 border-b border-slate-200 text-[11px] font-bold text-slate-700 uppercase tracking-wider">
                <tr>
                  <th className="px-6 py-4">Target Website</th>
                  <th className="px-6 py-4">Task Intent</th>
                  <th className="px-6 py-4">User Persona</th>
                  <th className="px-6 py-4">Success Score</th>
                  <th className="px-6 py-4">Completion Status</th>
                  <th className="px-6 py-4">Date</th>
                  <th className="px-6 py-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-medium">
                {tests.map((t) => (
                  <tr key={t.id} className="hover:bg-slate-50/60 transition">
                    <td className="px-6 py-4 font-mono text-[11px] text-slate-800 max-w-[200px] truncate">
                      <div className="flex items-center gap-1.5 truncate">
                        <Globe className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                        <span className="truncate">{t.url}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-slate-900 max-w-[240px] truncate font-semibold">
                      {t.task}
                    </td>
                    <td className="px-6 py-4 text-slate-700">
                      <span className="px-2.5 py-1 rounded-md bg-slate-100 text-slate-800 text-[11px]">
                        {t.persona.name}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      {getStatusBadge(t.status, t.score)}
                    </td>
                    <td className="px-6 py-4 text-slate-600">
                      {t.completionStatus || t.status}
                    </td>
                    <td className="px-6 py-4 text-slate-400 font-mono text-[11px]">
                      {new Date(t.createdAt).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <button
                        onClick={() => navigate(`/results/${t.id}`)}
                        className="text-xs font-semibold text-indigo-600 hover:text-indigo-800 inline-flex items-center gap-1"
                      >
                        <span>Open Report</span>
                        <ExternalLink className="w-3 h-3" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
