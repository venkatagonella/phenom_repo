# Adapting for another product experience

## Reuse as-is

- SN-first funnel and layers A–D
- Snowflake join (`SYS_ID` = `U_CASE_NUMBER_VALUE` → `U_JIRA_KEY`)
- [sql-templates.md](sql-templates.md)
- Shared type rules in `knowledge/service-request-analysis/_shared/type-rules.md`

## Extend (do not fork the skill)

1. Add or fill `knowledge/service-request-analysis/<pe>/` (`areas.md`, then `packages.md`, optional `label-sheet.md`).
2. Confirm exact `U_PRODUCT_EXPERIENCE` in Snowflake; write it into that PE’s `areas.md`.
3. Add the PE to the intake table in [SKILL.md](SKILL.md).
4. Run A–D once; only then optionally create a label sheet for a contested slice.

## Do not

- Put growing PE rules into `SKILL.md`
- Copy RX escalation numbers to another PE
- Use a label sheet as the population source
