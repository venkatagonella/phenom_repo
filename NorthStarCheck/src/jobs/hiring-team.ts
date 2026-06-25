import { resolveMembershipRole } from '../roles/registry.js';
import type { AuthContext, HiringTeamMember, Role } from '../roles/types.js';
import { getMembersForUserOnJob } from './job-repo.js';

export function resolveEffectiveRole(ctx: AuthContext, jobId: string): Role | null {
  const memberships = getMembersForUserOnJob(jobId, ctx.userId);
  if (memberships.length === 0) return null;

  let best: Role | null = null;
  for (const m of memberships) {
    const { role } = resolveMembershipRole(m.expandedRoleId, m.legacyRole);
    if (!best || role.hierarchyPriority > best.hierarchyPriority) {
      best = role;
    }
  }
  return best;
}

export function hasLegacyRecruiterMembership(ctx: AuthContext, jobId: string): boolean {
  return getMembersForUserOnJob(jobId, ctx.userId).some(
    (m) => m.legacyRole === 'Recruiter',
  );
}

export function assignMember(member: HiringTeamMember): HiringTeamMember {
  return { ...member };
}
