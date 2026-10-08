import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Compass, Play, Sparkles, CheckCircle2, ArrowRight, ShieldCheck, UserCheck, Layers, AlertTriangle } from 'lucide-react';

export const LandingPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col min-h-[calc(100vh-4rem)]">
      {/* Hero Section */}
      <section className="pt-16 pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full text-center">
        {/* Hackathon Badge */}
        <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-indigo-50 border border-indigo-200 text-indigo-700 text-xs font-semibold mb-6">
          <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
          <span>HackIIITD 2026 Innovation &bull; Task-Level Accessibility Simulator</span>
        </div>

        {/* Hero Title */}
        <h1 className="text-4xl sm:text-6xl font-extrabold text-slate-900 tracking-tight max-w-4xl mx-auto leading-tight">
          Can a real person <span className="text-indigo-600 underline decoration-indigo-300 decoration-wavy underline-offset-8">actually complete</span> the task?
        </h1>

        {/* Tagline & Supporting Text */}
        <p className="text-lg sm:text-xl text-slate-600 mt-6 max-w-2xl mx-auto leading-relaxed font-normal">
          Don&rsquo;t just test website code. AccessPath AI uses a live browser agent to test real user journeys, identify where people get stuck, and turn those failures into actionable improvements.
        </p>

        {/* Action Buttons */}
        <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link
            to="/new-test"
            className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-base shadow-sm hover:shadow transition flex items-center justify-center space-x-2"
          >
            <Play className="w-4 h-4 fill-white" />
            <span>Start a Test</span>
          </Link>

          <Link
            to="/new-test?demo=true"
            className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-white hover:bg-slate-50 text-slate-800 font-semibold text-base border border-slate-300 shadow-xs transition flex items-center justify-center space-x-2"
          >
            <Sparkles className="w-4 h-4 text-indigo-600" />
            <span>Try Demo (Scholarship Portal)</span>
          </Link>
        </div>

        {/* Clean Process Flow Visual (Specified in Section 8) */}
        <div className="mt-16 pt-12 border-t border-slate-200">
          <div className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-8">
            The AccessPath Task-Level Validation Pipeline
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3 max-w-6xl mx-auto">
            {[
              { title: 'Website URL', sub: 'Target Site', color: 'border-slate-200 bg-white' },
              { title: 'Task Intent', sub: 'Specific Goal', color: 'border-slate-200 bg-white' },
              { title: 'User Persona', sub: 'Real Constraints', color: 'border-indigo-200 bg-indigo-50/50 text-indigo-900' },
              { title: 'AI Browser Agent', sub: 'TinyFish Live Web', color: 'border-indigo-500 bg-indigo-600 text-white font-bold' },
              { title: 'Task Journey', sub: 'Step-by-Step Path', color: 'border-slate-200 bg-white' },
              { title: 'Barrier Detection', sub: '8 Classifications', color: 'border-amber-200 bg-amber-50/50 text-amber-900' },
              { title: 'Actionable Report', sub: 'Evidence + Score', color: 'border-emerald-200 bg-emerald-50/50 text-emerald-900' }
            ].map((node, i) => (
              <div key={i} className={`p-4 rounded-xl border flex flex-col justify-center items-center shadow-xs ${node.color}`}>
                <div className="text-xs font-bold">{node.title}</div>
                <div className="text-[11px] opacity-75 mt-0.5">{node.sub}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Philosophy Section: Why Task-Level vs Traditional Checkers */}
      <section className="bg-white border-y border-slate-200 py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <span className="text-xs font-bold uppercase tracking-wider text-indigo-600">Product Philosophy</span>
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 mt-1">
              Why Traditional Accessibility Scanners Fall Short
            </h2>
            <p className="text-sm text-slate-500 mt-2">
              A website can technically score 100% on automated DOM linters and still be impossible for a citizen or student to use.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {/* Traditional Scanner Card */}
            <div className="p-6 rounded-2xl border border-slate-200 bg-slate-50/50">
              <div className="flex items-center space-x-2 text-rose-600 font-bold text-sm mb-3">
                <AlertTriangle className="w-4 h-4" />
                <span>Traditional Code / DOM Scanners</span>
              </div>
              <ul className="space-y-3 text-xs text-slate-600">
                <li className="flex items-start gap-2">
                  <span className="text-rose-500 font-bold">&times;</span>
                  <span>Inspects isolated HTML tags, color contrast formulas, and alt attributes.</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-rose-500 font-bold">&times;</span>
                  <span>Cannot tell if an instruction is confusing or full of legal jargon.</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-rose-500 font-bold">&times;</span>
                  <span>Never navigates across multiple pages to see if the user gets stuck on hidden accordions or confusing forms.</span>
                </li>
              </ul>
            </div>

            {/* AccessPath AI Card */}
            <div className="p-6 rounded-2xl border-2 border-indigo-500 bg-indigo-50/20 shadow-xs">
              <div className="flex items-center space-x-2 text-indigo-700 font-bold text-sm mb-3">
                <CheckCircle2 className="w-4 h-4 text-indigo-600" />
                <span>AccessPath AI (Task Simulator + AI Browser Agent)</span>
              </div>
              <ul className="space-y-3 text-xs text-slate-700">
                <li className="flex items-start gap-2">
                  <span className="text-emerald-600 font-bold">&check;</span>
                  <span><strong>Attempts real user goals:</strong> &ldquo;Apply for scholarship and verify required files&rdquo;.</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-600 font-bold">&check;</span>
                  <span><strong>Applies persona cognitive constraints:</strong> First-Time User, Hindi-Speaking, Screen-Reader, Low-Digital-Literacy.</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-600 font-bold">&check;</span>
                  <span><strong>Generates transparent score &amp; concrete fixes:</strong> Transparent deductions and before/after re-testing.</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto text-center w-full">
        <div className="bg-gradient-to-br from-indigo-900 to-slate-900 text-white rounded-3xl p-8 sm:p-12 shadow-md">
          <h3 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            Ready to test live task feasibility?
          </h3>
          <p className="text-sm text-indigo-200 mt-2 max-w-xl mx-auto">
            Experience how the TinyFish Web Agent navigates a real multi-page workflow and highlights barriers.
          </p>
          <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              to="/new-test?demo=true"
              className="w-full sm:w-auto px-7 py-3 rounded-xl bg-white text-indigo-900 font-bold text-sm hover:bg-indigo-50 transition"
            >
              Run Instant Fellowship Demo
            </Link>
            <Link
              to="/new-test"
              className="w-full sm:w-auto px-7 py-3 rounded-xl bg-indigo-800/80 hover:bg-indigo-800 text-white font-medium text-sm border border-indigo-700 transition"
            >
              Test Custom URL
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};
