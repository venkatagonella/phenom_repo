# RX — category / subcategory taxonomy

> **Legacy seed — not the live taxonomy.** Level 1 / level 2 categories live on the sheet's **Product Taxonomy** tab
> (RX - Service Request Analysis), which the SR triage agent and the SR Prevention dashboard both read. Do not add categories here.

Living theme list for true-SR (and related) packaging. Type rules stay in `_shared/type-rules.md`; area remaps in `areas.md`.

Seed from current packages / sub_themes — refine with PM:

## CRM admin
### lists / access / roles
- **Pick when:** Support asked to grant access, fix list membership, or similar admin ops
- **Do not use when:** product is broken (→ Bug-Customer)
- **Typical true_type:** Service Request
- **Typical product area:** CRM - Profile or CRM - Core (as filed, unless remap applies)

### fields, filters, watchlists
- **Pick when:** seed/map/enable a field, filter, watchlist, or hiring status
- **Typical true_type:** Service Request

## Config hub
### feature-flag enablement
- **Pick when:** tenant flag enable/disable via Support
- **Typical true_type:** Service Request

## Privacy ops
### purge / export / retention
- **Pick when:** GDPR/DSAR/purge/export/retention fulfillment
- **Typical product area:** Compliance

### consent / opt-in
- **Pick when:** general consent/opt-in/repermission (not SMS/WhatsApp channel consent)
- **Typical product area:** Compliance

## Profile ops
### guided unmerge
- **Pick when:** client asks to unmerge incorrectly merged people
- **Typical true_type:** Service Request
- **Typical product area:** CRM - Profile

## Lifecycle ops
### delete / reactivate events & jobs
- **Pick when:** Support asked to delete/reactivate event or job lifecycle objects
- **Typical true_type:** Service Request

---

_PMs/agent: propose new rows via the label sheet Taxonomy tab, then PR into this file when accepted._
