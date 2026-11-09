import { readTokenStore } from "./src/auth/token-store.ts";
import { readFile } from "fs/promises";

const store = await readTokenStore();
const token = store.google?.access_token;
if (!token) throw new Error("No google token");

const PRES_ID = "1sL7hBtUoc4QsqfpdqYo-TqvOdpjHcrjI9oit2cbS-Q4";

const specPath = process.argv[2];
if (!specPath) throw new Error("Usage: rebuild-deck.ts <spec.json>");
const spec = JSON.parse(await readFile(specPath, "utf-8")) as {
  keep_first: number;
  slides: Array<{ title: string; body: string; notes?: string }>;
};

const SLIDE_W = 9144000;
const SLIDE_H = 5143500;
const MARGIN_X = 457200;
const TITLE_Y = 304800;
const TITLE_H = 685800;
const BODY_Y = TITLE_Y + TITLE_H + 152400;
const BODY_H = SLIDE_H - BODY_Y - 304800;
const CONTENT_W = SLIDE_W - 2 * MARGIN_X;

async function api(path: string, body?: unknown, method = "POST") {
  const res = await fetch(`https://slides.googleapis.com/v1${path}`, {
    method,
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`${res.status}: ${text}`);
  return text ? JSON.parse(text) : {};
}

const pres = await api(`/presentations/${PRES_ID}?fields=slides(objectId)`, undefined, "GET");
const currentIds: string[] = pres.slides.map((s: any) => s.objectId);
const toDelete = currentIds.slice(spec.keep_first);

let uid = 0;
const nid = (p: string) => `${p}_${Date.now().toString(36)}_${uid++}`;

const requests: any[] = [];

for (const id of toDelete) {
  requests.push({ deleteObject: { objectId: id } });
}

const createdSlides: Array<{ slideId: string; notes?: string }> = [];

for (const [i, s] of spec.slides.entries()) {
  const sid = nid("slide");
  const tid = nid("title");
  const bid = nid("body");

  requests.push({
    createSlide: {
      objectId: sid,
      insertionIndex: spec.keep_first + i,
    },
  });

  requests.push({
    createShape: {
      objectId: tid,
      shapeType: "TEXT_BOX",
      elementProperties: {
        pageObjectId: sid,
        size: { width: { magnitude: CONTENT_W, unit: "EMU" }, height: { magnitude: TITLE_H, unit: "EMU" } },
        transform: { scaleX: 1, scaleY: 1, translateX: MARGIN_X, translateY: TITLE_Y, unit: "EMU" },
      },
    },
  });
  requests.push({ insertText: { objectId: tid, text: s.title, insertionIndex: 0 } });
  requests.push({
    updateTextStyle: {
      objectId: tid,
      style: { fontSize: { magnitude: 22, unit: "PT" }, bold: true, foregroundColor: { opaqueColor: { rgbColor: { red: 0.13, green: 0.13, blue: 0.18 } } } },
      textRange: { type: "ALL" },
      fields: "fontSize,bold,foregroundColor",
    },
  });

  requests.push({
    createShape: {
      objectId: bid,
      shapeType: "TEXT_BOX",
      elementProperties: {
        pageObjectId: sid,
        size: { width: { magnitude: CONTENT_W, unit: "EMU" }, height: { magnitude: BODY_H, unit: "EMU" } },
        transform: { scaleX: 1, scaleY: 1, translateX: MARGIN_X, translateY: BODY_Y, unit: "EMU" },
      },
    },
  });
  requests.push({ insertText: { objectId: bid, text: s.body, insertionIndex: 0 } });
  requests.push({
    updateTextStyle: {
      objectId: bid,
      style: { fontSize: { magnitude: 11, unit: "PT" }, foregroundColor: { opaqueColor: { rgbColor: { red: 0.2, green: 0.2, blue: 0.2 } } } },
      textRange: { type: "ALL" },
      fields: "fontSize,foregroundColor",
    },
  });
  requests.push({
    updateParagraphStyle: {
      objectId: bid,
      style: { lineSpacing: 115, spaceBelow: { magnitude: 4, unit: "PT" } },
      textRange: { type: "ALL" },
      fields: "lineSpacing,spaceBelow",
    },
  });

  createdSlides.push({ slideId: sid, notes: s.notes });
}

console.log(`Deleting ${toDelete.length} slides, creating ${spec.slides.length}, total requests: ${requests.length}`);
await api(`/presentations/${PRES_ID}:batchUpdate`, { requests });
console.log("✓ Slides rewritten");

const withNotes = createdSlides.filter((s) => s.notes);
if (withNotes.length > 0) {
  const updated = await api(
    `/presentations/${PRES_ID}?fields=slides(objectId,slideProperties(notesPage(pageElements(objectId,shape(placeholder(type))))))`,
    undefined,
    "GET"
  );
  const notesReqs: any[] = [];
  for (const meta of withNotes) {
    const slide = updated.slides?.find((s: any) => s.objectId === meta.slideId);
    if (!slide) continue;
    const notesShape = slide.slideProperties?.notesPage?.pageElements?.find(
      (el: any) => el.shape?.placeholder?.type === "BODY"
    );
    if (notesShape) {
      notesReqs.push({ insertText: { objectId: notesShape.objectId, text: meta.notes, insertionIndex: 0 } });
    }
  }
  if (notesReqs.length > 0) {
    await api(`/presentations/${PRES_ID}:batchUpdate`, { requests: notesReqs });
    console.log(`✓ Added speaker notes to ${notesReqs.length} slides`);
  }
}

console.log("Done.");
