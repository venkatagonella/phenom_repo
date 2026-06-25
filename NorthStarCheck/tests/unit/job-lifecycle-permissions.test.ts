import { describe, it, expect } from 'vitest';
import '../helpers/setup.js';
import { setExpandedRolesFlag } from '../../src/roles/feature-flags.js';
import { addHiringTeamMember } from '../../src/jobs/job-repo.js';
import { createJobRecord } from '../../src/jobs/job-repo.js';
import {
  canCloseJob,
  canDeleteJob,
} from '../../src/permissions/job-lifecycle.js';
import {
  PRIMARY_RECRUITER_ID,
  SECONDARY_RECRUITER_ID,
  LEGACY_RECRUITER,
} from '../../src/roles/types.js';

describe('Job lifecycle permissions', () => {
  const tenantId = 'tenant-1';

  function setupJob(createdBy: string): string {
    const job = createJobRecord(tenantId, createdBy, 'blank');
    return job.jobId;
  }

  it('denies Secondary delete/close when flag ON', () => {
    setExpandedRolesFlag(tenantId, true);
    const id = setupJob('other-user');
    addHiringTeamMember({
      jobId: id,
      userId: 'secondary-user',
      expandedRoleId: SECONDARY_RECRUITER_ID,
      legacyRole: 'Secondary Recruiter',
    });

    const ctx = { userId: 'secondary-user', tenantId };
    expect(canDeleteJob(ctx, id)).toBe(false);
    expect(canCloseJob(ctx, id)).toBe(false);
  });

  it('allows Primary delete/close when flag ON', () => {
    setExpandedRolesFlag(tenantId, true);
    const id = setupJob('other-user');
    addHiringTeamMember({
      jobId: id,
      userId: 'primary-user',
      expandedRoleId: PRIMARY_RECRUITER_ID,
      legacyRole: LEGACY_RECRUITER,
    });

    const ctx = { userId: 'primary-user', tenantId };
    expect(canDeleteJob(ctx, id)).toBe(true);
    expect(canCloseJob(ctx, id)).toBe(true);
  });

  it('uses legacy path when flag OFF', () => {
    setExpandedRolesFlag(tenantId, false);
    const id = setupJob('user-legacy');
    addHiringTeamMember({
      jobId: id,
      userId: 'user-legacy',
      expandedRoleId: SECONDARY_RECRUITER_ID,
      legacyRole: LEGACY_RECRUITER,
    });

    const ctx = { userId: 'user-legacy', tenantId };
    expect(canDeleteJob(ctx, id)).toBe(true);
    expect(canCloseJob(ctx, id)).toBe(true);
  });

  it('denies Secondary who created the job (not createdBy-based allow)', () => {
    setExpandedRolesFlag(tenantId, true);
    const id = setupJob('secondary-creator');
    addHiringTeamMember({
      jobId: id,
      userId: 'secondary-creator',
      expandedRoleId: SECONDARY_RECRUITER_ID,
      legacyRole: 'Secondary Recruiter',
    });

    const ctx = { userId: 'secondary-creator', tenantId };
    expect(canDeleteJob(ctx, id)).toBe(false);
    expect(canCloseJob(ctx, id)).toBe(false);
  });

  it('allows Primary who did not create the job', () => {
    setExpandedRolesFlag(tenantId, true);
    const id = setupJob('secondary-creator');
    addHiringTeamMember({
      jobId: id,
      userId: 'primary-not-creator',
      expandedRoleId: PRIMARY_RECRUITER_ID,
      legacyRole: LEGACY_RECRUITER,
    });

    const ctx = { userId: 'primary-not-creator', tenantId };
    expect(canDeleteJob(ctx, id)).toBe(true);
  });
});
