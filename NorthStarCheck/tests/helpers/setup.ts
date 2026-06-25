import { beforeEach } from 'vitest';
import { clearFeatureFlags } from '../../src/roles/feature-flags.js';
import { clearStores } from '../../src/jobs/job-repo.js';
import { clearUserGlobalRoles } from '../../src/jobs/job-service.js';

export function resetAll(): void {
  clearFeatureFlags();
  clearStores();
  clearUserGlobalRoles();
}

export function authHeaders(userId: string, tenantId: string): Record<string, string> {
  return {
    'x-user-id': userId,
    'x-tenant-id': tenantId,
    'Content-Type': 'application/json',
  };
}

beforeEach(() => {
  resetAll();
});
