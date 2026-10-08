import React from 'react';
import { ExternalLink, Globe, Radio, Shield, Eye } from 'lucide-react';

interface LiveBrowserViewProps {
  streamingUrl?: string;
  targetUrl: string;
  currentAction?: string;
  status: string;
}

export const LiveBrowserView: React.FC<LiveBrowserViewProps> = ({
  streamingUrl,
  targetUrl,
  currentAction,
  status
}) => {
  return (
    <div className="bg-slate-900 text-white rounded-2xl shadow-lg border border-slate-800 overflow-hidden">
      {/* Browser Chrome Header */}
      <div className="bg-slate-950 px-4 py-3 flex items-center justify-between border-b border-slate-800 text-xs">
        <div className="flex items-center space-x-2">
          <div className="flex space-x-1.5">
            <div className="w-3 h-3 rounded-full bg-rose-500/80" />
            <div className="w-3 h-3 rounded-full bg-amber-500/80" />
            <div className="w-3 h-3 rounded-full bg-emerald-500/80" />
          </div>
          <span className="text-slate-400 font-mono text-[11px] ml-2 flex items-center gap-1.5">
            <Radio className="w-3 h-3 text-emerald-400 animate-pulse" />
            <span>Live Agent View</span>
          </span>
        </div>

        {/* Address bar mockup */}
        <div className="flex-1 max-w-md mx-4 hidden sm:flex items-center bg-slate-900 px-3 py-1 rounded-md border border-slate-800 text-slate-300 font-mono text-[11px] truncate">
          <Globe className="w-3.5 h-3.5 text-slate-500 mr-2 shrink-0" />
          <span className="truncate">{targetUrl}</span>
        </div>

        {/* Action Link */}
        <div>
          {streamingUrl && (
            <a
              href={streamingUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center space-x-1 px-2.5 py-1 rounded bg-indigo-600 hover:bg-indigo-500 text-white text-[11px] font-medium transition"
            >
              <span>Popout Window</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          )}
        </div>
      </div>

      {/* Main View Area */}
      <div className="relative min-h-[380px] max-h-[520px] bg-slate-950 flex flex-col justify-center items-center">
        {streamingUrl ? (
          <iframe
            src={streamingUrl}
            title="Live Agent Browser View"
            className="w-full h-[460px] border-0 bg-white"
            sandbox="allow-scripts allow-same-origin allow-forms"
          />
        ) : (
          <div className="text-center p-8 max-w-md">
            <div className="w-14 h-14 rounded-2xl bg-indigo-900/50 border border-indigo-700/50 flex items-center justify-center mx-auto mb-4 text-indigo-400">
              <Eye className="w-7 h-7" />
            </div>
            <h4 className="font-bold text-base text-slate-200">TinyFish Agent Active</h4>
            <p className="text-xs text-slate-400 mt-2 leading-relaxed">
              The live agent is inspecting page layout, interactive controls, and document requirements.
            </p>
            <div className="mt-4 inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-800 border border-slate-700 text-xs text-indigo-300 font-mono">
              <span className="w-2 h-2 rounded-full bg-indigo-400 animate-ping" />
              <span>Status: {status}</span>
            </div>
          </div>
        )}

        {/* Current Agent Action Ticker */}
        {currentAction && (
          <div className="w-full bg-slate-900/90 border-t border-slate-800 px-4 py-2.5 flex items-center gap-2 text-xs text-slate-300">
            <span className="font-semibold text-indigo-400 shrink-0">Current Action:</span>
            <span className="font-mono text-slate-200 truncate">{currentAction}</span>
          </div>
        )}
      </div>

      {/* Safety Notice footer */}
      <div className="bg-slate-950 px-4 py-2 border-t border-slate-900 flex items-center justify-between text-[10px] text-slate-500">
        <span className="flex items-center gap-1">
          <Shield className="w-3 h-3 text-emerald-500" />
          <span>Non-destructive test mode active: Real submissions & logins withheld</span>
        </span>
        <span className="font-mono">Engine: TinyFish Web Agent</span>
      </div>
    </div>
  );
};
