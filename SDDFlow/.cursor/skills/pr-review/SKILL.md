---

name: pr-review

description: Review pull requests for code quality, security issues,

  and test coverage. Use when reviewing PRs or preparing code for review.

---

 

# PR Review

 

## Review process

1. Check for security vulnerabilities — inputs validated, no hardcoded

   secrets, no SQL via string concatenation. Cross-reference

   security.mdc.

2. Verify error handling — every async operation in try/catch, errors

   logged with structured fields, user-facing messages don't leak internals.

3. Confirm test coverage — every AC from the spec has a test that

   references it.

4. Review naming — files kebab-case, functions camelCase, types PascalCase.

5. Confirm the diff matches [DESIGN.md](http://DESIGN.md). Flag unexplained deviations.

 

## Output format

Produce a markdown report with sections:

Summary, Blockers, Suggestions, Nits.

Reference exact file:line for every finding.