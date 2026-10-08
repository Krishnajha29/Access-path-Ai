import { Router, Request, Response } from 'express';
import { randomUUID } from 'crypto';
import { Persona, TestRecord } from '../types.js';
import { dbService } from '../db/database.js';
import { tinyfishService, TinyFishRunEvent } from '../services/tinyfishService.js';
import { calculateTaskSuccessScore } from '../services/scoreService.js';
import { enrichBarriersWithImpact, generatePersonaInsights } from '../services/analysisService.js';

const router = Router();

// Store active SSE subscriber response objects by testId
const activeEventClients: Map<string, Response[]> = new Map();

function broadcastEvent(testId: string, event: TinyFishRunEvent) {
  const clients = activeEventClients.get(testId) || [];
  const payload = `data: ${JSON.stringify(event)}\n\n`;
  for (const res of clients) {
    try {
      res.write(payload);
    } catch (err) {
      // client disconnected
    }
  }
}

// POST /api/tests
router.post('/', async (req: Request, res: Response) => {
  try {
    const { url, task, persona, isImprovedDemo } = req.body;

    if (!url || typeof url !== 'string') {
      return res.status(400).json({ error: 'Valid website URL is required.' });
    }
    if (!task || typeof task !== 'string') {
      return res.status(400).json({ error: 'Task description is required.' });
    }
    if (!persona || !persona.id || !persona.name) {
      return res.status(400).json({ error: 'User persona selection is required.' });
    }

    const testId = `test-${Date.now().toString(36)}-${Math.random().toString(36).substring(2, 7)}`;
    const now = new Date().toISOString();

    const newTest: TestRecord = {
      id: testId,
      url: url.trim(),
      task: task.trim(),
      persona: persona as Persona,
      status: 'running',
      steps: [],
      barriers: [],
      createdAt: now,
      updatedAt: now,
      isImprovedDemo: Boolean(isImprovedDemo)
    };

    dbService.createTest(newTest);

    // Launch TinyFish execution asynchronously in background
    runTestAsync(newTest);

    return res.status(201).json(newTest);
  } catch (err: any) {
    return res.status(500).json({ error: err.message || 'Failed to initialize test.' });
  }
});

// GET /api/tests
router.get('/', (req: Request, res: Response) => {
  try {
    const tests = dbService.getAllTests();
    return res.json(tests);
  } catch (err: any) {
    return res.status(500).json({ error: err.message || 'Failed to list tests.' });
  }
});

// GET /api/tests/:id
router.get('/:id', (req: Request, res: Response) => {
  try {
    const test = dbService.getTest(req.params.id);
    if (!test) {
      return res.status(404).json({ error: 'Test not found.' });
    }

    const personaInsights = generatePersonaInsights(test.persona, test.barriers);
    return res.json({
      ...test,
      personaInsights
    });
  } catch (err: any) {
    return res.status(500).json({ error: err.message || 'Failed to retrieve test.' });
  }
});

// GET /api/tests/:id/events (Server-Sent Events for live execution & browser preview)
router.get('/:id/events', (req: Request, res: Response) => {
  const testId = req.params.id;
  const test = dbService.getTest(testId);
  if (!test) {
    return res.status(404).json({ error: 'Test not found' });
  }

  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.flushHeaders();

  if (!activeEventClients.has(testId)) {
    activeEventClients.set(testId, []);
  }
  activeEventClients.get(testId)!.push(res);

  // Send initial snapshot
  const initialEvent: TinyFishRunEvent = {
    type: test.status === 'completed' ? 'COMPLETE' : 'STARTED',
    testId,
    streamingUrl: test.streamingUrl,
    purpose: test.status === 'completed' ? 'Report ready' : 'Agent running...'
  };
  res.write(`data: ${JSON.stringify(initialEvent)}\n\n`);

  req.on('close', () => {
    const clients = activeEventClients.get(testId) || [];
    const filtered = clients.filter(c => c !== res);
    if (filtered.length === 0) {
      activeEventClients.delete(testId);
    } else {
      activeEventClients.set(testId, filtered);
    }
  });
});

// POST /api/tests/:id/retest
router.post('/:id/retest', async (req: Request, res: Response) => {
  try {
    const originalTest = dbService.getTest(req.params.id);
    if (!originalTest) {
      return res.status(404).json({ error: 'Original test not found.' });
    }

    const retestId = `test-retest-${Date.now().toString(36)}-${Math.random().toString(36).substring(2, 7)}`;
    const now = new Date().toISOString();

    const willBeImproved = originalTest.url.includes('/demo-site') || originalTest.isImprovedDemo === false || true;
    const retestUrl = originalTest.url.includes('/demo-site') && !originalTest.url.includes('improved=true')
      ? `${originalTest.url}?improved=true`
      : originalTest.url;

    const retestRecord: TestRecord = {
      id: retestId,
      url: retestUrl,
      task: originalTest.task,
      persona: originalTest.persona,
      status: 'running',
      steps: [],
      barriers: [],
      createdAt: now,
      updatedAt: now,
      retestedFromId: originalTest.id,
      isImprovedDemo: willBeImproved
    };

    dbService.createTest(retestRecord);
    dbService.updateTest(originalTest.id, { retestId });

    runTestAsync(retestRecord);

    return res.status(201).json(retestRecord);
  } catch (err: any) {
    return res.status(500).json({ error: err.message || 'Failed to trigger retest.' });
  }
});

async function runTestAsync(test: TestRecord) {
  try {
    const onEvent = (event: TinyFishRunEvent) => {
      if (event.streamingUrl) {
        dbService.updateTest(test.id, { streamingUrl: event.streamingUrl });
      }
      broadcastEvent(test.id, event);
    };

    const rawResult = await tinyfishService.executeTest(test, onEvent);

    const scoring = calculateTaskSuccessScore(
      rawResult.overallTaskSuccess,
      rawResult.steps,
      rawResult.barriers as any
    );

    const enrichedBarriers = enrichBarriersWithImpact(rawResult.barriers as any, test.persona);

    dbService.updateTest(test.id, {
      status: 'completed',
      score: scoring.score,
      completionStatus: scoring.completionStatus,
      scoreBreakdown: scoring.scoreBreakdown,
      overallTaskSuccess: rawResult.overallTaskSuccess,
      confidence: rawResult.confidence,
      summary: rawResult.summary,
      steps: rawResult.steps as any,
      barriers: enrichedBarriers
    });

    broadcastEvent(test.id, {
      type: 'COMPLETE',
      testId: test.id,
      result: rawResult
    });
  } catch (err: any) {
    dbService.updateTest(test.id, {
      status: 'failed',
      summary: `The website could not be tested: ${err.message || 'Agent could not access page'}.`
    });
    broadcastEvent(test.id, {
      type: 'ERROR',
      testId: test.id,
      error: err.message
    });
  }
}

export default router;
