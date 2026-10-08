import React from 'react';
import { Persona } from '../types';
import { User, Smartphone, Languages, Accessibility, Eye, Check } from 'lucide-react';

interface PersonaCardProps {
  persona: Persona;
  isSelected: boolean;
  onSelect: (persona: Persona) => void;
}

export const PersonaCard: React.FC<PersonaCardProps> = ({
  persona,
  isSelected,
  onSelect
}) => {
  const getIcon = () => {
    switch (persona.id) {
      case 'first-time-user':
        return <User className="w-5 h-5 text-indigo-600" />;
      case 'mobile-first-user':
        return <Smartphone className="w-5 h-5 text-sky-600" />;
      case 'hindi-speaking-student':
        return <Languages className="w-5 h-5 text-emerald-600" />;
      case 'low-digital-literacy':
        return <Accessibility className="w-5 h-5 text-amber-600" />;
      case 'screen-reader-user':
        return <Eye className="w-5 h-5 text-purple-600" />;
      default:
        return <User className="w-5 h-5 text-indigo-600" />;
    }
  };

  return (
    <div
      onClick={() => onSelect(persona)}
      className={`relative p-5 rounded-xl border-2 cursor-pointer transition-all ${
        isSelected
          ? 'border-indigo-600 bg-indigo-50/40 shadow-sm ring-1 ring-indigo-500'
          : 'border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50/50'
      }`}
    >
      <div className="flex items-start justify-between gap-3 mb-2">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-slate-100 flex items-center justify-center shrink-0">
            {getIcon()}
          </div>
          <div>
            <h4 className="font-bold text-sm text-slate-900">{persona.name}</h4>
            <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider">
              {persona.badge}
            </span>
          </div>
        </div>

        {isSelected && (
          <div className="w-5 h-5 rounded-full bg-indigo-600 flex items-center justify-center text-white shrink-0">
            <Check className="w-3.5 h-3.5" />
          </div>
        )}
      </div>

      <p className="text-xs text-slate-600 mb-3 leading-relaxed">
        {persona.description}
      </p>

      <div className="pt-2 border-t border-slate-100 space-y-1">
        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
          Key Constraints:
        </span>
        <ul className="text-[11px] text-slate-500 space-y-0.5 list-disc list-inside">
          {persona.constraints.slice(0, 2).map((c, i) => (
            <li key={i} className="truncate">{c}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};
