# Vanilla API reference — drafts and reads

Base URL `https://community.phenom.com/api/v2`. Auth: `Authorization: Bearer <token>` from `~/.copilot/tokens.json` → `vanilla.access_token`.

**Cloudflare:** requests without a browser `User-Agent` are rejected with error 1010. `scripts/kb_draft.py` sets one.

---

## The draft mechanism

Vanilla stores unpublished work as **drafts** (`POST /drafts`), separate from live articles. A draft:

- has `draftStatus: "draft"` and is not visible to customers
- is private to the author
- opens in the Vanilla article editor via its `editUrl`
- is deleted with `DELETE /drafts/{draftID}`
- **does not become an article until a human saves/publishes it in the editor**

This is why the skill can write to Vanilla without any publishing risk.

### Create a draft

`POST /drafts`

```json
{
  "recordType": "article",
  "recordID": 12165,
  "attributes": {
    "name": "LinkedIn CRM Connect",
    "body": "## What is…",
    "format": "markdown",
    "knowledgeCategoryID": 970,
    "knowledgeBaseID": 3
  }
}
```

| Field | Notes |
|-------|-------|
| `recordType` | `"article"` |
| `recordID` | **Omit for a new article.** Set to the article ID to stage a new version of an existing one. |
| `attributes.body` | **Required.** Empty body fails validation. |
| `attributes.format` | One of `rich`, `bbcode`, `markdown`, `html`, `wysiwyg`, `text`, `textex`, `rich2`. Vanilla's own editor writes `rich2` (a Slate-style JSON structure); `markdown` is far easier to author and is accepted. |
| `attributes.knowledgeCategoryID` | Determines where the article would live. Look it up with `categories --kb N`. |

Response includes `draftID`, `draftStatus`, and (for drafts on an existing article) `editUrl`:

```
https://community.phenom.com/kb/articles/{articleID}/editor?draftID={draftID}&knowledgeBaseID=…&knowledgeCategoryID=…
```

### Read endpoints used

| Endpoint | Purpose |
|----------|---------|
| `GET /search?query=…&recordTypes[]=article&knowledgeBaseID=N` | Find articles. Returns `recordID` (= article ID); `articleID` is often null in search results. |
| `GET /articles/{id}` | Full article. `body` is HTML. Also returns `status`, `knowledgeCategoryID`, `knowledgeBaseID`, `dateUpdated`. |
| `GET /articles/{id}/revisions` | Revision history with authors and dates — useful for judging staleness. |
| `GET /knowledge-bases` | KB IDs. |
| `GET /knowledge-categories?limit=100&page=N&expand=knowledgeBase` | Paginated; filter client-side by KB. |
| `GET /drafts?recordType=article` | Your pending drafts. |

---

## Never call these

| Endpoint | Effect |
|----------|--------|
| `POST /articles` | Creates a **live** article |
| `PATCH /articles/{id}` | Edits a **live** article |
| `PATCH /articles/{id}/status` | Publishes / unpublishes |

`scripts/kb_draft.py` refuses these at the request layer. Do not work around it with raw `curl` or ad-hoc Python.

---

## Gotchas

- **`GET /open-api/v3` returns 403** for this token — the schema isn't introspectable. Learn field requirements by sending a deliberately invalid payload and reading the validation error.
- **Invalid `recordType` values still create a draft.** Validation on `recordType` is loose, so a typo produces a junk draft. Always pass `"article"`, and clean up with `delete-draft` if one slips through.
- **Search results use `recordID`,** not `articleID`. The script normalises this.
- **`format` is not returned** by `GET /articles/{id}` or `/revisions`, so you cannot detect an existing article's format from the API. Markdown drafts are the safe default.
- **Category IDs repeat across knowledge bases in listings** — always filter by `--kb`.

## Useful IDs

| Purpose | ID |
|---------|-----|
| CRM knowledge base | kb 3 |
| CRM > Candidate Management > LinkedIn CRM Connect | category 970 |
| Screening knowledge base (house-style reference) | kb 29 |
| Article Drafts (INTERNAL) staging KB | kb 20 |
| Article Drafts > CRM | category 233 |
