import { readTokenStore } from "./src/auth/token-store.ts";

const store = await readTokenStore();
const token = store.google?.access_token;
if (!token) throw new Error("No google token");

const id = "1sL7hBtUoc4QsqfpdqYo-TqvOdpjHcrjI9oit2cbS-Q4";
const res = await fetch(`https://slides.googleapis.com/v1/presentations/${id}?fields=slides(objectId,slideProperties(layoutObjectId,masterObjectId))`, {
  headers: { Authorization: `Bearer ${token}` },
});
const data = await res.json();
for (const s of data.slides ?? []) {
  console.log(`${s.objectId}  layout=${s.slideProperties?.layoutObjectId}  master=${s.slideProperties?.masterObjectId}`);
}
