# Policy templates

Shared copy-paste templates for Phenom product work. Prefer these over inventing new structures.

| Template | When to use | Audience |
|----------|-------------|----------|
| [`sa-crm-customer-requirements.md`](./sa-crm-customer-requirements.md) | Customer development ask entering CRM — problem, workflows, sequence & state diagrams, before FRD | Solution Architects → CRM PM |
| [`epic.md`](./epic.md) | Jira Epic description | PM |
| [`story.md`](./story.md) | Jira Story description (Given/When/Then) | PM |

Related (outside this folder):

| Artifact | Location |
|----------|----------|
| FRD (Parts A–D) | `phenom_repo/SpecDrivenDev/templates/frd-template.md` |
| PRD skill (PM pipeline) | `skills/prd.md` |
| Platform pod routing | `policies/platform-routing.md` |
| CUSP feedback (not commits) | `skills/product-feedback.md` |

**Flow for customer build asks:**

```
SA pack (sa-crm-customer-requirements)
  → FRD (SpecDrivenDev frd-template)
    → Epic (epic.md) + Stories (story.md)
      → Development
```
