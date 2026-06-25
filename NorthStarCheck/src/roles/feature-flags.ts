const tenantFlags = new Map<string, boolean>();

export function setExpandedRolesFlag(tenantId: string, enabled: boolean): void {
  tenantFlags.set(tenantId, enabled);
}

export function isExpandedRolesEnabled(tenantId: string): boolean {
  return tenantFlags.get(tenantId) ?? false;
}

export function clearFeatureFlags(): void {
  tenantFlags.clear();
}
