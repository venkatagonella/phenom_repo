# Example Product Story (filled template)

> Dummy example showing a complete SA Product Story. Based on the Siemens Healthineers locale tickets (ISHIC1S-909, -919, -1130, -1134). Values in `[brackets]` were not in the original tickets and are placeholders.

---

**Title:** `Siemens Healthineers – Job creation – Publish jobs to all locales with job details copied`

---

## 1. Summary

Siemens recruiters need one action to publish a job to all locales with its details copied, so every global position is available in every locale without manual rework.

---

## 2. Customer problem

- **What happens today:** "We hire globally and want every position available in all locales. Today, every job needs dozens of manual clicks and copy-pastes before it is live everywhere."
- **Who is affected:** Recruiters creating jobs, manually or from a job template
- **How often / how many:** 24 clicks per job to select locales, plus 24 copy-paste operations and 24 clicks to copy job details. [Jobs created per month: to confirm]

---

## 3. Customer impact

| | |
|---|---|
| **This customer** | Recruiter time per job; risk of jobs going live in only some locales. [UAT / go-live dates: to confirm] |
| **Other customers with the same need** | [Names or count — SA channel checked: Yes / No] |
| **Committed to the customer?** | [No / Yes — by whom, when, where documented] |
| **Workaround discussed** | Uncheck and re-check External and Internal on the review page. This replaces the default English (Global) locale with all locales. Job details still have to be copied by hand. Accepted as temporary. |

---

## 4. Requirements

| # | Requirement | Priority |
|---|-------------|----------|
| R1 | Recruiter can publish a job to all locales in one action (all locales selected by default, or a "Publish to all locales" option) | Must |
| R2 | Recruiter can copy job title, job category, job description, required skills and experience, and benefits to all locales in one action | Must |
| R3 | R1 and R2 work for manually created jobs **and** jobs created from templates | Must |
| R4 | Recruiter can still edit a single locale after copying | Nice to have |

**Non-functional:** Works for all locales configured for the tenant [count: to confirm]; no change to posting time.

**Data and compliance:** None (no personal or sensitive data).

---

## 5. Expected user journey

**User flow diagram (recommended):** [Miro link — job creation to posting, all locales]

1. Recruiter creates a job, manually or from a template, in the default locale.
2. Recruiter selects "Copy details to all locales". The system copies title, category, description, required skills and experience, and benefits to every configured locale.
3. On the review page, all locales are selected for publishing (or the recruiter selects "Publish to all locales").
4. Recruiter publishes. The job goes live in every locale.
5. Edge case: a locale already has its own content. The system asks before overwriting it.
6. Edge case: the tenant has only one locale. The copy and publish-all options are hidden.

---

## 6. Acceptance criteria

**Scenario 1: Publish a manual job to all locales**
- Given a recruiter has created a job manually
- When they open the review page
- Then all configured locales can be selected for publishing in one action

**Scenario 2: Publish a template-based job to all locales**
- Given a recruiter has created a job from a template
- When they open the review page
- Then the same one-action option to publish to all locales is available

**Scenario 3: Copy job details to all locales**
- Given a job has title, category, description, required skills and experience, and benefits filled in one locale
- When the recruiter selects "Copy details to all locales"
- Then those five fields are filled identically in every configured locale

**Scenario 4: Existing locale content**
- Given a locale already has its own job description
- When the recruiter copies details to all locales
- Then the system asks for confirmation before overwriting that locale

---

## 7. Scope

- **In scope:** Locale selection and copying of the five job-detail fields, for manual and template-based jobs
- **Out of scope:** Automatic translation of job content; copying custom fields beyond the five listed

---

## 8. Related tickets

- **Duplicates checked:** `project = ISHIC1S AND text ~ "locales"` and PHEM epics for "all locales"
- **Related Product Stories / PHEM epics:** Replaces ISHIC1S-909, ISHIC1S-919, ISHIC1S-1130, ISHIC1S-1134 (close as duplicates and link here)
- **Implementation tickets:** [key]

---

## 9. Teams required

| Product | Required (Yes / TBD) | Reason |
|---------|----------------------|--------|
| CRM | Yes | "Publish to all locales" on the review job page; default locale selection |
| HRM | Yes | Copy job details to all locales, for manual and template-based job creation |
| Platform Config | TBD | Only if "all locales by default" should be a tenant setting |

**External systems involved:** None

---

## 10. Open questions

| Question | Owner | Status |
|----------|-------|--------|
| Should all locales be selected by default, or offered as a "Publish to all locales" option? | SA with customer | Open |
| Should "all locales by default" be configurable per tenant? | Product (CRM) | Open |
| Does "all locales" mean all locales configured for the tenant? | SA | Open |
