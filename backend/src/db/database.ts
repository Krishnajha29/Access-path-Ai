import fs from 'fs';
import path from 'path';
import { TestRecord } from '../types.js';

interface DatabaseSchema {
  tests: Record<string, TestRecord>;
}

const DATA_DIR = path.resolve(process.cwd(), 'data');
const DB_FILE = path.join(DATA_DIR, 'accesspath.json');

function ensureDbFile(): DatabaseSchema {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }

  if (!fs.existsSync(DB_FILE)) {
    const initial: DatabaseSchema = { tests: {} };
    fs.writeFileSync(DB_FILE, JSON.stringify(initial, null, 2), 'utf8');
    return initial;
  }

  try {
    const content = fs.readFileSync(DB_FILE, 'utf8');
    return JSON.parse(content);
  } catch (err) {
    const initial: DatabaseSchema = { tests: {} };
    fs.writeFileSync(DB_FILE, JSON.stringify(initial, null, 2), 'utf8');
    return initial;
  }
}

function saveDb(data: DatabaseSchema) {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
  const tempFile = `${DB_FILE}.tmp`;
  fs.writeFileSync(tempFile, JSON.stringify(data, null, 2), 'utf8');
  fs.renameSync(tempFile, DB_FILE);
}

export class DatabaseService {
  private static instance: DatabaseService;

  private constructor() {
    ensureDbFile();
  }

  public static getInstance(): DatabaseService {
    if (!DatabaseService.instance) {
      DatabaseService.instance = new DatabaseService();
    }
    return DatabaseService.instance;
  }

  public createTest(test: TestRecord): TestRecord {
    const db = ensureDbFile();
    db.tests[test.id] = test;
    saveDb(db);
    return test;
  }

  public getTest(id: string): TestRecord | null {
    const db = ensureDbFile();
    return db.tests[id] || null;
  }

  public updateTest(id: string, updates: Partial<TestRecord>): TestRecord | null {
    const db = ensureDbFile();
    const existing = db.tests[id];
    if (!existing) return null;

    const updated: TestRecord = {
      ...existing,
      ...updates,
      updatedAt: new Date().toISOString()
    };

    db.tests[id] = updated;
    saveDb(db);
    return updated;
  }

  public getAllTests(): TestRecord[] {
    const db = ensureDbFile();
    return Object.values(db.tests).sort(
      (a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    );
  }
}

export const dbService = DatabaseService.getInstance();
