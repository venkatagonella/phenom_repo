# Confidence and PM review

The authoritative confidence and review policy is
[`../rulebook.md` §7](../rulebook.md#7-confidence-and-pm-review).

Current sheet outputs:

| Output | Values |
|--------|--------|
| Recommendation Conficence Level | `high` · `medium` · `low` |
| Recommendation PM Review Required | `TRUE` · `FALSE` |
| Recommendation Status | `proposed` · `reviewed` |

Do not use the retired `label_status = needs_review`, numeric confidence, or Platform-remap fields.
Thin evidence alone follows `E-THIN`: confidence `low`, reasoning starts with “Insufficient evidence —”,
and PM Review Required remains `FALSE` unless another real ambiguity exists.
