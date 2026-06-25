import { describe, it, expect } from 'vitest';
import '../helpers/setup.js';
import {
  isExpandedRolesEnabled,
  setExpandedRolesFlag,
} from '../../src/roles/feature-flags.js';

describe('Feature flags', () => {
  it('defaults to OFF per tenant', () => {
    expect(isExpandedRolesEnabled('tenant-a')).toBe(false);
  });

  it('reflects per-tenant enablement', () => {
    setExpandedRolesFlag('tenant-a', true);
    setExpandedRolesFlag('tenant-b', false);
    expect(isExpandedRolesEnabled('tenant-a')).toBe(true);
    expect(isExpandedRolesEnabled('tenant-b')).toBe(false);
  });
});
