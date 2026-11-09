/**
 * build-gslides.ts — Build a Phenom-branded Google Slides deck by DUPLICATING the
 * canonical template ("Product - Slide Bank for Cursor") and filling placeholders.
 * This preserves 100% of the template's design (shapes, colors, diagrams).
 *
 * Usage:  npx tsx build-gslides.ts <spec.json>
 *
 * Two modes:
 *   A) IN-PLACE (works with current scopes): user makes a copy of the template in
 *      Google Drive (File ▸ Make a copy) and passes its ID as "deckId". The script
 *      edits that copy in place — keeps chosen slides, deletes the rest, fills text.
 *   B) AUTO-COPY (needs Drive write scope): omit "deckId" and the script copies the
 *      template itself. Requires the Google connection to include a Drive write scope
 *      (drive.file or drive). With read-only Drive this returns a clear error.
 *
 * Spec format:
 * {
 *   "deckName": "My Deck",              // used to rename the deck (auto-copy mode)
 *   "deckId": "1AbC...",               // optional; an existing copy to edit IN PLACE
 *   "templateId": "1r1Wq...",          // optional; defaults to TEMPLATE_ID below
 *   "slides": [
 *     {
 *       "template": 1,                   // 1-based index of the template slide to clone
 *       "replace": {                     // exact-string replacements (placeholders)
 *         "[Section]": "Product Innovation",
 *         "Cursor & Claude Skills": "Q3 Board Review"
 *       },
 *       "body": "Optional long paragraph that replaces the slide's lorem-ipsum body.",
 *       "notes": "Optional speaker notes."
 *     }
 *   ]
 * }
 *
 * Notes:
 *  - `replace` uses Slides replaceAllText scoped to the single cloned slide, so the
 *    same placeholder string on other slides is unaffected.
 *  - `body` replaces the longest lorem-ipsum text box on that slide (for prose slides).
 *  - The template's built-in colors are preserved. Per-section color rotation in the
 *    Google route relies on choosing template slides that already carry the right tint.
 */
import { FileCredentialProvider } from "./src/auth/file-credential-provider.ts";
import { readFile } from "fs/promises";

const TEMPLATE_ID = "1r1WqCfvohkmfjEdmjzd0pJiFYznxPElyi4IWEZuaWNg";

interface SpecSlide {
  template: number;
  replace?: Record<string, string>;
  /** Position-ordered fill for repeated placeholders (metrics, cards, timeline…).
   *  e.g. { "100,000": ["4,123","$4M","150%"], "[Metric]": ["Interviews","Saved","Lift"] }
   *  Shapes containing the token are sorted top-to-bottom, then left-to-right, and the
   *  i-th shape gets the i-th value. */
  items?: Record<string, string[]>;
  body?: string;
  notes?: string;
}
interface Spec {
  deckName: string;
  deckId?: string;
  templateId?: string;
  slides: SpecSlide[];
}

const specPath = process.argv[2];
if (!specPath) throw new Error("Usage: build-gslides.ts <spec.json>");
const spec = JSON.parse(await readFile(specPath, "utf-8")) as Spec;
const templateId = spec.templateId ?? TEMPLATE_ID;

const cred = new FileCredentialProvider();
const row = await cred.getCredentials("google");
if (!row?.access_token) throw new Error("Google not connected.");
const token = row.access_token;

