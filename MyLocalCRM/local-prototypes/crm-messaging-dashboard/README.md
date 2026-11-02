# crm-messaging-dashboard (local prototype)

Local **Phenom-shaped** Messaging Inbox project: PDS UI chrome like
`DesignSystem/templates/html/jobs-dashboard.html`, domain data/APIs from the
**phenom-messaging** knowledge pack (`crm-inbox-fe` + `crm-messaging-platform`).

> Not a production clone. Do not push to Bitbucket as a replacement for real MFEs.
> Lives under `MyLocalCRM/local-prototypes/` next to shallow clones.

## Quick start (runnable UI)

```bash
cd MyLocalCRM/local-prototypes/crm-messaging-dashboard
open prototypes/messaging-dashboard.html
open prototypes/how-this-repo-was-built.html   # process + diagrams (Bitbucket → local)
# or: npm run prototype   # serves prototypes/ on :4310
```

Uses symlinked PDS tokens from `DesignSystem/styles/`.

## Layout (mirrors `crm-inbox-fe`)

```
crm-messaging-dashboard/
├── prototypes/messaging-dashboard.html   ← open this (jobs-dashboard pattern → Inbox)
├── docs/grounded-apis.md                 ← repo/path map
├── webpack.config.js                     ← MF expose ./inbox (stub)
├── angular.json / package.json / tsconfig*
└── src/
    ├── styles/                           ← pds-tokens (symlink) + messaging-dashboard.css
    ├── assets/mock/conversations.json
    ├── environments/environment.ts
    └── app/
        ├── app.module.ts / app-routing.module.ts
        ├── core/service/messaging-api.constants.ts
        └── inbox/
            ├── inbox.module.ts
            ├── inbox-page/
            └── services/inbox.service.ts   ← same method names as production InboxService
```

## Agent skills to load

- **phenom-messaging** — controllers / intents / vendors  
- **phenom-design-system** — PDS tokens / px-* rules  
- **phenom-knowledge** — other CRM areas  

## Next steps toward a real Angular MFE

1. Copy deps/`@phenom/ui` patterns from `MyLocalCRM/repos/crm-inbox-fe` (VPN + `.npmrc`).
2. Replace HTML prototype with Angular templates using PDS / existing inbox components.
3. Point `environment.useMock = false` at a tenant CRM hub gateway.
4. Keep exposes aligned with host shell Module Federation config.
