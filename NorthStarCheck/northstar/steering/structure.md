# Repository structure

```
NorthStarCheck/
├── northstar/
│   ├── specs/           # Increment specs (SDD)
│   └── steering/        # Living product/tech context
├── src/
│   ├── roles/
│   ├── jobs/
│   ├── permissions/
│   ├── api/
│   ├── ui/
│   ├── app.ts           # Express app factory (used by tests)
│   └── index.ts         # Server entrypoint
└── tests/
    ├── unit/
    ├── integration/
    └── helpers/
```

New features add a numbered folder under `northstar/specs/` and must be listed in `northstar/specs/INDEX.md`.
