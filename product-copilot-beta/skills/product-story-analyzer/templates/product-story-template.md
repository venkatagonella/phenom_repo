# SA Product Story Template

> For **Product Stories created by Solution Architects** in customer / implementation projects (e.g. `ISHIC1S-…`, `IDPRP-…`).
> Copy into the Product Story description (markdown). Rules → `policies/jira-story-rules.md` → "SA Product Stories". Quality check → `skills/product-story-analyzer/SKILL.md`.
>
> **Before you create a new ticket**
> 1. **Search first.** Is there already a Product Story or PHEM epic for this need — for this customer *or another one*? If yes, comment and link there. Do **not** open a second ticket.
> 2. **One need = one Product Story.** Do not split it by team (CRM, HRM, IX). Product breaks it into team stories inside the PHEM epic.
> 3. **No ETA here.** The ETA is committed on the PHEM epic once the work is planned ("in staging / production by R1 or R2").
>
> **Title:** `[Customer] – [Product area] – [Need in plain words]`
> e.g. `Siemens Healthineers – Job creation – Publish jobs to all locales with job details copied`
>
> **Style:** Write for someone who was not on the customer call. No "as discussed", no shorthand, no pasted AI text you have not checked. Attach screenshots, sample files and customer documents. Do not reference local or personal file paths.

---

## 1. Summary

One sentence: **who** needs **what**, and **why**.

---

## 2. Customer problem

- **What happens today:** [current behavior, in the customer's words]
- **Who is affected:** [role(s), e.g. recruiter, hiring manager, candidate]
- **How often / how many:** [volume, e.g. 300 jobs a month in 12 locales]

---

## 3. Customer impact

| | |
|---|---|
| **This customer** | [what is blocked or degraded; go-live / UAT dates] |
| **Other customers with the same need** | [names or count; SA channel checked: Yes / No] |
| **Workaround discussed** | [what was tried; accepted by customer? temporary until?] |

---

## 4. Requirements

Numbered, observable, testable. Rank them, so priority is set once by the SA owner and not argued per ticket.

| # | Requirement | Priority |
|---|-------------|----------|
| R1 | [Role] can [action] in [place in the product] | Must |
| R2 | System [does X] when [condition] | Must |
| R3 | | Nice to have |

**Non-functional:** [latency, volume, languages / locales — e.g. "job must exist in Workday before it is posted, no 5–10 min delay"]

**Data and compliance:** [Personal or sensitive data involved (e.g. EEO, PII)? Who may see it, consent, retention, which downstream system consumes it. Write "None" if not applicable.]

---

## 5. Expected user journey

**User flow diagram (recommended):** [Miro / Figma / FigJam link]

> Recommended for anything beyond a small change: link a diagram that shows the expected behavior end to end: who does what, what the system does at each step, which systems are involved, and the failure paths. The steps below summarize it so the ticket is readable without opening the link.

1. [User / system does …]
2. [System responds …]
3. [Edge case: what happens if … fails / is rejected / is cancelled]

---

## 6. Acceptance criteria

**Scenario 1: [Brief name]**
- Given [precondition]
- When [action]
- Then [expected result]

**Scenario 2: [Brief name]**
- Given …
- When …
- Then …

*(3–5 scenarios)*

---

## 7. Scope

- **In scope:** [ … ]
- **Out of scope:** [ … ]

---

## 8. Related tickets

- **Duplicates checked:** [search used / "none found"]
- **Related Product Stories / PHEM epics:** [title + key]
- **Implementation tickets:** [title + key]

---

## 9. Teams required

> Same products as the PHEM epic's **Cross-Team Dependencies** table, so Product can reuse it. List every product you believe is needed and why. Use canonical names (CRM, Integration Experience, Automation Engine, Platform Config, Talent Analytics, Notifications / Messaging Platform, Scheduling, Interview Intelligence, …). No UX row. Product confirms this in the review.

| Product | Required (Yes / TBD) | Reason |
|---------|----------------------|--------|
| CRM | | |
| Integration Experience | | |
| Automation Engine | | |
| Platform Config | | |
| Talent Analytics | | |
| _(add products)_ | | |

**External systems involved:** [e.g. Workday, SuccessFactors, customer SFTP — or "None"]

---

## 10. Open questions

| Question | Owner | Status |
|----------|-------|--------|
| | | Open |

---

## 11. Product decision (filled by Product)

> SA leaves this blank. Once the story is approved, **everything moves to the PHEM epic**: requirements breakdown, team stories, the ETA and all delivery communication. This Product Story is only updated to link the epic.

| | |
|---|---|
| **Decision** | Approved / Rejected / Needs info |
| **Decided by, date** | |
| **Owning PM** | |
| **PHEM epic** | [link] |
| **Release window** | Committed on the PHEM epic (R1 / R2) |
| **Reason** (if rejected or needs info) | |

---

## Example

A fully filled example (Siemens Healthineers locale tickets) → `templates/example-product-story.md`.
