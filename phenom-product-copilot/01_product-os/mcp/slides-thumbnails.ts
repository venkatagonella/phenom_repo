/**
 * Download thumbnails of every slide in a Google Slides deck.
 * Usage: npx tsx slides-thumbnails.ts <presentationId> <outDir>
 *
 * Used by the phenom-slide-creator skill to capture the canonical template
 * deck as pixel-reference targets for the HTML component library.
 */
import { FileCredentialProvider } from "./src/auth/file-credential-provider.ts";
import { mkdir, writeFile } from "fs/promises";

const presId = process.argv[2];
const outDir = process.argv[3];
if (!presId || !outDir) throw new Error("Usage: slides-thumbnails.ts <presentationId> <outDir>");

const cred = new FileCredentialProvider();
const row = await cred.getCredentials("google");
if (!row?.access_token) throw new Error("Google not connected.");
const token = row.access_token;

async function api<T>(path: string): Promise<T> {
  const res = await fetch(`https://slides.googleapis.com/v1${path}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`${res.status}: ${text}`);
  return JSON.parse(text) as T;
}

await mkdir(outDir, { recursive: true });

const pres = await api<{ slides: Array<{ objectId: string }> }>(
  `/presentations/${presId}?fields=slides(objectId)`
);

console.log(`Deck has ${pres.slides.length} slides. Downloading thumbnails to ${outDir}`);

let i = 0;
for (const slide of pres.slides) {
  i++;
  const thumb = await api<{ contentUrl: string }>(
    `/presentations/${presId}/pages/${slide.objectId}/thumbnail?thumbnailProperties.mimeType=PNG&thumbnailProperties.thumbnailSize=LARGE`
  );
  const img = await fetch(thumb.contentUrl);
  const buf = Buffer.from(await img.arrayBuffer());
  const name = `slide-${String(i).padStart(2, "0")}.png`;
  await writeFile(`${outDir}/${name}`, buf);
  console.log(`✓ ${name} (${slide.objectId})`);
}

console.log("Done.");
