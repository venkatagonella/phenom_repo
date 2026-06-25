import { describe, it, expect, beforeEach } from 'vitest';
import request from 'supertest';
import '../helpers/setup.js';
import { buildApp } from '../../src/app.js';
import { setExpandedRolesFlag } from '../../src/roles/feature-flags.js';
import { addHiringTeamMember, createJobRecord, getJob } from '../../src/jobs/job-repo.js';
import { setUserGlobalRole, SECONDARY_RECRUITER_ID, PRIMARY_RECRUITER_ID } from '../../src/jobs/job-service.js';
import { authHeaders } from '../helpers/setup.js';
import { LEGACY_RECRUITER } from '../../src/roles/types.js';

const app = buildApp();

describe('API', () => {
  const tenantId = 'tenant-1';
  const secondaryUser = 'sec-user';
  const primaryUser = 'pri-user';

  beforeEach(() => {
    setExpandedRolesFlag(tenantId, true);
    setUserGlobalRole(secondaryUser, SECONDARY_RECRUITER_ID);
    setUserGlobalRole(primaryUser, PRIMARY_RECRUITER_ID);
  });

  it('returns 401 without session headers', async () => {
    const res = await request(app).get('/api/roles/registry');
    expect(res.status).toBe(401);
  });

  it('returns registry when flag ON', async () => {
    const res = await request(app)
      .get('/api/roles/registry')
      .set(authHeaders(primaryUser, tenantId));
    expect(res.status).toBe(200);
    expect(res.body.roles).toHaveLength(2);
  });

  it('returns 403 when Secondary deletes job', async () => {
    const job = createJobRecord(tenantId, 'other', 'blank');
    addHiringTeamMember({
      jobId: job.jobId,
      userId: secondaryUser,
      expandedRoleId: SECONDARY_RECRUITER_ID,
      legacyRole: 'Secondary Recruiter',
    });

    const res = await request(app)
      .delete(`/api/jobs/${job.jobId}`)
      .set(authHeaders(secondaryUser, tenantId));
    expect(res.status).toBe(403);
    expect(getJob(job.jobId)).toBeDefined();
  });

  it('returns 200 when Primary closes job', async () => {
    const job = createJobRecord(tenantId, 'other', 'blank');
    addHiringTeamMember({
      jobId: job.jobId,
      userId: primaryUser,
      expandedRoleId: PRIMARY_RECRUITER_ID,
      legacyRole: LEGACY_RECRUITER,
    });

    const res = await request(app)
      .post(`/api/jobs/${job.jobId}/close`)
      .set(authHeaders(primaryUser, tenantId));
    expect(res.status).toBe(200);
    expect(res.body.status).toBe('closed');
  });

  it('creates job via API for Secondary', async () => {
    const res = await request(app)
      .post('/api/jobs')
      .set(authHeaders(secondaryUser, tenantId))
      .send({ source: 'template' });
    expect(res.status).toBe(201);
    expect(res.body.createdByUserId).toBe(secondaryUser);
  });
});
