---
title: "Rating the filled template example"
prompt: "/product-story-analyzer Review the example story in templates/example-product-story.md"
note: "Run against the skill's own filled example, so no customer ticket is involved. The duplicate and team checks are shown as the skill reports them when Jira and the engineering clones are not connected."
---

### Example story: Job creation – Publish jobs to all locales with job details copied   🟠

**Verdict:** Clear, well-structured need; three facts are still placeholders, so it goes back to the SA before the decision.

| Section | Status | Gap |
|---------|--------|-----|
| Summary | ✅ | |
| Customer problem | ⚠️ | Jobs created per month is "to confirm"; without it the 24-click cost can't be sized |
| Customer impact | ⚠️ | UAT / go-live dates, other customers and "committed to the customer?" are placeholders |
| Requirements | ✅ | Numbered, observable, ranked Must / Nice to have |
| User journey | ✅ | Includes both edge cases; flow diagram link is still a placeholder (recommended, not rated) |
| Acceptance criteria | ✅ | Four Given / When / Then scenarios, all testable |
| Scope | ✅ | |
| Related tickets | ✅ | Four earlier tickets named as duplicates to close |
| Teams required | ✅ | Table with a reason per product |
| Open questions | ✅ | Every question has an owner |

**Duplicate / related:** Not run in this example (Jira not connected). The story itself says it replaces four earlier tickets, which is the right pattern.
**Teams (from code):** Not run in this example (no engineering clones). Validate CRM + HRM with the owning teams.

**Feedback for the SA** (ready to paste as a comment)
- How many jobs does the customer create per month, manually and from templates?
- What are the UAT and go-live dates this blocks?
- Did you check the SA channel for other customers with the same need? Name them or give a count.
- Was anything committed to the customer? If yes, by whom and where is it written down?
