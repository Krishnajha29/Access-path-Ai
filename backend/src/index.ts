import express from 'express';
import cors from 'cors';
import path from 'path';
import fs from 'fs';
import { PORT } from './config.js';
import testRoutes from './routes/testRoutes.js';

const app = express();

app.use(cors({
  origin: '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
}));

app.use(express.json());

// Health Check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    service: 'AccessPath AI Backend',
    timestamp: new Date().toISOString()
  });
});

// Test API Routes
app.use('/api/tests', testRoutes);

// Serve Controlled Demo Site statically on /demo-site
const demoSiteDir = path.resolve(process.cwd(), '../demo-site/public');
if (fs.existsSync(demoSiteDir)) {
  app.use('/demo-site', express.static(demoSiteDir));
}

// Serve Frontend Build if present
const frontendDist = path.resolve(process.cwd(), '../frontend/dist');
if (fs.existsSync(frontendDist)) {
  app.use(express.static(frontendDist));
  // SPA fallback for react-router (ignoring /api and /demo-site)
  app.get('*', (req, res, next) => {
    if (req.path.startsWith('/api') || req.path.startsWith('/demo-site')) {
      return next();
    }
    res.sendFile(path.join(frontendDist, 'index.html'));
  });
}

// Fallback error handler
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error('Unhandled server error:', err);
  res.status(500).json({
    error: 'Internal server error occurred.',
    message: err.message || 'Unknown error'
  });
});

app.listen(PORT, () => {
  console.log(`=======================================================`);
  console.log(`🚀 AccessPath AI Platform live on http://localhost:${PORT}`);
  console.log(`📡 API endpoint: http://localhost:${PORT}/api/tests`);
  console.log(`🧪 Demo site: http://localhost:${PORT}/demo-site/index.html`);
  console.log(`=======================================================`);
});
