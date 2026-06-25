export type RoleCategory = 'Leading' | 'Supporting';

export interface Role {
  roleId: string;
  displayName: string;
  hierarchyPriority: number;
  category: RoleCategory;
}

export const PRIMARY_RECRUITER_ID = 'primary-recruiter';
export const SECONDARY_RECRUITER_ID = 'secondary-recruiter';
export const LEGACY_RECRUITER = 'Recruiter';

export type JobStatus = 'open' | 'closed';
export type JobSource = 'template' | 'blank' | 'clone';

export interface Job {
  jobId: string;
  tenantId: string;
  status: JobStatus;
  createdByUserId: string;
  source: JobSource;
}

export interface HiringTeamMember {
  jobId: string;
  userId: string;
  expandedRoleId: string;
  legacyRole: string;
}

export interface AuthContext {
  userId: string;
  tenantId: string;
}

export interface JobPermissions {
  canDelete: boolean;
  canClose: boolean;
  effectiveRole: Role | null;
}
