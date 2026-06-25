import { Router } from 'express';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { isExpandedRolesEnabled } from '../roles/feature-flags.js';
import { getRegistry } from '../roles/registry.js';
import {
  AuthorizationError,
  NotFoundError,
  closeJob,
  createJob,
  deleteJob,
} from '../jobs/job-service.js';
import { addHiringTeamMember } from '../jobs/job-repo.js';
import { getJobPermissions } from '../permissions/job-lifecycle.js';
import type { JobSource } from '../roles/types.js';
import { authMiddleware, requireAuth, type AuthenticatedRequest } from './middleware.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export function createApp(): Router {
  const router = Router();

  router.use('/api', authMiddleware);

  router.get('/api/roles/registry', (req: AuthenticatedRequest, res) => {
    const ctx = requireAuth(req);
    if (!isExpandedRolesEnabled(ctx.tenantId)) {
      res.status(404).json({ error: 'Expanded roles not enabled for tenant' });
      return;
    }
    res.json({ roles: getRegistry() });
  });

  router.post('/api/jobs', (req: AuthenticatedRequest, res) => {
    try {
      const ctx = requireAuth(req);
      const source = req.body?.source as JobSource;
      const cloneFromJobId = req.body?.cloneFromJobId as string | undefined;

      if (!['template', 'blank', 'clone'].includes(source)) {
        res.status(400).json({ error: 'Invalid source' });
        return;
      }

      const job = createJob(ctx, source, cloneFromJobId);
      res.status(201).json(job);
    } catch (e) {
      handleError(res, e);
    }
  });

  router.delete('/api/jobs/:jobId', (req: AuthenticatedRequest, res) => {
    try {
      const ctx = requireAuth(req);
      deleteJob(ctx, req.params.jobId);
      res.status(200).json({ deleted: true });
    } catch (e) {
      handleError(res, e);
    }
  });

  router.post('/api/jobs/:jobId/close', (req: AuthenticatedRequest, res) => {
    try {
      const ctx = requireAuth(req);
      const job = closeJob(ctx, req.params.jobId);
      res.status(200).json(job);
    } catch (e) {
      handleError(res, e);
    }
  });

  router.get('/api/jobs/:jobId/permissions', (req: AuthenticatedRequest, res) => {
    try {
      const ctx = requireAuth(req);
      const permissions = getJobPermissions(ctx, req.params.jobId);
      res.json(permissions);
    } catch (e) {
      handleError(res, e);
    }
  });

  router.post('/api/jobs/:jobId/hiring-team', (req: AuthenticatedRequest, res) => {
    try {
      const ctx = requireAuth(req);
      const { userId, expandedRoleId, legacyRole } = req.body ?? {};
      if (!userId || !expandedRoleId || !legacyRole) {
        res.status(400).json({ error: 'userId, expandedRoleId, and legacyRole required' });
        return;
      }
      addHiringTeamMember({
        jobId: req.params.jobId,
        userId,
        expandedRoleId,
        legacyRole,
      });
      res.status(201).json({ jobId: req.params.jobId, userId, expandedRoleId, legacyRole });
    } catch (e) {
      handleError(res, e);
    }
  });

  router.get(['/ui/job-actions', '/ui/create-job'], (_req, res) => {
    res.sendFile(path.join(__dirname, '../ui/create-job.html'));
  });

  return router;
}

function handleError(res: import('express').Response, e: unknown): void {
  if (e instanceof AuthorizationError) {
    res.status(403).json({ error: e.message });
    return;
  }
  if (e instanceof NotFoundError) {
    res.status(404).json({ error: e.message });
    return;
  }
  res.status(500).json({ error: 'Internal server error' });
}
