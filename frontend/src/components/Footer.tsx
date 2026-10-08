import React from 'react';
import { Compass, ShieldCheck } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-white border-t border-slate-200 mt-auto py-8 text-slate-500 text-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center space-x-2">
          <div className="w-6 h-6 rounded bg-indigo-600 flex items-center justify-center text-white text-xs">
            <Compass className="w-3.5 h-3.5" />
          </div>
          <span className="font-semibold text-slate-800">AccessPath AI</span>
          <span>&mdash; National Hackathon Edition</span>
        </div>

        <div className="flex items-center space-x-2 text-slate-500">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          <span>Execution Engine: TinyFish Web Agent &bull; Non-destructive test observer mode</span>
        </div>

        <div className="text-slate-400">
          &ldquo;Don&rsquo;t just test a website. Test whether a real person can actually complete the task.&rdquo;
        </div>
      </div>
    </footer>
  );
};
