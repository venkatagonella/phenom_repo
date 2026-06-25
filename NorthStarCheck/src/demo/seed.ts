import { setExpandedRolesFlag } from '../roles/feature-flags.js';
import { addHiringTeamMember } from '../jobs/job-repo.js';
import {
  createJob,
  setUserGlobalRole,
  PRIMARY_RECRUITER_ID,
  SECONDARY_RECRUITER_ID,
} from '../jobs/job-service.js';
import { LEGACY_RECRUITER } from '../roles/types.js';

export const DEMO_TENANT = 'demo-tenant';
export const DEMO_SECONDARY_USER = 'secondary-demo';
export const DEMO_PRIMARY_USER = 'primary-demo';

export function seedDemoData(): string {
  setExpandedRolesFlag(DEMO_TENANT, true);
  setUserGlobalRole(DEMO_SECONDARY_USER, SECONDARY_RECRUITER_ID);
  setUserGlobalRole(DEMO_PRIMARY_USER, PRIMARY_RECRUITER_ID);

  const secondaryCtx = { userId: DEMO_SECONDARY_USER, tenantId: DEMO_TENANT };
  const job = createJob(secondaryCtx, 'template');

  addHiringTeamMember({
    jobId: job.jobId,
    userId: DEMO_PRIMARY_USER,
    expandedRoleId: PRIMARY_RECRUITER_ID,
    legacyRole: LEGACY_RECRUITER,
  });

  return job.jobId;
}

export function demoUiUrl(
  baseUrl: string,
  jobId: string,
  userId: string,
  tenantId: string = DEMO_TENANT,
): string {
  const q = new URLSearchParams({ jobId, userId, tenantId });
  return `${baseUrl}/ui/create-job?${q}`;
}

export function demoCreateUrl(
  baseUrl: string,
  userId: string,
  tenantId: string = DEMO_TENANT,
): string {
  const q = new URLSearchParams({ userId, tenantId });
  return `${baseUrl}/ui/create-job?${q}`;
}
