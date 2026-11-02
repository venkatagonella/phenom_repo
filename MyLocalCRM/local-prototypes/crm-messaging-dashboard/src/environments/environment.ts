/**
 * Local prototype env — mirrors crm-inbox-fe environment.endpoint.crmHub usage.
 * Real paths verified in MyLocalCRM/repos/crm-inbox-fe/.../inbox.service.ts
 */
export const environment = {
  production: false,
  useMock: true,
  endpoint: {
    /** CRM hub / API gateway base (tenant-routed in production) */
    crmHub: '/api',
  },
};
