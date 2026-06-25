import { describe, it, expect } from 'vitest';
import request from 'supertest';
import '../helpers/setup.js';
import { buildApp } from '../../src/app.js';
import { setExpandedRolesFlag } from '../../src/roles/feature-flags.js';
import { addHiringTeamMember, createJobRecord } from '../../src/jobs/job-repo.js';
import { getJobPermissions } from '../../src/permissions/job-lifecycle.js';
import { resolveEffectiveRole } from '../../src/jobs/hiring-team.js';
import { authHeaders } from '../helpers/setup.js';
import { SECONDARY_RECRUITER_ID, PRIMARY_RECRUITER_ID, LEGACY_RECRUITER } from '../../src/roles/types.js';

const app = buildApp();

describe('Server permissions endpoint', () => {
  const tenantId = 'tenant-1';

  it('exposes permissions for UI consumption', async () => {
    setExpandedRolesFlag(tenantId, true);
    const job = createJobRecord(tenantId, 'x', 'blank');
    addHiringTeamMember({
      jobId: job.jobId,
      userId: 'sec',
      expandedRoleId: SECONDARY_RECRUITER_ID,
      legacyRole: 'Secondary Recruiter',
    });

    const res = await request(app)
      .get(`/api/jobs/${job.jobId}/permissions`)
      .set(authHeaders('sec', tenantId));

    expect(res.body.canDelete).toBe(false);
    expect(res.body.canClose).toBe(false);
    expect(res.body.effectiveRole.roleId).toBe(SECONDARY_RECRUITER_ID);
  });

  it('role lookup completes within 5ms p95 in harness', () => {
    setExpandedRolesFlag(tenantId, true);
    const job = createJobRecord(tenantId, 'x', 'blank');
    addHiringTeamMember({
      jobId: job.jobId,
      userId: 'pri',
      expandedRoleId: PRIMARY_RECRUITER_ID,
      legacyRole: LEGACY_RECRUITER,
    });

    const ctx = { userId: 'pri', tenantId };
    const samples: number[] = [];
    for (let i = 0; i < 100; i++) {
      const start = performance.now();
      resolveEffectiveRole(ctx, job.jobId);
      getJobPermissions(ctx, job.jobId);
      samples.push(performance.now() - start);
    }
    samples.sort((a, b) => a - b);
    const p95 = samples[Math.floor(samples.length * 0.95)];
    expect(p95).toBeLessThanOrEqual(5);
  });
});
