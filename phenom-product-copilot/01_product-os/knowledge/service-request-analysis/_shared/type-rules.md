# Shared true-type rules (cross-PE)

This is a quick signal index. The authoritative decision order, exceptions, confidence, and PM-review rules live in
[`../rulebook.md`](../rulebook.md). Full product-area remaps live under each PE’s `areas.md`.

| Signal | True type | Notes |
|--------|-----------|--------|
| Unmerge of incorrectly merged people | **Service Request** | Do **not** open a separate Bug-Customer for the bad merge |
| UI control missing after a deploy | **Bug-Customer** | Regression / missing UI |
| Tenant feature-flag enablement | **Service Request** | Config / enablement |
| “How does X work?” / “is this possible?” with nothing broken | **Service Request** | Question is retired; classify as Product & Knowledge Issues |
| ATS↔CRM (or system) sync gap Support can manually correct | **Service Request** | Manual fix path |
| Sync gap Support cannot correct | **Bug-Customer** | Needs engineering |
| Support seeds/maps field, filter, watchlist, status, or similar config | **Service Request** | Ops fulfillment |
| Automation not firing / wrong action / email not sent | **Bug-Customer** | Broken behavior, unless investigation proves expected behavior, configuration, suppression/consent, an external provider, or unsupported use |
| Template / branding / logo / copy via Support | **Service Request** | Content ops |

For the complete decision order and locked exceptions, use
[`../rulebook.md`](../rulebook.md); this file is only a compact cross-PE summary.
