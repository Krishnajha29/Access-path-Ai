import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Compass, Play, History, Sparkles, CheckCircle2 } from 'lucide-react';

export const Navbar: React.FC = () => {
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <Link to="/" className="flex items-center space-x-3 group">
          <div className="w-9 h-9 rounded-lg bg-indigo-600 group-hover:bg-indigo-700 flex items-center justify-center text-white shadow-sm transition">
            <Compass className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-lg text-slate-900 tracking-tight">AccessPath</span>
              <span className="text-xs bg-indigo-100 text-indigo-700 font-semibold px-2 py-0.5 rounded-full border border-indigo-200">AI</span>
            </div>
            <p className="text-[10px] text-slate-500 hidden sm:block">Task-Level Accessibility & Usability</p>
          </div>
        </Link>

        {/* Navigation Links */}
        <nav className="flex items-center space-x-1 sm:space-x-3">
          <Link
            to="/new-test"
            className={`px-3 py-2 rounded-lg text-sm font-medium transition flex items-center space-x-1.5 ${
              isActive('/new-test')
                ? 'bg-indigo-50 text-indigo-700'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
            }`}
          >
            <Play className="w-4 h-4" />
            <span>New Test</span>
          </Link>

          <Link
            to="/history"
            className={`px-3 py-2 rounded-lg text-sm font-medium transition flex items-center space-x-1.5 ${
              isActive('/history')
                ? 'bg-indigo-50 text-indigo-700'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
            }`}
          >
            <History className="w-4 h-4" />
            <span>History</span>
          </Link>

          <div className="h-5 w-px bg-slate-200 mx-1 hidden sm:block" />

          {/* TinyFish Agent Connection Badge */}
          <div className="hidden md:flex items-center space-x-1.5 text-xs text-emerald-800 bg-emerald-50 border border-emerald-200 px-2.5 py-1 rounded-full">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
            <span className="font-medium">TinyFish Agent Active</span>
          </div>

          <Link
            to="/new-test?demo=true"
            className="inline-flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-xs sm:text-sm font-medium shadow-sm transition"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Try Demo</span>
          </Link>
        </nav>
      </div>
    </header>
  );
};
