import { readTokenStore } from "./src/auth/token-store.ts";

const store = await readTokenStore();
const token = store.google?.access_token;
if (!token) throw new Error("No google token");

const id = "1sL7hBtUoc4QsqfpdqYo-TqvOdpjHcrjI9oit2cbS-Q4";
const res = await fetch(`https://slides.googleapis.com/v1/presentations/${id}?fields=layouts(objectId,layoutProperties(displayName,name),pageElements(shape(placeholder(type)))),masters(objectId,masterProperties(displayName))`, {
  headers: { Authorization: `Bearer ${token}` },
});
const data = await res.json();
for (const m of data.masters ?? []) {
  console.log(`MASTER ${m.objectId} ${m.masterProperties?.displayName ?? ""}`);
}
console.log("---");
for (const layout of data.layouts ?? []) {
  const placeholders = (layout.pageElements ?? []).map((el: any) => el.shape?.placeholder?.type).filter(Boolean);
  console.log(`${layout.objectId}\t${layout.layoutProperties?.displayName ?? ""}\t${layout.layoutProperties?.name ?? ""}\t[${placeholders.join(",")}]`);
}
