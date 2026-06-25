import type { Request, Response, NextFunction } from 'express';
import type { AuthContext } from '../roles/types.js';

export interface AuthenticatedRequest extends Request {
  auth?: AuthContext;
}

export function authMiddleware(
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction,
): void {
  const userId = req.header('x-user-id');
  const tenantId = req.header('x-tenant-id');

  if (!userId || !tenantId) {
    res.status(401).json({ error: 'Authentication required' });
    return;
  }

  req.auth = { userId, tenantId };
  next();
}

export function requireAuth(req: AuthenticatedRequest): AuthContext {
  if (!req.auth) {
    throw new Error('Missing auth context');
  }
  return req.auth;
}
