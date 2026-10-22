#!/usr/bin/env python3
"""Write font-metrics.json: per-character advance widths (units of font size).

Lets build_pptx_leadership.py wrap text exactly without the fonts installed, so
the layout is deterministic and reproducible. Re-run only if the type scale or
the corpus gains characters; run render_qa_leadership.py first to fetch the TTFs.
"""
import json, sys
from pathlib import Path
from PIL import ImageFont

HERE = Path(__file__).parent
FONTDIR = HERE / "qa-fonts"
FACES = {
    "sans400": ("DMSans.ttf", "Regular"),
    "sans500": ("DMSans.ttf", "Medium"),
    "sans700": ("DMSans.ttf", "Bold"),
    "serif600": ("Fraunces.ttf", "SemiBold"),
    "serif600i": ("Fraunces-Italic.ttf", "SemiBold Italic"),
}
SZ = 1000
# every codepoint this deck can render, plus ASCII
CHARS = sorted(set(chr(c) for c in range(32, 127)) |
               set("·—–’‘“”…↔→°§¶†•×÷≈≤≥"))
out = {}
for face, (fname, inst) in FACES.items():
    f = ImageFont.truetype(str(FONTDIR / fname), SZ)
    try:
        f.set_variation_by_name(inst)
    except Exception as e:
        print(f"warn: {face}: {e}", file=sys.stderr)
    w = {c: round(f.getlength(c) / SZ, 5) for c in CHARS}
    out[face] = {"avg": round(sum(w.values()) / len(w), 5), "w": w}
(HERE / "font-metrics.json").write_text(json.dumps(out, ensure_ascii=False,
                                                   separators=(",", ":")))
print("wrote font-metrics.json", {k: v["avg"] for k, v in out.items()})
