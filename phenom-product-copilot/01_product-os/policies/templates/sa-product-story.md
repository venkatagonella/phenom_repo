# SA Product Story Template

> For **Product Stories created by Solution Architects** in customer / implementation projects (e.g. `ISHIC1S-…`, `IDPRP-…`).
> Copy into the Product Story description (markdown). Rules → `policies/jira-story-rules.md` → "SA Product Stories".
>
> **Before you create a new ticket**
> 1. **Search first.** Is there already a Product Story or PHEM epic for this need — for this customer *or another one*? If yes, comment and link there. Do **not** open a second ticket.
> 2. **One need = one Product Story.** Do not split it by team (CRM, HRM, IX). Product breaks it into team stories inside the PHEM epic.
> 3. **No ETA here.** The ETA is committed on the PHEM epic once the work is planned ("in staging / production by R1 or R2").
>
> **Title:** `[Customer] – [Product area] – [Need in plain words]`
> e.g. `Siemens Healthineers – Job creation – Publish template-based jobs to all configured locales`
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
| **Workaround discussed** | [what was presented to the customer, what was the push back? List three workarounds.] |

---

## 4. Requirements

Numbered, observable, testable. Rank them, so priority is set once by the SA owner and not argued per ticket.

| # | Requirement | Priority |
|---|-------------|----------|
| R1 | [Role] can [action] in [place in the product] | Must |
| R2 | System [does X] when [condition] | Must |
| R3 | ... | Nice to have |

**Non-functional:** [latency, volume, languages / locales — e.g. "job must exist in Workday before it is posted, ..."]

**Data and compliance:** [Personal or sensitive data involved (e.g. EEO, PII)? Who may see it, consent, retention, which downstream system consumes it. Write "None" if not applicable.]

---

## 5. Expected user journey

Step by step in the system, including the failure paths.

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

---

## 9. Systems and teams required

[Which products / integrations you believe are involved — e.g. CRM, HRM, Integration Experience, Automation Engine, Workday. Product confirms this in the review.]

---

## 10. Open questions

| Question | Owner | Status |
|----------|-------|--------|
| | | Open |

---

## For Product (filled at review — SA leaves blank)

| | |
|---|---|
| **Quality gate** | Green / Amber / Red — [what is missing] |
| **AI pre-review** | Completeness · feasibility from code · teams needed · suggested owner |
| **Decision** | Yes / No / Needs info — [date, by whom] |
| **Owning PM** | |
| **PHEM epic** | [key] — team stories: [CRM …, HRM …] |
| **Committed ETA** | Set on the PHEM epic only |

---

## SA checklist before submitting

- [ ] Searched for existing stories / epics for the same need (this and other customers)
- [ ] One need, one ticket. Not split by team
- [ ] Problem written in the customer's words, readable without the call
- [ ] Customer impact filled: this customer, others, commitment status
- [ ] Requirements numbered and ranked (Must / Nice to have)
- [ ] User journey covers the failure paths
- [ ] 3–5 acceptance criteria (Given / When / Then)
- [ ] Attachments added; no ETA in the ticket

## Review rubric (Product)

| Rating | Meaning | Next step |
|--------|---------|-----------|
| **Green** | All sections clear; requirements testable; journey and impact complete | To decision |
| **Amber** | Gaps in requirements, journey or impact | SA adds detail, re-review |
| **Red** | Duplicate, unclear problem, or not usable | SA rewrites or links to existing ticket |

---

## Example — Siemens Healthineers (how it should have been)

> Today this need sits in four Product Stories (ISHIC1S-909, -919, -1130, -1134) with different owners, ETAs and priorities. It should be **one** story.

**Title:** `Siemens Healthineers – Job creation – Publish template-based jobs to all configured locales, with job details copied`

**Title:** `Siemens Healthineers – Job creation – Publish jobs to all locales with job details copied`

**Summary:** Siemens hires globally and wants every job available in all locales. Recruiters need one action to publish a job to all locales with its details copied, for both manually created and template-based jobs.

**Customer problem:** Selecting locales takes 24 clicks per job. Copying title, category, description, required skills and experience, and benefits takes another 24 copy-paste operations plus 24 clicks, even when the posting language is the same.

**Workaround discussed:** Uncheck and re-check External and Internal on the review page. This replaces the default English (Global) locale with all locales. Job details still have to be copied by hand.

**Requirements (ranked)**

| # | Requirement | Priority |
|---|-------------|----------|
| R1 | Recruiter can publish a job to all locales in one action (all locales selected by default, or a "Publish to all locales" option) | Must |
| R2 | Recruiter can copy job title, category, description, required skills and experience, and benefits to all locales in one action | Must |
| R3 | R1 and R2 work for manually created jobs **and** jobs created from templates | Must |

**Systems and teams (SA's view):** CRM (job posting), HRM (job creation / templates)

**Related tickets:** replaces ISHIC1S-909, ISHIC1S-919, ISHIC1S-1130, ISHIC1S-1134 (close as duplicates, link here)

> **What went wrong in the originals:** 1130 and 1134 only say "same as 909 / 919, but for templates". 919 lists three fields to copy and 1134 lists five. As of Oct 9, 909 and 919 are on hold, 1130 is in Story Elaboration and 1134 is in Development, with three different assignees.
