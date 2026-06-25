import { isExpandedRolesEnabled } from '../roles/feature-flags.js';
import { isPrimaryRecruiter } from '../roles/registry.js';
import type { AuthContext, JobPermissions } from '../roles/types.js';
import { getJob } from '../jobs/job-repo.js';
import { hasLegacyRecruiterMembership, resolveEffectiveRole } from '../jobs/hiring-team.js';

export function canDeleteJob(ctx: AuthContext, jobId: string): boolean {
  return canPerformLifecycleAction(ctx, jobId);
}

export function canCloseJob(ctx: AuthContext, jobId: string): boolean {
  return canPerformLifecycleAction(ctx, jobId);
}

export function canCreateJob(_ctx: AuthContext): boolean {
  return true;
}

export function getJobPermissions(ctx: AuthContext, jobId: string): JobPermissions {
  const effectiveRole = isExpandedRolesEnabled(ctx.tenantId)
    ? resolveEffectiveRole(ctx, jobId)
    : null;

  return {
    canDelete: canDeleteJob(ctx, jobId),
    canClose: canCloseJob(ctx, jobId),
    effectiveRole,
  };
}

function canPerformLifecycleAction(ctx: AuthContext, jobId: string): boolean {
  if (!getJob(jobId)) return false;

  if (!isExpandedRolesEnabled(ctx.tenantId)) {
    return hasLegacyRecruiterMembership(ctx, jobId);
  }

  const effective = resolveEffectiveRole(ctx, jobId);
  return effective !== null && isPrimaryRecruiter(effective);
}
