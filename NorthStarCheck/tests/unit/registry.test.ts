import { describe, it, expect } from 'vitest';
import '../helpers/setup.js';
import { getRegistry, resolveMembershipRole } from '../../src/roles/registry.js';
import {
  PRIMARY_RECRUITER_ID,
  SECONDARY_RECRUITER_ID,
  LEGACY_RECRUITER,
} from '../../src/roles/types.js';

describe('Role registry', () => {
  it('returns Primary and Secondary with stable IDs and categories', () => {
    const first = getRegistry();
    const second = getRegistry();

    expect(first).toHaveLength(2);
    expect(first[0].roleId).toBe(PRIMARY_RECRUITER_ID);
    expect(first[0].category).toBe('Leading');
    expect(first[1].roleId).toBe(SECONDARY_RECRUITER_ID);
    expect(first[1].category).toBe('Supporting');
    expect(first[0].roleId).toBe(second[0].roleId);
  });

  it('resolves legacy Recruiter to Primary with preserved display label', () => {
    const { role, legacyDisplay } = resolveMembershipRole(undefined as unknown as string, LEGACY_RECRUITER);
    expect(role.roleId).toBe(PRIMARY_RECRUITER_ID);
    expect(legacyDisplay).toBe(LEGACY_RECRUITER);
  });
});
