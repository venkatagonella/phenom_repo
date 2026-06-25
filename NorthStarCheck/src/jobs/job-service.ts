import {
  PRIMARY_RECRUITER_ID,
  SECONDARY_RECRUITER_ID,
  LEGACY_RECRUITER,
  type AuthContext,
  type Job,
  type JobSource,
} from '../roles/types.js';
import {
  canCloseJob,
  canCreateJob,
  canDeleteJob,
} from '../permissions/job-lifecycle.js';
import {
  addHiringTeamMember,
  createJobRecord,
  deleteJobRecord,
  getJob,
  setJobStatus,
} from './job-repo.js';

export class AuthorizationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'AuthorizationError';
  }
}

export class NotFoundError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'NotFoundError';
  }
}

const userGlobalRoles = new Map<string, string>();

export function setUserGlobalRole(userId: string, expandedRoleId: string): void {
  userGlobalRoles.set(userId, expandedRoleId);
}

export function clearUserGlobalRoles(): void {
  userGlobalRoles.clear();
}

function globalRoleForUser(userId: string): string {
  return userGlobalRoles.get(userId) ?? PRIMARY_RECRUITER_ID;
}

function legacyRoleForExpanded(expandedRoleId: string): string {
  return expandedRoleId === PRIMARY_RECRUITER_ID ? LEGACY_RECRUITER : 'Secondary Recruiter';
}

export function createJob(
  ctx: AuthContext,
  source: JobSource,
  cloneFromJobId?: string,
): Job {
  if (!canCreateJob(ctx)) {
    throw new AuthorizationError('Not authorized to create jobs');
  }

  if (source === 'clone' && cloneFromJobId && !getJob(cloneFromJobId)) {
    throw new NotFoundError(`Job not found: ${cloneFromJobId}`);
  }

  const job = createJobRecord(ctx.tenantId, ctx.userId, source);
  const expandedRoleId = globalRoleForUser(ctx.userId);

  addHiringTeamMember({
    jobId: job.jobId,
    userId: ctx.userId,
    expandedRoleId,
    legacyRole: legacyRoleForExpanded(expandedRoleId),
  });

  return job;
}

export function deleteJob(ctx: AuthContext, jobId: string): void {
  if (!getJob(jobId)) {
    throw new NotFoundError(`Job not found: ${jobId}`);
  }
  if (!canDeleteJob(ctx, jobId)) {
    throw new AuthorizationError('Not authorized to delete this job');
  }
  deleteJobRecord(jobId);
}

export function closeJob(ctx: AuthContext, jobId: string): Job {
  if (!getJob(jobId)) {
    throw new NotFoundError(`Job not found: ${jobId}`);
  }
  if (!canCloseJob(ctx, jobId)) {
    throw new AuthorizationError('Not authorized to close this job');
  }
  const updated = setJobStatus(jobId, 'closed');
  if (!updated) {
    throw new NotFoundError(`Job not found: ${jobId}`);
  }
  return updated;
}

export { SECONDARY_RECRUITER_ID, PRIMARY_RECRUITER_ID };
