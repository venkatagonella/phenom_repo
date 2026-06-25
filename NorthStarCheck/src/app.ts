import express from 'express';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createApp } from './api/routes.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export function buildApp(): express.Application {
  const app = express();
  app.use(express.json());
  app.use(createApp());
  app.use('/ui', express.static(path.join(__dirname, 'ui')));
  return app;
}
