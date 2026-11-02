# Category / subcategory taxonomy — how to evolve it

Type (Service Request / Bug-Customer) and product area are **stable policy**.
Categories and subcategories are **living themes** — PMs and the agent may extend them.

## Where the source of truth lives

| Concern | Home |
|---------|------|
| When is it Service Request vs Bug-Customer? | `_shared/type-rules.md` |
| Which product area? | `<pe>/areas.md` |
| Which L1 / L2 names exist? | Live label sheet **Product Taxonomy** tab |
| Which ticket got which labels? | Label sheet (Drive) |

## Rules for changing taxonomy

1. **Add** a category/subcategory when ≥ ~5 true SRs clearly share a theme (or PM names a prevention package).
2. **Rename** only with a redirect note (old name → new name) so historical sheet rows still map.
3. **Do not** encode type/area decisions only inside a subcategory name — type rules stay in `type-rules.md`.
4. Every taxonomy row needs a one-line **pick when** rule (and optionally **do not use when**).
5. Agent may **propose** new categories; PM **accepts** before they become default picks.
6. After acceptance, update the sheet Product Taxonomy tab. PE `taxonomy.md` files are optional legacy seeds, not a second source of truth.

## Pick-policy template (per subcategory)

```markdown
### Category — Subcategory
- **Pick when:** …
- **Do not use when:** …
- **Typical true_type:** Service Request | Bug-Customer
- **Typical product area:** …
- **Prevention package:** (optional link/name)
```
