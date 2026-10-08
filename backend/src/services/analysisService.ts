import { Barrier, Persona } from '../types.js';

export interface PersonaAnalysisInsight {
  personaName: string;
  evaluationFocus: string;
  personaBarriers: string[];
}

export function generatePersonaInsights(persona: Persona, barriers: Barrier[]): PersonaAnalysisInsight {
  const personaBarriers: string[] = [];

  switch (persona.id) {
    case 'first-time-user':
      personaBarriers.push(
        'Unclear next action requires external guidance or trial-and-error',
        'Confusing terminology and acronyms reduce user confidence',
        'Lack of upfront requirement checklist causes unexpected drop-offs'
      );
      break;
    case 'mobile-first-user':
      personaBarriers.push(
        'Tap targets too close to each other cause accidental clicks',
        'Complex multi-column tables require horizontal scrolling',
        'File uploads fail without mobile-friendly camera or gallery pickers'
      );
      break;
    case 'hindi-speaking-student':
      personaBarriers.push(
        'Dense bureaucratic English vocabulary lacks Hindi/regional language translation',
        'Legalistic instructions obscure essential eligibility thresholds',
        'Error messages in cryptic technical English hinder self-recovery'
      );
      break;
    case 'low-digital-literacy':
      personaBarriers.push(
        'Hidden interactive triggers (e.g. unstyled collapsibles) are missed',
        'Unclear distinction between secondary "Reset" action and primary "Submit"',
        'Cryptic validation warnings leave user stuck on forms'
      );
      break;
    case 'screen-reader-user':
      personaBarriers.push(
        'Unlabeled form fields prevent speech synthesizer from announcing inputs',
        'Missing ARIA live regions mean status changes are not verbalized',
        'Non-semantic button tags and low-contrast indicators fail accessibility trees'
      );
      break;
    default:
      personaBarriers.push('General task flow impediment detected');
  }

  // Filter or augment with actual observed barriers
  for (const b of barriers) {
    if (!personaBarriers.includes(b.title)) {
      personaBarriers.push(`${b.type}: ${b.title}`);
    }
  }

  return {
    personaName: persona.name,
    evaluationFocus: `This test evaluates whether a ${persona.description.toLowerCase()} can complete the workflow without outside guidance.`,
    personaBarriers: personaBarriers.slice(0, 4)
  };
}

export function enrichBarriersWithImpact(barriers: Barrier[], persona: Persona): Barrier[] {
  return barriers.map(b => {
    let impact = b.description;
    if (b.type === 'Form Usability') {
      impact = `A ${persona.name} may become confused or enter invalid data, risking form submission failure.`;
    } else if (b.type === 'Navigation' || b.type === 'Dead End') {
      impact = `A ${persona.name} cannot easily locate the next forward step, leading to high frustration and task abandonment.`;
    } else if (b.type === 'Language') {
      impact = `Important information remains incomprehensible to users without specialized institutional knowledge or English fluency.`;
    } else if (b.type === 'Accessibility') {
      impact = `Assistive technology users will not be able to identify or interact with this control.`;
    }

    return {
      ...b,
      userImpact: impact
    };
  });
}
