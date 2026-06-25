import { describe, it, expect } from 'vitest';
import request from 'supertest';
import '../helpers/setup.js';
import { buildApp } from '../../src/app.js';
import { setExpandedRolesFlag } from '../../src/roles/feature-flags.js';
import { addHiringTeamMember, createJobRecord } from '../../src/jobs/job-repo.js';
import { authHeaders } from '../helpers/setup.js';
import { SECONDARY_RECRUITER_ID } from '../../src/roles/types.js';

const app = buildApp();

describe('UI permissions', () => {
  it('serves create job HTML page', async () => {
    const res = await request(app)
      .get('/ui/create-job')
      .set(authHeaders('u', 't'));
    expect(res.status).toBe(200);
    expect(res.text).toContain('Create New Job');
    expect(res.text).toContain('pds.css');
  });

  it('permissions endpoint reflects Secondary cannot delete/close (UI hides actions)', async () => {
    const tenantId = 'tenant-1';
    setExpandedRolesFlag(tenantId, true);
    const job = createJobRecord(tenantId, 'creator', 'blank');
    addHiringTeamMember({
      jobId: job.jobId,
      userId: 'sec',
      expandedRoleId: SECONDARY_RECRUITER_ID,
      legacyRole: 'Secondary Recruiter',
    });

    const perms = await request(app)
      .get(`/api/jobs/${job.jobId}/permissions`)
      .set(authHeaders('sec', tenantId));
    expect(perms.body.canDelete).toBe(false);
    expect(perms.body.canClose).toBe(false);

    const directDelete = await request(app)
      .delete(`/api/jobs/${job.jobId}`)
      .set(authHeaders('sec', tenantId));
    expect(directDelete.status).toBe(403);
  });

  it('serves job actions page at legacy path', async () => {
    const res = await request(app)
      .get('/ui/job-actions')
      .set(authHeaders('u', 't'));
    expect(res.status).toBe(200);
    expect(res.text).toContain('Create New Job');
  });
});
