#!/usr/bin/env python3
"""Build a Claude Slides artifact deck (project/deck.json + project/slides/*.html) from a JSON spec.

Usage:  python3 build_deck.py spec.json <out-root>
Then publish <out-root>/project/deck.json with the Artifact tool (root=<out-root>, files=the slide files).

Output is the Artifact Slides HTML subset: one <section> per slide, inline px styles only, 1920x1080.
Styles: leadership-editorial (default) and corporate-template. Layouts: cover, divider, statement, cards,
tiles, steps, triptych, table, compare, rows, stats, split, takeaway, custom. Any slide may add "callout",
"source" and "notes". See STYLE.md for when to use which.
"""
import html, json, os, re, sys
from datetime import datetime, timezone

STYLES = {
    "leadership-editorial": dict(
        paper="#F2F0EA", card="#FFFFFF", ink="#141416", body="#414241", muted="#8A8A8A", navy="#22224B",
        kicker="#373775", black="#141416", mauve="#A67D8B", rule="#D6D3CB",
        tints=["#EDE0C3", "#EEDDD9", "#DDDDEA", "#FFFFFF", "#DDE3D5"],
        strong=["#CEA667", "#C9A49A", "#77779F", "#8A9A7B"],
        serif="'Fraunces', Georgia, serif", sans="'DM Sans', Arial, sans-serif",
        faces={"fraunces": {"family": "Fraunces", "href": "https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,600;1,600&display=swap"},
               "dm-sans": {"family": "DM Sans", "href": "https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap"}},
    ),
    "summit-mono": dict(
        paper="#FFFFFF", card="#FCF1E9", ink="#141416", body="#3A3A3A", muted="#6B6B6B", navy="#0B0B0B",
        kicker="#141416", black="#0B0B0B", mauve="#E88050", rule="#D9D9D9", accent="#E88050",
        tints=["#FCF1E9", "#F3F0FA", "#EAF5F3", "#FFFFFF"],
        strong=["#E88050", "#E8B058", "#C8C0F0", "#B9DED8"],
        serif="'Fraunces', Georgia, serif", sans="'IBM Plex Sans', Arial, sans-serif",
        faces={"fraunces": {"family": "Fraunces", "href": "https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,600;1,600&display=swap"},
               "ibm-plex-sans": {"family": "IBM Plex Sans", "href": "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&display=swap"},
               "poppins": {"family": "Poppins", "href": "https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap"}},
    ),
    "corporate-template": dict(
        paper="#FFFFFF", card="#F2F2F3", ink="#1A1C2E", body="#434343", muted="#6B6B73", navy="#131A4A",
        kicker="#4543D9", black="#0A0D37", mauve="#426C68", rule="#E4E4E8",
        tints=["#DAF3F2", "#F6E2D5", "#FAEDD7", "#E9E6F9"],
        strong=["#64A39C", "#D36238", "#DDA04A", "#4543D9"],
        serif="'Poppins', Arial, sans-serif", sans="'Poppins', Arial, sans-serif",
        faces={"poppins": {"family": "Poppins", "href": "https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap"}},
    ),
}
STATUS = {"green": "#2F7A4F", "amber": "#A86A12", "red": "#B23A32", "unknown": "#6B6B6B"}

def esc(s): return html.escape(str(s), quote=False)

def rich(s):
    """Escape, then allow *italic* and **bold** markers."""
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\*(.+?)\*", r"<i>\1</i>", s)
    s = re.sub(r"\{(.+?)\}", r'<span style="color:ACCENT">\1</span>', s)
    return s

