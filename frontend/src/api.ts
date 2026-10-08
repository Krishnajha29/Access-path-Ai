import { Persona, TestRecord } from './types';

const API_BASE = 'http://localhost:5000/api';

export async function createTest(params: {
  url: string;
  task: string;
  persona: Persona;
  isImprovedDemo?: boolean;
}): Promise<TestRecord> {
  const res = await fetch(`${API_BASE}/tests`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params)
  });

  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.error || `Failed to create test (${res.status})`);
  }

  return res.json();
}

export async function getTest(id: string): Promise<TestRecord> {
  const res = await fetch(`${API_BASE}/tests/${id}`);
  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.error || `Failed to fetch test details (${res.status})`);
  }
  return res.json();
}

export async function getAllTests(): Promise<TestRecord[]> {
  const res = await fetch(`${API_BASE}/tests`);
  if (!res.ok) {
    throw new Error(`Failed to fetch tests list (${res.status})`);
  }
  return res.json();
}

export async function triggerRetest(id: string): Promise<TestRecord> {
  const res = await fetch(`${API_BASE}/tests/${id}/retest`, {
    method: 'POST'
  });
  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.error || `Failed to trigger retest (${res.status})`);
  }
  return res.json();
}

export function subscribeToTestEvents(
  testId: string,
  onEvent: (event: any) => void,
  onError?: (err: any) => void
): () => void {
  const eventSource = new EventSource(`${API_BASE}/tests/${testId}/events`);

  eventSource.onmessage = (e) => {
    try {
      const data = JSON.parse(e.data);
      onEvent(data);
    } catch (err) {
      // ignore
    }
  };

  eventSource.onerror = (err) => {
    onError?.(err);
  };

  return () => {
    eventSource.close();
  };
}
