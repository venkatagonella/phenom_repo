import { describe, it, expect, beforeEach } from 'vitest';
import '../helpers/setup.js';
import { setExpandedRolesFlag } from '../../src/roles/feature-flags.js';
import { addHiringTeamMember } from '../../src/jobs/job-repo.js';
import { resolveEffectiveRole } from '../../src/jobs/hiring-team.js';
import {
  PRIMARY_RECRUITER_ID,
  SECONDARY_RECRUITER_ID,
  LEGACY_RECRUITER,
} from '../../src/roles/types.js';

describe('Hiring team effective role', () => {
  const ctx = { userId: 'user-1', tenantId: 'tenant-1' };
  const jobId = 'job-1';

  beforeEach(() => {
    setExpandedRolesFlag('tenant-1', true);
  });

  it('picks Primary when user has both Primary and Secondary on same job', () => {
    addHiringTeamMember({
      jobId,
      userId: 'user-1',
      expandedRoleId: SECONDARY_RECRUITER_ID,
      legacyRole: 'Secondary Recruiter',
    });
    addHiringTeamMember({
      jobId,
      userId: 'user-1',
      expandedRoleId: PRIMARY_RECRUITER_ID,
      legacyRole: LEGACY_RECRUITER,
    });

    const role = resolveEffectiveRole(ctx, jobId);
    expect(role?.roleId).toBe(PRIMARY_RECRUITER_ID);
    expect(role!.hierarchyPriority).toBeGreaterThan(50);
  });
});