async function slides<T>(path: string, body?: unknown, method = "POST"): Promise<T> {
  const res = await fetch(`https://slides.googleapis.com/v1${path}`, {
    method,
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`Slides ${res.status}: ${text}`);
  return (text ? JSON.parse(text) : {}) as T;
}
async function drive<T>(path: string, body?: unknown, method = "POST"): Promise<T> {
  const res = await fetch(`https://www.googleapis.com/drive/v3${path}`, {
    method,
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`Drive ${res.status}: ${text}`);
  return (text ? JSON.parse(text) : {}) as T;
}

// 1. Obtain the working deck -----------------------------------------------------
let newId: string;
if (spec.deckId) {
  // IN-PLACE mode — edit the copy the user already made.
  newId = spec.deckId;
  console.log(`Editing existing copy in place: ${newId}`);
} else {
  // AUTO-COPY mode — needs Drive write scope.
  console.log(`Copying template ${templateId} → "${spec.deckName}"`);
  try {
    const copy = await drive<{ id: string }>(`/files/${templateId}/copy`, { name: spec.deckName });
    newId = copy.id;
    console.log(`✓ New deck: ${newId}`);
  } catch (e: any) {
    if (/SCOPE_INSUFFICIENT|PERMISSION_DENIED|403/.test(String(e?.message))) {
      throw new Error(
        "Drive write scope missing — cannot auto-copy the template.\n" +
          "Fix: in Google Drive open the template, File ▸ Make a copy, then re-run with\n" +
          '  "deckId": "<the new copy\'s id>"  in the spec (in-place mode).\n' +
          "Template: https://docs.google.com/presentation/d/" + templateId + "/edit"
      );
    }
    throw e;
  }
}

// 2. Read the cloned deck's slide object IDs (mirrors template order) -------------
const cloned = await slides<{ slides: Array<{ objectId: string }> }>(
  `/presentations/${newId}?fields=slides(objectId)`,
  undefined,
  "GET"
);
const templateIds = cloned.slides.map((s) => s.objectId);

// 3. Duplicate the chosen template slides, in spec order -------------------------
let uid = 0;
const nid = (p: string) => `${p}_${Date.now().toString(36)}_${uid++}`;
const build: any[] = [];
const newSlideIds: string[] = [];

for (const s of spec.slides) {
  const src = templateIds[s.template - 1];
  if (!src) throw new Error(`Template slide ${s.template} out of range (deck has ${templateIds.length}).`);
  const dupId = nid("slide");
  newSlideIds.push(dupId);
  build.push({ duplicateObject: { objectId: src, objectIds: { [src]: dupId } } });
}

// 4. Move the duplicates to the front, in order ---------------------------------
build.push({ updateSlidesPosition: { slideObjectIds: newSlideIds, insertionIndex: 0 } });

// 5. Delete the original template slides -----------------------------------------
for (const id of templateIds) build.push({ deleteObject: { objectId: id } });

// 6. Scoped placeholder replacements --------------------------------------------
for (const [i, s] of spec.slides.entries()) {
  for (const [find, replaceText] of Object.entries(s.replace ?? {})) {
    build.push({
      replaceAllText: {
        pageObjectIds: [newSlideIds[i]],
        containsText: { text: find, matchCase: true },
        replaceText,
      },
    });
  }
}

console.log(`Duplicating ${spec.slides.length} slides, deleting ${templateIds.length}, ${build.length} requests…`);
await slides(`/presentations/${newId}:batchUpdate`, { requests: build });
console.log("✓ Structure + placeholders done");

// 7. Per-item (repeated placeholder) + body (lorem) replacement ------------------
const editSlides = spec.slides
  .map((s, i) => ({ s, id: newSlideIds[i] }))
  .filter((x) => x.s.body || x.s.items);

if (editSlides.length > 0) {
  type El = {
    objectId: string;
    transform?: { translateX?: number; translateY?: number };
    shape?: { text?: { textElements?: Array<{ textRun?: { content?: string } }> } };
  };
  const full = await slides<{ slides: Array<{ objectId: string; pageElements?: El[] }> }>(
    `/presentations/${newId}?fields=slides(objectId,pageElements(objectId,transform,shape(text(textElements(textRun(content))))))`,
    undefined,
    "GET"
  );
  const textOf = (el: El) => (el.shape?.text?.textElements ?? []).map((t) => t.textRun?.content ?? "").join("");
  const editReqs: any[] = [];

  for (const { s, id } of editSlides) {
    const slide = full.slides.find((sl) => sl.objectId === id);
    if (!slide) continue;
    const els = slide.pageElements ?? [];
    const consumed = new Set<string>();

    // 7a. Position-ordered items
    for (const [token, values] of Object.entries(s.items ?? {})) {
      const matches = els
        .filter((el) => textOf(el).includes(token))
        .sort((a, b) => {
          const ay = a.transform?.translateY ?? 0, by = b.transform?.translateY ?? 0;
          if (Math.abs(ay - by) > 50000) return ay - by; // different row
          return (a.transform?.translateX ?? 0) - (b.transform?.translateX ?? 0);
        });
      for (let i = 0; i < Math.min(matches.length, values.length); i++) {
        editReqs.push({ deleteText: { objectId: matches[i].objectId, textRange: { type: "ALL" } } });
        editReqs.push({ insertText: { objectId: matches[i].objectId, text: values[i], insertionIndex: 0 } });
        consumed.add(matches[i].objectId);
      }
    }

    // 7b. Body — longest remaining lorem box
    if (s.body) {
      let best: { objectId: string; len: number } | null = null;
      for (const el of els) {
        if (consumed.has(el.objectId)) continue;
        const txt = textOf(el);
        if (/lorem ipsum/i.test(txt) && (!best || txt.length > best.len)) best = { objectId: el.objectId, len: txt.length };
      }
      if (best) {
        editReqs.push({ deleteText: { objectId: best.objectId, textRange: { type: "ALL" } } });
        editReqs.push({ insertText: { objectId: best.objectId, text: s.body, insertionIndex: 0 } });
      }
    }
  }
  if (editReqs.length > 0) {
    await slides(`/presentations/${newId}:batchUpdate`, { requests: editReqs });
    console.log(`✓ Filled items/body (${editReqs.length / 2} text edits)`);
  }
}

// 8. Speaker notes ---------------------------------------------------------------
const noteSlides = spec.slides
  .map((s, i) => ({ s, id: newSlideIds[i] }))
  .filter((x) => x.s.notes);

if (noteSlides.length > 0) {
  const withNotes = await slides<{
    slides: Array<{
      objectId: string;
      slideProperties?: { notesPage?: { pageElements?: Array<{ objectId: string; shape?: { placeholder?: { type?: string } } }> } };
    }>;
  }>(
    `/presentations/${newId}?fields=slides(objectId,slideProperties(notesPage(pageElements(objectId,shape(placeholder(type))))))`,
    undefined,
    "GET"
  );
  const noteReqs: any[] = [];
  for (const { s, id } of noteSlides) {
    const slide = withNotes.slides.find((sl) => sl.objectId === id);
    const shape = slide?.slideProperties?.notesPage?.pageElements?.find(
      (el) => el.shape?.placeholder?.type === "BODY"
    );
    if (shape) noteReqs.push({ insertText: { objectId: shape.objectId, text: s.notes, insertionIndex: 0 } });
  }
  if (noteReqs.length > 0) {
    await slides(`/presentations/${newId}:batchUpdate`, { requests: noteReqs });
    console.log(`✓ Added speaker notes to ${noteReqs.length} slides`);
  }
}

console.log(`\nDone. https://docs.google.com/presentation/d/${newId}/edit`);
