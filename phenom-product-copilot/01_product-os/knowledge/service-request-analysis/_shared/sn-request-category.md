# ServiceNow request category (SR subcategory)

Source field: `FIVETRAN_DB.SERVICENOW.SN_CUSTOMERSERVICE_CASE.U_REQUEST_CATEGORY`  
Join: `TASK.SYS_ID = CASE.SYS_ID` → `TASK.NUMBER` (CS…).

Used on the RX label sheet as **`SN - Request Category`** (source metadata). It is separate from the `Recommendation …` outputs.

## Service Request subcategory definitions

These are subcategories of the Service Request request type, not peer request types.

| Subcategory | Meaning |
|-------------|---------|
| **Admin Tasks/ EIS Tasks** | Routine administrative or enable/disable work. |
| **Adoption** | Help using existing documented functionality. |
| **Functionality Clarification** | Explanation of how the feature technically works. |
| **Feature Clarification** | Explanation of what a feature does and why it exists. |
| **Service Request - Issue/Question** | Holding value only; never recommend it as the corrected destination. Snowflake may store it as `issue_question`. |

Snowflake also has occasional values that do not belong to the Service Request taxonomy (for example, Problem Management or `product_defect`). Keep them as-is after normalizing known slugs; do not force them into a formal subcategory.

## Related fields

- `U_REQUEST_TYPE` = `Service Request` (population filter)
- `U_TICKET_CLASSIFICATION` / `U_TICKET_CLASSIFICATION_CHILD` — separate closeout taxonomy (sheet: `SN - Classification` / `SN - Classification (Child)`)
