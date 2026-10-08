import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { PRESET_PERSONAS, Persona } from '../types';
import { PersonaCard } from '../components/PersonaCard';
import { createTest } from '../api';
import { Globe, FileText, Users, Play, Sparkles, AlertCircle, ArrowRight } from 'lucide-react';

const SUGGESTED_TASKS = [
  'Apply for a scholarship and identify everything required before starting the application.',
  'Find the scholarship application steps and prerequisite criteria.',
  'Find the admission registration process and start candidate profile.',
  'Locate the contact/support workflow and grievance submission.',
  'Find how to upload the required income verification document.'
];

export const CreateTestPage: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const [url, setUrl] = useState('');
  const [task, setTask] = useState('');
  const [selectedPersona, setSelectedPersona] = useState<Persona>(PRESET_PERSONAS[0]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // Demo auto-populate trigger
  const handlePopulateDemo = (improved = false) => {
    setUrl(improved ? 'http://localhost:5000/demo-site/index.html?improved=true' : 'http://localhost:5000/demo-site/index.html');
    setTask('Apply for a scholarship and identify everything required before starting the application.');
    setSelectedPersona(PRESET_PERSONAS[0]); // First-Time User
    setError(null);
  };

  useEffect(() => {
    if (searchParams.get('demo') === 'true') {
      handlePopulateDemo();
    }
  }, [searchParams]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!url.trim()) {
      setError('Please provide a target website URL to test.');
      return;
    }

    // Basic URL validation
    try {
      new URL(url.trim());
    } catch {
      setError('Please provide a valid URL (including http:// or https://).');
      return;
    }

    if (!task.trim()) {
      setError('Please describe the specific user task to test.');
      return;
    }

    try {
      setLoading(true);
      const isImprovedDemo = url.includes('improved=true');
      const test = await createTest({
        url: url.trim(),
        task: task.trim(),
        persona: selectedPersona,
        isImprovedDemo
      });

      navigate(`/test/${test.id}`);
    } catch (err: any) {
      setError(err.message || 'Failed to initialize test.');
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <div>
          <span className="text-xs font-bold uppercase tracking-wider text-indigo-600">Configuration</span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-1">Create a New Test</h1>
          <p className="text-sm text-slate-500 mt-1">
            Specify a target website, user goal, and persona to evaluate real task feasibility.
          </p>
        </div>

        {/* Demo Fast-fill button */}
        <button
          type="button"
          onClick={() => handlePopulateDemo()}
          className="inline-flex items-center space-x-2 px-4 py-2 rounded-xl bg-amber-50 hover:bg-amber-100 border border-amber-200 text-amber-900 font-semibold text-xs transition shadow-xs self-start sm:self-auto"
        >
          <Sparkles className="w-4 h-4 text-amber-600" />
          <span>Auto-Fill Controlled Demo</span>
        </button>
      </div>

      {error && (
        <div className="mb-6 p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-sm flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
          <div>
            <div className="font-bold">Invalid Configuration</div>
            <p className="text-xs mt-0.5">{error}</p>
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-8 bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-sm">
        {/* Field 1: Website URL */}
        <div>
          <label htmlFor="url" className="block text-sm font-bold text-slate-900 mb-1 flex items-center gap-2">
            <Globe className="w-4 h-4 text-indigo-600" />
            <span>Target Website URL</span>
          </label>
          <p className="text-xs text-slate-500 mb-2">
            The live website URL the TinyFish browser agent will navigate and test.
          </p>
          <input
            id="url"
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.gov.in/fellowship or http://localhost:5000/demo-site/index.html"
            className="w-full px-4 py-3 rounded-xl border border-slate-300 focus:border-indigo-600 focus:ring-2 focus:ring-indigo-100 text-sm font-mono text-slate-800 transition"
          />
        </div>

        {/* Field 2: Task */}
        <div>
          <label htmlFor="task" className="block text-sm font-bold text-slate-900 mb-1 flex items-center gap-2">
            <FileText className="w-4 h-4 text-indigo-600" />
            <span>User Task to Perform</span>
          </label>
          <p className="text-xs text-slate-500 mb-2">
            Describe the concrete goal a real human is trying to accomplish.
          </p>
          <textarea
            id="task"
            rows={3}
            value={task}
            onChange={(e) => setTask(e.target.value)}
            placeholder="e.g. Find the scholarship application page and identify the steps required to begin the application."
            className="w-full px-4 py-3 rounded-xl border border-slate-300 focus:border-indigo-600 focus:ring-2 focus:ring-indigo-100 text-sm text-slate-800 transition leading-relaxed"
          />

          {/* Quick task suggestions */}
          <div className="mt-3">
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-2">
              Suggested Example Tasks:
            </span>
            <div className="flex flex-wrap gap-2">
              {SUGGESTED_TASKS.map((t, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => setTask(t)}
                  className="text-xs bg-slate-50 hover:bg-indigo-50 hover:text-indigo-700 text-slate-600 px-3 py-1.5 rounded-lg border border-slate-200 transition text-left"
                >
                  + {t}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Field 3: User Persona Selection */}
        <div>
          <label className="block text-sm font-bold text-slate-900 mb-1 flex items-center gap-2">
            <Users className="w-4 h-4 text-indigo-600" />
            <span>Select User Persona</span>
          </label>
          <p className="text-xs text-slate-500 mb-4">
            The agent will adopt this persona&rsquo;s cognitive constraints, literacy level, and navigation habits.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {PRESET_PERSONAS.map((persona) => (
              <PersonaCard
                key={persona.id}
                persona={persona}
                isSelected={selectedPersona.id === persona.id}
                onSelect={(p) => setSelectedPersona(p)}
              />
            ))}
          </div>
        </div>

        {/* Form Actions */}
        <div className="pt-6 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="text-xs text-slate-500">
            Engine: <span className="font-semibold text-slate-700">TinyFish Web Agent</span> &bull; Safe test mode
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full sm:w-auto px-8 py-3.5 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 text-white font-semibold rounded-xl shadow-sm transition flex items-center justify-center space-x-2 text-sm"
          >
            {loading ? (
              <span>Initializing Live Agent...</span>
            ) : (
              <>
                <span>Start Task Simulation</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};