class Deck:
    def __init__(self, spec):
        self.spec = spec
        self.T = STYLES[spec.get("style", "leadership-editorial")]
        self.rail = spec.get("rail", False)
        self.logo = spec.get("logo", {})  # {"dark": "/_blob/..", "light": "/_blob/.."}
        self.name = spec.get("rail_label", spec["title"]).upper()
        self.left = 160 if self.rail else 128

    # ---------- chrome ----------
    def rich(self, s):
        return rich(s).replace("ACCENT", self.T.get("accent", self.T["kicker"]))

    def chrome(self, dark=False):
        T, out = self.T, []
        if self.rail:
            out.append(f'<div style="position:absolute;left:0px;top:0px;width:72px;height:1080px;background:{T["black"]}"></div>')
            out.append(f'<svg aria-label="{esc(self.name)}" style="position:absolute;left:0px;top:340px;width:72px;height:400px" width="72" height="400" viewBox="0 0 72 400"><text x="0" y="0" transform="translate(42 200) rotate(-90)" text-anchor="middle" font-family="Arial, sans-serif" font-size="17" font-weight="700" fill="#FFFFFF" letter-spacing="1">{esc(self.name)}</text></svg>')
        logo = self.logo.get("light" if (dark or self.rail) else "dark")
        if logo:
            out.append(f'<img src="{logo}" alt="Phenom" style="position:absolute;left:{20 if self.rail else 48}px;top:996px;width:33px;height:42px;object-fit:contain">')
        return "\n".join(out)

    def section(self, sid, inner, bg=None, dark=False, row=False, extra_pad=None, gap=40):
        T = self.T
        bg = bg or (T["black"] if dark else T["paper"])
        color = "#FFFFFF" if dark else T["ink"]
        pad = extra_pad or f"72px 96px 72px {self.left}px"
        # full-bleed backdrops (img/div pinned at 0,0 1920x1080) must paint before the chrome, or they hide the logo
        back = re.match(r'^((?:<(?:img|div)[^>]*position:absolute;left:0px;top:\d+px;width:1920px;height:\d+px[^>]*>(?:</div>)?)+)', inner)
        pre = back.group(1) if back else ""; rest = inner[len(pre):]
        return (f'<section id="{sid}" data-transition="fade" style="background:{bg};color:{color};font-family:{T["sans"]};'
                f'padding:{pad};display:flex;flex-direction:{"row" if row else "column"};gap:{gap}px">\n{pre}{self.chrome(dark)}\n{rest}\n</section>\n')

    def head(self, s, size=60, dark=False):
        T = self.T
        if self.spec.get("style") == "summit-mono":
            k = f'<p style="font-size:24px;color:{"#FFFFFF" if dark else T["ink"]};border:2px solid {"#FFFFFF" if dark else T["ink"]};border-radius:999px;padding:4px 18px;align-self:flex-start">{esc(s["kicker"])}</p>' if s.get("kicker") else ""
        else:
            k = f'<p style="font-size:24px;font-weight:700;color:{"#DDDDEA" if dark else T["kicker"]};text-transform:uppercase;letter-spacing:1px">{esc(s["kicker"])}</p>' if s.get("kicker") else ""
        t = f'<h2 style="font-family:{T["serif"]};font-size:{size}px;font-weight:600;line-height:1.1">{self.rich(s["title"])}</h2>' if s.get("title") else ""
        sub = f'<p style="font-size:30px;color:{"#DDDDEA" if dark else T["body"]}">{self.rich(s["sub"])}</p>' if s.get("sub") else ""
        return f'<div style="display:flex;flex-direction:column;gap:8px">{k}{t}{sub}</div>'

    def foot(self, s):
        T, out = self.T, []
        c = s.get("callout")
        if c:
            tone = s.get("callout_tone", "navy")
            if tone == "navy": bg, fg = T["navy"], "#FFFFFF"
            else: bg, fg = T["tints"][{"honey": 0, "rose": 1, "lilac": 2}.get(tone, 0)], T["ink"]
            label = f'<b>{esc(c["label"])}</b>  ' if isinstance(c, dict) and c.get("label") else ""
            text = c["text"] if isinstance(c, dict) else c
            out.append(f'<p style="background:{bg};color:{fg};border-radius:20px;padding:20px 32px;font-size:26px">{label}{rich(text)}</p>')
        if s.get("source"):
            out.append(f'<p style="font-size:24px;color:{T["muted"]}">{rich(s["source"])}</p>')
        return "\n".join(out)

    def notes(self, s): return f'<aside>{esc(s["notes"])}</aside>' if s.get("notes") else ""

    def tint(self, i): return self.T["tints"][i % len(self.T["tints"])]

    # ---------- layouts ----------
    def cover(self, s):
        T = self.T
        if s.get("image") and s.get("image_side") == "right":   # text-free crop pinned bottom-right (e.g. imagery/rocket.jpg)
            w = s.get("image_width", 900); h = s.get("image_height", 640)
            img = f'<img src="{s["image"]}" alt="" style="position:absolute;left:{1920 - w}px;top:{1080 - h}px;width:{w}px;height:{h}px;object-fit:cover">'; scrim = ""
        else:
            img = f'<img src="{s["image"]}" alt="" style="position:absolute;left:0px;top:0px;width:1920px;height:1080px;object-fit:cover">' if s.get("image") else ""
            scrim = f'<div style="position:absolute;left:0px;top:0px;width:1920px;height:1080px;background:linear-gradient(90deg, {T["navy"]} 0%, rgba(34,34,75,0.55) 100%)"></div>' if s.get("image") and s.get("scrim", True) else ""
        if s.get("centered"):
            # vertically centred (two flex spacers; a fixed-height empty div is dropped by the editor), clear of a wordmark at the top
            inner = (f'{img}{scrim}<div style="flex:1"></div>'
                     f'<h1 style="font-family:{T["serif"]};font-size:{s.get("size",96)}px;font-weight:600;line-height:1.08;color:#FFFFFF;text-align:center">{self.rich(s["title"])}</h1>'
                     f'<p style="font-size:30px;color:#DDDDEA;text-align:center">{self.rich(s.get("sub",""))}</p><div style="flex:1"></div>' + self.notes(s))
            return self.section(s["id"], inner, bg=T["navy"], dark=True, gap=20, extra_pad="72px 260px 72px 260px")
        inner = (f'{img}{scrim}<div style="flex:1"></div>'
                 f'<p style="font-size:26px;color:#DDDDEA;text-transform:uppercase;letter-spacing:1px">{esc(s.get("kicker",""))}</p>'
                 f'<h1 style="font-family:{T["serif"]};font-size:{s.get("size",112)}px;font-weight:600;line-height:1.05;color:#FFFFFF;max-width:1300px">{rich(s["title"])}</h1>'
                 f'<p style="font-size:32px;color:#DDDDEA;max-width:1200px">{rich(s.get("sub",""))}</p><div style="height:48px"></div>')
        return self.section(s["id"], inner, bg=T["navy"], dark=True, gap=16)

    def divider(self, s):
        T = self.T
        img = ""
        if s.get("band"):   # e.g. clouds-band.jpg along the bottom
            img = f'<img src="{s["band"]}" alt="" style="position:absolute;left:0px;top:{s.get("band_top",560)}px;width:1920px;height:{1080 - s.get("band_top",560)}px;object-fit:cover">'
        elif s.get("image") and s.get("image_side", "full") == "right":   # text-free right panel
            img = f'<img src="{s["image"]}" alt="" style="position:absolute;left:{s.get("image_left",1000)}px;top:0px;width:{1920 - s.get("image_left",1000)}px;height:1080px;object-fit:cover">'
        elif s.get("image"):   # clean full-bleed image (imagery/*-full.jpg): opacity 1; a cropped one: 0.55
            img = f'<img src="{s["image"]}" alt="" style="position:absolute;left:0px;top:0px;width:1920px;height:1080px;object-fit:cover;opacity:{s.get("opacity",1)}">'
        num = f'<p style="font-family:{T["serif"]};font-size:160px;font-weight:600;line-height:1;color:#FFFFFF">{esc(s["number"])}</p>' if s.get("number") else ""
        mode = s.get("text", "bottom")   # bottom (default) · top (text in the top-left sky) · band (centred in a dark band across the image)
        if s.get("overlay"):   # draw the translucent band for images that lack a baked-in one
            img += f'<div style="position:absolute;left:0px;top:{s.get("band_top",195)}px;width:1920px;height:{s.get("band_height",690)}px;background:rgba(20,20,22,0.55)"></div>'
        inner = (f'{img}' + ('' if mode == "top" else '<div style="flex:1"></div>') + f'{num}{self.head(s, 84, dark=True)}' + ('<div style="flex:1"></div>' if mode in ("top", "band") else '')
                 + (f'<div data-text style="position:absolute;left:1000px;top:640px;width:800px;font-family:{T["serif"]};font-size:36px;font-weight:600;line-height:1.6;color:#FFFFFF">' + "".join(f"<p>{rich(q)}</p>" for q in s["questions"]) + "</div>" if s.get("questions") else "")
                 + '<div style="height:72px"></div>')
        return self.section(s["id"], inner, dark=True, gap=24)

    def statement(self, s):
        T = self.T
        parts = s["parts"]  # [{"big":"20","label":"HUMAN","caption":"How work is done","accent":false}]
        cols = []
        for i, p in enumerate(parts):
            col = T["strong"][0] if p.get("accent") else "#FFFFFF"
            cols.append(f'<div style="flex:{p.get("flex",1)};display:flex;flex-direction:column;align-items:center;gap:12px">'
                        f'<p style="font-family:{T["serif"]};font-size:{s.get("size",300)}px;font-weight:600;line-height:1;color:{col}">{esc(p["big"])}</p>'
                        f'<p style="font-size:24px;letter-spacing:2px;color:#BBBBC8">{esc(p.get("label",""))}</p>'
                        + (f'<p style="font-family:{T["serif"]};font-size:36px;font-style:italic;color:{col}">{esc(p["caption"])}</p>' if p.get("caption") else "") + "</div>")
            if i < len(parts) - 1: cols.append('<div style="width:3px;background:#55556A;align-self:stretch"></div>')
        bar = "".join(f'<div style="flex:{p.get("flex",1)};height:10px;background:{T["strong"][0] if p.get("accent") else "#FFFFFF"};border-radius:999px"></div>' for p in parts)
        inner = (f'<p style="font-size:24px;letter-spacing:2px;color:#BBBBC8;text-align:center">{esc(s.get("kicker",""))}</p><div style="flex:1"></div>'
                 f'<div style="display:flex;flex-direction:row;gap:48px;align-items:center;justify-content:center">{"".join(cols)}</div>'
                 f'<div style="display:flex;flex-direction:row;gap:24px;padding:0px 240px">{bar}</div>'
                 + (f'<p style="font-family:{T["serif"]};font-size:48px;font-style:italic;text-align:center;color:#FFFFFF">{rich(s["tagline"])}</p>' if s.get("tagline") else "") + '<div style="flex:1"></div>')
        return self.section(s["id"], inner, dark=True, gap=40)

    def cards(self, s):
        T = self.T
        items = s["items"]; n = len(items); rows = 2 if n > 4 else 1; per = (n + rows - 1) // rows
        cards = []
        for i, it in enumerate(items):
            navy = it.get("navy"); bg = T["navy"] if navy else (self.tint(i) if s.get("tinted", True) and i < 3 else T["card"])
            fg, fb = ("#FFFFFF", "#DDDDEA") if navy else (T["ink"], T["body"])
            num = f'<p style="font-family:{T["serif"]};font-size:48px;font-weight:600;line-height:1;color:{"#DDDDEA" if navy else T["mauve"]}">{esc(it["num"])}</p>' if it.get("num") else ""
            tag = f'<p style="font-size:24px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:{"#DDDDEA" if navy else T["kicker"]}">{esc(it["tag"])}</p>' if it.get("tag") else ""
            foot = f'<div style="flex:1"></div><p style="font-size:24px;font-weight:700;color:{"#DDDDEA" if navy else T["kicker"]}">{rich(it["foot"])}</p>' if it.get("foot") else ""
            cards.append(f'<div style="flex:1;background:{bg};border-radius:40px;padding:36px 40px;display:flex;flex-direction:column;gap:12px;color:{fg}">{num}{tag}'
                         f'<h3 style="font-size:30px;font-weight:700;line-height:1.2;color:{fg}">{rich(it["title"])}</h3>'
                         f'<p style="font-size:26px;line-height:1.35;color:{fb}">{rich(it.get("body",""))}</p>{foot}</div>')
        grid = f'<div style="flex:1;display:grid;grid-template-columns:{" ".join(["1fr"]*per)};grid-template-rows:{" ".join(["1fr"]*rows)};gap:24px">{"".join(cards)}</div>' if rows > 1 else f'<div style="flex:1;display:flex;flex-direction:row;gap:24px;align-items:stretch">{"".join(cards)}</div>'
        return self.section(s["id"], self.head(s) + grid + self.foot(s) + self.notes(s))

    def tiles(self, s):
        T = self.T; tiles = []
        for i, it in enumerate(s["items"]):
            navy = it.get("navy", i != 1); bg = T["navy"] if navy else T["tints"][2]
            fg, fb = ("#FFFFFF", "#DDDDEA") if navy else (T["ink"], T["body"])
            tiles.append(f'<div style="flex:1;background:{bg};border-radius:24px;padding:48px;display:flex;flex-direction:column;align-items:center;gap:8px">'
                         f'<p style="font-family:{T["serif"]};font-size:120px;font-weight:600;line-height:1;color:{T["strong"][0] if navy else T["navy"]}">{esc(it["big"])}</p>'
                         f'<p style="font-size:24px;letter-spacing:2px;color:{fb}">{esc(it.get("label",""))}</p>'
                         f'<p style="font-size:34px;font-weight:700;text-align:center;color:{fg}">{rich(it.get("title",""))}</p></div>')
        inner = self.head(s) + f'<div style="flex:1;display:flex;flex-direction:row;gap:24px;align-items:stretch">{"".join(tiles)}</div>' + self.foot(s) + self.notes(s)
        return self.section(s["id"], inner)

    def steps(self, s):
        T = self.T; n = len(s["items"]); cols = []
        for i, it in enumerate(s["items"]):
            cols.append(f'<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:12px">'
                        f'<div style="width:96px;height:96px;border-radius:50%;background:{T["tints"][(i) % 4] if (i % 4) != 3 else T["tints"][4] if len(T["tints"]) > 4 else T["tints"][3]};border:3px solid {T["strong"][i % 4]};display:flex;align-items:center;justify-content:center"><p style="font-family:{T["serif"]};font-size:36px;font-weight:600;color:{T["ink"]}">{esc(it.get("num", f"{i+1:02d}"))}</p></div>'
                        f'<p style="font-size:30px;font-weight:700;text-align:center">{rich(it["title"])}</p>'
                        f'<p style="font-size:24px;line-height:1.35;text-align:center;color:{T["body"]}">{rich(it.get("body",""))}</p></div>')
        line = f'<div style="position:relative;height:0px"><hr style="position:absolute;left:{self.left + 160}px;top:48px;width:{1920 - self.left - 96 - 320}px;border-top:2px solid {T["rule"]}"></div>'
        inner = self.head(s) + '<div style="flex:1"></div>' + f'<div style="display:flex;flex-direction:row;gap:24px;align-items:flex-start">{"".join(cols)}</div><div style="flex:1"></div>' + self.foot(s) + self.notes(s)
        return self.section(s["id"], inner)

    def triptych(self, s):
        T = self.T
        c = s["company"]  # {"name","tag","stat","stat_label"}
        left = (f'<div style="width:300px;background:{T["card"]};border-radius:32px;padding:32px;display:flex;flex-direction:column;gap:14px">'
                f'<p style="font-family:{T["serif"]};font-size:40px;font-weight:600">{esc(c["name"])}</p>'
                f'<p style="background:{T["tints"][2]};color:{T["ink"]};font-size:24px;font-weight:700;letter-spacing:1px;padding:4px 14px;border-radius:999px;align-self:flex-start">{esc(c.get("tag",""))}</p>'
                f'<p style="font-family:{T["serif"]};font-size:64px;font-weight:600;line-height:1">{esc(c.get("stat",""))}</p>'
                f'<p style="font-size:24px;line-height:1.35;color:{T["body"]}">{rich(c.get("stat_label",""))}</p></div>')
        cols = []
        for i, col in enumerate(s["columns"]):  # 3 columns: {"pct","who","title","bullets":[]}
            navy = i == 1; bg = T["navy"] if navy else (T["tints"][2] if i == 0 else T["tints"][0])
            fg, fb = ("#FFFFFF", "#DDDDEA") if navy else (T["ink"], T["body"])
            bul = "".join(f'<li style="font-size:24px;line-height:1.35;color:{fb}">{rich(b)}</li>' for b in col.get("bullets", []))
            cols.append(f'<div style="flex:{1.4 if navy else 1};background:{bg};border-radius:32px;padding:32px;display:flex;flex-direction:column;gap:10px;color:{fg}">'
                        f'<p style="font-family:{T["serif"]};font-size:48px;font-weight:600;line-height:1;color:{T["strong"][0] if navy else T["ink"]}">{esc(col["pct"])}</p>'
                        f'<p style="font-size:24px;letter-spacing:1px;text-transform:uppercase;color:{fb}">{esc(col.get("who",""))}</p>'
                        f'<p style="font-size:30px;font-weight:700;color:{fg}">{rich(col["title"])}</p><ul style="font-size:24px;padding:0px 0px 0px 28px">{bul}</ul></div>')
        inner = self.head(s) + f'<div style="flex:1;display:flex;flex-direction:row;gap:24px;align-items:stretch">{left}{"".join(cols)}</div>' + self.foot(s) + self.notes(s)
        return self.section(s["id"], inner)

    def table(self, s):
        T = self.T; cols = s["columns"]; widths = s.get("widths") or [round(100 / len(cols))] * len(cols)
        th = "".join(f'<th style="width:{w}%;color:#FFFFFF;padding:16px 20px">{esc(c)}</th>' for c, w in zip(cols, widths))
        rows = []
        for i, r in enumerate(s["rows"]):
            bg = f' style="background:{T["tints"][2]}"' if i % 2 else ""
            tds = []
            for j, cell in enumerate(r):
                col = ""
                if isinstance(cell, dict): col = f' style="color:{STATUS.get(cell.get("status"), T["ink"])}"'; cell = cell["text"]
                tds.append(f"<td{col}>{('<b>' + rich(cell) + '</b>') if j == 0 else rich(cell)}</td>")
            rows.append(f"<tr{bg}>{''.join(tds)}</tr>")
        tbl = f'<table style="font-size:{s.get("font",24)}px;color:{T["ink"]};background:{T["card"]};border-radius:24px"><tr style="background:{T["navy"]}">{th}</tr>{"".join(rows)}</table>'
        return self.section(s["id"], self.head(s) + tbl + '<div style="flex:1"></div>' + self.foot(s) + self.notes(s))

    def compare(self, s):
        T = self.T; cols = []
        for i, c in enumerate(s["columns"]):  # {"tag","title","rows":[["Process","..."],...]} or {"tag","title","body"}
            navy = c.get("navy", i == 1); bg = T["navy"] if navy else T["tints"][0]
            fg, fb = ("#FFFFFF", "#DDDDEA") if navy else (T["ink"], T["body"])
            body = ""
            if c.get("rows"):
                body = "".join(f'<div style="display:flex;flex-direction:row;gap:20px"><p style="width:200px;font-size:24px;font-weight:700;color:{T["strong"][0] if navy else T["kicker"]}">{esc(k)}</p><p style="flex:1;font-size:24px;line-height:1.35;color:{fb}">{rich(v)}</p></div>' for k, v in c["rows"])
            elif c.get("stats"):
                body = "".join(f'<div style="display:flex;flex-direction:row;gap:20px;align-items:baseline"><p style="width:200px;font-family:{T["serif"]};font-size:56px;font-weight:600;color:{fg}">{esc(k)}</p><p style="flex:1;font-size:24px;line-height:1.35;color:{fb}">{rich(v)}</p></div>' for k, v in c["stats"])
            else:
                body = f'<p style="font-size:26px;line-height:1.4;color:{fb}">{rich(c.get("body",""))}</p>'
            cols.append(f'<div style="flex:1;background:{bg};border-radius:32px;padding:40px;display:flex;flex-direction:column;gap:20px;color:{fg}">'
                        f'<p style="font-size:24px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:{T["strong"][0] if navy else T["kicker"]}">{esc(c.get("tag",""))}</p>'
                        f'<p style="font-family:{T["serif"]};font-size:40px;font-weight:600;color:{fg}">{rich(c["title"])}</p>{body}</div>')
        inner = self.head(s) + f'<div style="flex:1;display:flex;flex-direction:row;gap:24px;align-items:stretch">{"".join(cols)}</div>' + self.foot(s) + self.notes(s)
        return self.section(s["id"], inner)

    def rows(self, s):
        T = self.T; out = []; n = len(s["items"])
        for i, it in enumerate(s["items"]):  # {"label","body","navy":bool}
            navy = it.get("navy", i == n - 1 and s.get("last_navy", True)); bg = T["navy"] if navy else self.tint(i)
            fg, fb = ("#FFFFFF", "#DDDDEA") if navy else (T["ink"], T["body"])
            out.append(f'<div style="display:flex;flex-direction:row;gap:32px;align-items:center;background:{bg};border-radius:20px;padding:22px 32px">'
                       f'<p style="width:420px;font-size:28px;font-weight:700;color:{fg}">{rich(it["label"])}</p>'
                       f'<p style="flex:1;font-size:24px;line-height:1.35;color:{fb}">{rich(it["body"])}</p></div>')
        inner = self.head(s) + f'<div style="display:flex;flex-direction:column;gap:14px">{"".join(out)}</div><div style="flex:1"></div>' + self.foot(s) + self.notes(s)
        return self.section(s["id"], inner)

    def stats(self, s):
        T = self.T
        tiles = "".join(f'<div style="flex:1;background:{T["card"]};border-radius:24px;padding:28px 32px;display:flex;flex-direction:column;gap:6px">'
                        f'<p style="font-size:24px;font-weight:700;color:{T["kicker"]}">{esc(t.get("label",""))}</p>'
                        f'<p style="font-family:{T["serif"]};font-size:64px;font-weight:600;line-height:1">{esc(t["big"])}</p>'
                        f'<p style="font-size:24px;color:{T["body"]}">{rich(t.get("sub",""))}</p></div>' for t in s["tiles"])
        cards = "".join(f'<div style="flex:1;background:{self.tint(i)};border-radius:24px;padding:28px 32px;display:flex;flex-direction:column;gap:8px">'
                        f'<p style="font-size:28px;font-weight:700">{rich(c["title"])}</p><p style="font-size:24px;line-height:1.35;color:{T["body"]}">{rich(c["body"])}</p></div>' for i, c in enumerate(s.get("cards", [])))
        inner = self.head(s) + f'<div style="display:flex;flex-direction:row;gap:20px">{tiles}</div>' + (f'<div style="display:flex;flex-direction:row;gap:20px">{cards}</div>' if cards else "") + '<div style="flex:1"></div>' + self.foot(s) + self.notes(s)
        return self.section(s["id"], inner)

    def split(self, s):
        T = self.T
        blocks = "".join(f'<div style="display:flex;flex-direction:column;gap:8px"><p style="font-size:24px;font-weight:700;color:{T["kicker"]};text-transform:uppercase;letter-spacing:1px">{esc(b["label"])}</p><p style="font-size:26px;line-height:1.4;color:{T["body"]}">{rich(b["text"])}</p></div>' for b in s.get("blocks", []))
        left = f'<div style="width:{s.get("left_width",560)}px;display:flex;flex-direction:column;gap:36px">{self.head(s, 52)}{blocks}</div>'
        right = f'<div style="flex:1;background:{T["card"]};border-radius:32px;padding:40px;display:flex;flex-direction:column;gap:24px">{s.get("panel","")}<div style="flex:1"></div>' + (f'<p style="font-size:24px;color:{T["muted"]}">{rich(s["source"])}</p>' if s.get("source") else "") + "</div>"
        return self.section(s["id"], left + right + self.notes(s), row=True, gap=48)

    def takeaway(self, s):
        T = self.T; cards = []
        for i, c in enumerate(s["items"]):
            last = i == len(s["items"]) - 1; bg = T["strong"][0] if last else "#FFFFFF"
            cards.append(f'<div style="flex:1;background:{bg};border-radius:24px;padding:36px;display:flex;flex-direction:column;gap:10px">'
                         f'<p style="font-size:30px;font-weight:700;color:{T["ink"]}">{rich(c["title"])}</p><p style="font-size:24px;line-height:1.35;color:{T["body"]}">{rich(c.get("body",""))}</p></div>')
        inner = self.head(s, dark=True) + '<div style="flex:1"></div>' + f'<div style="display:flex;flex-direction:row;gap:24px">{"".join(cards)}</div>' + (f'<p style="font-size:30px;text-align:center;color:#DDDDEA">{rich(s["closing"])}</p>' if s.get("closing") else "") + '<div style="flex:1"></div>' + self.notes(s)
        return self.section(s["id"], inner, dark=True)

    def bignum(self, s):
        """One giant number, one line, one source (summit-mono s54-s66)."""
        T = self.T; dark = s.get("dark", False); acc = T.get("accent", T["mauve"])
        fg = "#FFFFFF" if dark else T["ink"]; fb = "#DDDDDD" if dark else T["body"]
        inner = (f'<p style="font-size:24px;font-weight:700;letter-spacing:2px;text-transform:uppercase;text-align:center;color:{acc}">{esc(s.get("kicker",""))}</p><div style="flex:1"></div>'
                 f'<p style="font-family:{s.get("font", T["serif"])};font-size:{s.get("size",260)}px;font-weight:{s.get("weight",600)};line-height:1;text-align:center;color:{acc if s.get("accent", True) else fg}">{esc(s["big"])}</p>'
                 f'<p style="font-size:40px;text-align:center;color:{fg}">{self.rich(s.get("line",""))}</p>'
                 + (f'<p style="font-size:26px;text-align:center;color:{fb}">{self.rich(s["sub"])}</p>' if s.get("sub") else "") + '<div style="flex:1"></div>'
                 + (f'<p style="font-size:24px;text-align:center;color:{T["muted"]}">{self.rich(s["source"])}</p>' if s.get("source") else "") + self.notes(s))
        return self.section(s["id"], inner, dark=dark, gap=24)

    def numbers(self, s):
        """Two to four giant numbers in a row; the last one in the accent (s03, s44)."""
        T = self.T; acc = T.get("accent", T["mauve"]); n = len(s["items"]); cols = []
        for i, it in enumerate(s["items"]):
            col = acc if it.get("accent", i == n - 1) else (T["muted"] if it.get("grey") else T["ink"])
            cols.append(f'<div style="flex:1;display:flex;flex-direction:column;gap:12px"><p style="font-family:{T["serif"]};font-size:{s.get("size",140)}px;font-weight:600;line-height:1;color:{col}">{esc(it["big"])}</p><p style="font-size:26px;line-height:1.35;color:{T["body"]}">{self.rich(it.get("body",""))}</p></div>')
        inner = self.head(s) + '<div style="flex:1"></div>' + f'<div style="display:flex;flex-direction:row;gap:40px">{"".join(cols)}</div><div style="flex:1"></div>' + (f'<p style="font-size:30px;font-weight:600">{self.rich(s["closing"])}</p>' if s.get("closing") else "") + self.foot(s) + self.notes(s)
        return self.section(s["id"], inner)

    def chain(self, s):
        """Columns with a thin coloured top rule, numbered (s07, s12, s50)."""
        T = self.T; acc = T.get("accent", T["kicker"]); cols = []
        for i, it in enumerate(s["items"]):
            rule = T["strong"][i % len(T["strong"])] if s.get("rotate") else acc
            cols.append(f'<div style="flex:1;display:flex;flex-direction:column;gap:10px;border-top:4px solid {rule};padding:20px 0px 0px 0px">'
                        f'<p style="font-size:24px;font-weight:600;color:{acc}">{esc(it.get("num", f"{i+1:02d}"))}</p>'
                        f'<p style="font-family:{T["serif"]};font-size:34px;font-weight:600;line-height:1.15">{self.rich(it["title"])}</p>'
                        f'<p style="font-size:24px;line-height:1.35;color:{T["body"]}">{self.rich(it.get("body",""))}</p></div>')
        inner = self.head(s) + f'<div style="display:flex;flex-direction:row;gap:32px;align-items:flex-start">{"".join(cols)}</div><div style="flex:1"></div>' + (f'<p style="font-size:30px;font-weight:600">{self.rich(s["closing"])}</p>' if s.get("closing") else "") + self.foot(s) + self.notes(s)
        return self.section(s["id"], inner)

    def bars(self, s):
        """Horizontal bars, label left and value right; low values in the accent (s16)."""
        T = self.T; acc = T.get("accent", T["mauve"]); rows = []
        for it in s["items"]:  # {"label","value":0-100,"low":bool}
            col = acc if it.get("low") else T["ink"]
            rows.append(f'<div style="display:flex;flex-direction:row;gap:24px;align-items:center"><p style="width:380px;font-size:26px;font-weight:600;text-align:right">{esc(it["label"])}</p>'
                        f'<div style="flex:1;height:24px;background:#EEEEEE;border-radius:999px;display:flex;flex-direction:row"><div style="width:{it["value"]}%;height:24px;background:{col};border-radius:999px"></div></div>'
                        f'<p style="width:100px;font-size:26px;color:{T["body"]}">{esc(str(it["value"]))}%</p></div>')
        inner = self.head(s) + f'<div style="display:flex;flex-direction:column;gap:18px">{"".join(rows)}</div><div style="flex:1"></div>' + self.foot(s) + self.notes(s)
        return self.section(s["id"], inner)

    def accent(self, s):
        """Full accent-colour statement slide (s68)."""
        T = self.T; acc = T.get("accent", T["navy"])
        inner = ('<div style="flex:1"></div>' + f'<h1 style="font-family:{T["sans"]};font-size:{s.get("size",88)}px;font-weight:600;line-height:1.15;text-align:center;color:#FFFFFF">{self.rich(s["title"])}</h1>'
                 + (f'<p style="font-size:28px;text-align:center;color:#FFF3EC">{self.rich(s["sub"])}</p>' if s.get("sub") else "") + '<div style="flex:1"></div>' + self.notes(s))
        return self.section(s["id"], inner, bg=acc, dark=True, gap=24)

    def custom(self, s):
        return self.section(s["id"], self.head(s) + s["html"] + self.foot(s) + self.notes(s), dark=s.get("dark", False))

    def render(self, s):
        return getattr(self, s["layout"])(s)

def main():
    spec = json.load(open(sys.argv[1])); out = sys.argv[2]
    d = Deck(spec)
    os.makedirs(os.path.join(out, "project", "slides"), exist_ok=True)
    ids = []
    for s in spec["slides"]:
        ids.append(s["id"])
        with open(os.path.join(out, "project", "slides", f'{s["id"]}.html'), "w") as f: f.write(d.render(s))
    index = {"v": 4, "createdOnFiles": {"v": 1, "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}, "lists": "css",
             "title": spec["title"], "order": ids, "cover": ids[0],
             "sections": spec.get("sections") or {"s1": {"description": spec.get("description", spec["title"]), "start": ids[0]}},
             "faces": d.T["faces"], "designSystems": []}
    with open(os.path.join(out, "project", "deck.json"), "w") as f: json.dump(index, f, separators=(",", ":"))
    print(f"{len(ids)} slides -> {out}/project (deck.json + slides/)")

if __name__ == "__main__":
    main()
