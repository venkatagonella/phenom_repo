#!/usr/bin/env python3
"""Tile slide PNGs (sNN.png from render-pdf.swift) into 3x4 contact sheets.
Usage: python3 contact_sheet.py <png-dir> <out-prefix>   -> <out-prefix>0.png, 1.png, ...
"""
import glob, sys
from PIL import Image

src, prefix = sys.argv[1], sys.argv[2]
files = sorted(glob.glob(f"{src}/s*.png"))
W, H = 480, 270
for k in range(0, len(files), 12):
    chunk = files[k:k + 12]
    sheet = Image.new("RGB", (W * 3, H * 4), "white")
    for j, f in enumerate(chunk):
        sheet.paste(Image.open(f).convert("RGB").resize((W, H)), ((j % 3) * W, (j // 3) * H))
    sheet.save(f"{prefix}{k // 12}.png")
print(f"{len(files)} slides -> {(len(files) + 11) // 12} sheets")
