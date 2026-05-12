#!/usr/bin/env python3
"""Polish Crafties product preview photos without changing mascot/logo art.

Applies gentle, craft-friendly enhancements to assets/product-photos/*.jpg:
- mild autocontrast
- warm saturation/contrast/sharpness lift
- selective brightness fixes for images that visually tested too dark/bright
- optimized progressive JPEG output
"""
from __future__ import annotations

import shutil
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
PHOTO_DIR = ROOT / "assets" / "product-photos"
BACKUP_DIR = ROOT / "assets" / "backup-before-photo-polish"

DARK_LIFT = {
    "charm-safety-pin-brooch.jpg": 1.10,
    "felt-heart-ornament.jpg": 1.08,
    "tiny-driftwood-boat.jpg": 1.12,
    "painted-jar-lantern.jpg": 1.06,
}
BRIGHT_TAME = {
    "thank-you-flower-card.jpg": 0.97,
    "tiny-doodle-garden.jpg": 0.98,
    "watercolor-bloom-card.jpg": 0.98,
    "beginner-granny-square.jpg": 0.99,
}
EXTRA_SHARPEN = {
    "crafties-welcome-card.jpg": 1.08,
    "embroidered-name-patch.jpg": 1.08,
    "painted-dot-greeting-card.jpg": 1.05,
}


def backup_originals() -> None:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    for src in PHOTO_DIR.glob("*.jpg"):
        dst = BACKUP_DIR / src.name
        if not dst.exists():
            shutil.copy2(src, dst)


def polish(path: Path) -> tuple[int, int]:
    before = path.stat().st_size
    with Image.open(path) as im:
        im = im.convert("RGB")
        # Normalize the generated-photo set gently; keep the warm handmade look.
        im = ImageOps.autocontrast(im, cutoff=0.8, preserve_tone=True)
        im = ImageEnhance.Color(im).enhance(1.07)
        im = ImageEnhance.Contrast(im).enhance(1.035)
        im = ImageEnhance.Brightness(im).enhance(DARK_LIFT.get(path.name, BRIGHT_TAME.get(path.name, 1.01)))
        im = im.filter(ImageFilter.UnsharpMask(radius=1.25, percent=82, threshold=4))
        if path.name in EXTRA_SHARPEN:
            im = ImageEnhance.Sharpness(im).enhance(EXTRA_SHARPEN[path.name])
        # Keep exact dimensions but reduce excessive JPEG baggage.
        im.save(path, "JPEG", quality=88, optimize=True, progressive=True, subsampling=1)
    return before, path.stat().st_size


def main() -> None:
    backup_originals()
    total_before = total_after = count = 0
    for path in sorted(PHOTO_DIR.glob("*.jpg")):
        before, after = polish(path)
        total_before += before
        total_after += after
        count += 1
        print(f"polished {path.name}: {before:,} -> {after:,} bytes")
    print(f"\nDone: {count} photos polished")
    print(f"Total: {total_before:,} -> {total_after:,} bytes")


if __name__ == "__main__":
    main()
