import fs from 'fs';
import path from 'path';
import os from 'os';
import dotenv from 'dotenv';

dotenv.config();

export function getTinyFishApiKey(): string | undefined {
  if (process.env.TINYFISH_API_KEY && process.env.TINYFISH_API_KEY.trim()) {
    return process.env.TINYFISH_API_KEY.trim();
  }

  try {
    const configPath = path.join(os.homedir(), '.tinyfish', 'config.json');
    if (fs.existsSync(configPath)) {
      const raw = fs.readFileSync(configPath, 'utf8');
      const parsed = JSON.parse(raw);
      if (parsed.api_key && typeof parsed.api_key === 'string') {
        return parsed.api_key.trim();
      }
    }
  } catch (err) {
    // silently fail back to undefined
  }

  return undefined;
}

export const PORT = process.env.PORT ? parseInt(process.env.PORT, 10) : 5000;
export const DEMO_SITE_PORT = 5000; // Served on /demo-site by express
export const TINYFISH_API_URL = process.env.TINYFISH_API_URL || 'https://agent.tinyfish.ai';
