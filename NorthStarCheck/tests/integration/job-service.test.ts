import { describe, it, expect, beforeEach } from 'vitest';
import '../helpers/setup.js';
import { setExpandedRolesFlag } from '../../src/roles/feature-flags.js';
import { addHiringTeamMember, getJob } from '../../src/jobs/job-repo.js';
import {
  AuthorizationError,
  createJob,
  deleteJob,
  closeJob,
  setUserGlobalRole,
  PRIMARY_RECRUITER_ID,
  SECONDARY_RECRUITER_ID,
} from '../../src/jobs/job-service.js';
import { LEGACY_RECRUITER } from '../../src/roles/types.js';

describe('Job service', () => {
  const tenantId = 'tenant-1';
  const secondaryCtx = { userId: 'sec-user', tenantId };
  const primaryCtx = { userId: 'pri-user', tenantId };

  beforeEach(() => {
    setExpandedRolesFlag(tenantId, true);
    setUserGlobalRole('sec-user', SECONDARY_RECRUITER_ID);
    setUserGlobalRole('pri-user', PRIMARY_RECRUITER_ID);
  });

  it.each(['template', 'blank', 'clone'] as const)(
    'Secondary can create job from %s',
    (source) => {
      let cloneFromJobId: string | undefined;
      if (source === 'clone') {
        const seed = createJob(primaryCtx, 'blank');
        cloneFromJobId = seed.jobId;
      }
      const job = createJob(secondaryCtx, source, cloneFromJobId);
      expect(job.jobId).toBeTruthy();
      expect(job.createdByUserId).toBe('sec-user');
    },
  );

  it('denies Secondary delete and close', () => {
    const job = createJob(secondaryCtx, 'blank');
    expect(() => deleteJob(secondaryCtx, job.jobId)).toThrow(AuthorizationError);
    expect(() => closeJob(secondaryCtx, job.jobId)).toThrow(AuthorizationError);
    expect(getJob(job.jobId)?.status).toBe('open');
  });

  it('allows Primary delete and close on assigned job', () => {
    const job = createJob(secondaryCtx, 'blank');
    addHiringTeamMember({
      jobId: job.jobId,
      userId: 'pri-user',
      expandedRoleId: PRIMARY_RECRUITER_ID,
      legacyRole: LEGACY_RECRUITER,
    });

    closeJob(primaryCtx, job.jobId);
    expect(getJob(job.jobId)?.status).toBe('closed');

    const job2 = createJob(secondaryCtx, 'blank');
    addHiringTeamMember({
      jobId: job2.jobId,
      userId: 'pri-user',
      expandedRoleId: PRIMARY_RECRUITER_ID,
      legacyRole: LEGACY_RECRUITER,
    });
    deleteJob(primaryCtx, job2.jobId);
    expect(getJob(job2.jobId)).toBeUndefined();
  });
});
