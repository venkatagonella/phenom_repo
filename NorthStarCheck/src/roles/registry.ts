import {
  LEGACY_RECRUITER,
  PRIMARY_RECRUITER_ID,
  SECONDARY_RECRUITER_ID,
  type Role,
} from './types.js';

const REGISTRY: Role[] = [
  {
    roleId: PRIMARY_RECRUITER_ID,
    displayName: 'Recruiter (Primary)',
    hierarchyPriority: 100,
    category: 'Leading',
  },
  {
    roleId: SECONDARY_RECRUITER_ID,
    displayName: 'Secondary Recruiter',
    hierarchyPriority: 50,
    category: 'Supporting',
  },
];

const byId = new Map(REGISTRY.map((r) => [r.roleId, r]));

export function getRegistry(): readonly Role[] {
  return REGISTRY;
}

export function getRoleById(roleId: string): Role | undefined {
  return byId.get(roleId);
}

/**
 * Resolves expanded role from membership fields.
 * Legacy "Recruiter" maps to Primary Recruiter while preserving legacy display label.
 */
export function resolveMembershipRole(
  expandedRoleId: string | undefined,
  legacyRole: string,
): { role: Role; legacyDisplay: string } {
  if (expandedRoleId) {
    const role = byId.get(expandedRoleId);
    if (role) {
      return { role, legacyDisplay: legacyRole };
    }
  }

  if (legacyRole === LEGACY_RECRUITER) {
    const primary = byId.get(PRIMARY_RECRUITER_ID)!;
    return { role: primary, legacyDisplay: LEGACY_RECRUITER };
  }

  throw new Error(`Unknown role: expanded=${expandedRoleId}, legacy=${legacyRole}`);
}

export function isPrimaryRecruiter(role: Role): boolean {
  return role.roleId === PRIMARY_RECRUITER_ID;
}
