import { describe, it, expect } from 'vitest';
import request from 'supertest';
import '../helpers/setup.js';
import { buildApp } from '../../src/app.js';
import { setExpandedRolesFlag } from '../../src/roles/feature-flags.js';
import { addHiringTeamMember, createJobRecord, getJob } from '../../src/jobs/job-repo.js';
import { authHeaders } from '../helpers/setup.js';
import { SECONDARY_RECRUITER_ID, LEGACY_RECRUITER } from '../../src/roles/types.js';

const app = buildApp();

describe('Legacy regression (flag OFF)', () => {
  const tenantId = 'legacy-tenant';
  const userId = 'legacy-recruiter';

  it('allows legacy recruiter to delete and close when flag OFF', async () => {
    setExpandedRolesFlag(tenantId, false);
    const job = createJobRecord(tenantId, userId, 'blank');
    addHiringTeamMember({
      jobId: job.jobId,
      userId,
      expandedRoleId: SECONDARY_RECRUITER_ID,
      legacyRole: LEGACY_RECRUITER,
    });

    const closeRes = await request(app)
      .post(`/api/jobs/${job.jobId}/close`)
      .set(authHeaders(userId, tenantId));
    expect(closeRes.status).toBe(200);

    const job2 = createJobRecord(tenantId, userId, 'template');
    addHiringTeamMember({
      jobId: job2.jobId,
      userId,
      expandedRoleId: SECONDARY_RECRUITER_ID,
      legacyRole: LEGACY_RECRUITER,
    });

    const deleteRes = await request(app)
      .delete(`/api/jobs/${job2.jobId}`)
      .set(authHeaders(userId, tenantId));
    expect(deleteRes.status).toBe(200);
    expect(getJob(job2.jobId)).toBeUndefined();
  });

  it('allows legacy recruiter to create jobs when flag OFF', async () => {
    setExpandedRolesFlag(tenantId, false);
    const res = await request(app)
      .post('/api/jobs')
      .set(authHeaders(userId, tenantId))
      .send({ source: 'blank' });
    expect(res.status).toBe(201);
  });
});
