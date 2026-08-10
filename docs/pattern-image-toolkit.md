# Team Crafties Pattern Image Toolkit

Local tools for Nath's pattern-making workflow. The toolkit keeps AI image generation, Recraft-style design assets, social graphics, and exact SVG diagrams separated so we do not use the wrong model for the wrong job.

## Quick commands

From the project root:

```bash
python3 scripts/pattern-image-toolkit.py check
python3 scripts/pattern-image-toolkit.py list
```

Render a prompt without spending credits:

```bash
python3 scripts/pattern-image-toolkit.py prompt \
  --preset pattern-cover-recraft \
  --title "Free Crochet Hippo Pattern" \
  --craft crochet \
  --details "soft purple hippo, teal flower, beginner-friendly printable cover"
```

Generate a Recraft-style pattern cover using the FAL key in `~/.hermes/.env`:

```bash
python3 scripts/pattern-image-toolkit.py generate \
  --preset pattern-cover-recraft \
  --title "Free Crochet Hippo Pattern" \
  --craft crochet \
  --details "soft purple hippo, teal flower, beginner-friendly printable cover"
```

From Nath's Telegram bot, use the shortcut command instead of Terminal:

```text
/patterncover Free Crochet Hippo Pattern | crochet | soft purple hippo, teal flower, beginner-friendly printable cover
```

The command runs on the Mac through Hermes Gateway and sends the generated image back to Telegram. Files still save under `.crafties-toolkit/images/` for review.

Make an exact local SVG diagram with no AI call:

```bash
python3 scripts/pattern-image-toolkit.py diagram \
  --title "Purple Hippo Assembly" \
  --component "Body: Rounds 1-24, oval stuffed body" \
  --component "Head: Attach centered above body" \
  --component "Flower: Sew teal flower beside one ear"
```

Generated drafts land under `.crafties-toolkit/` and are ignored by Git/Netlify until a human deliberately copies an approved asset into `assets/product-photos/` or another public folder.

## Presets

| Preset | Backend | Use it for |
|---|---|---|
| `realistic-finished-project` | FAL Nano Banana Pro | General finished-project photos, plush/candle/jewelry/soap/yarn hero images |
| `crochet-texture-photo` | FAL FLUX 2 Pro | Yarn texture, crochet/knit/macramé closeups, realistic finished craft materials |
| `pattern-cover-recraft` | FAL Recraft V4 Pro | Clean pattern covers, branded graphics, printable title cards, icons |
| `text-label-graphic` | FAL Ideogram V3 | Short readable labels and text-forward graphics |
| `social-square` | FAL Recraft V4 Pro | Facebook/Instagram square promo graphics |
| `local-pattern-cover-svg` | local SVG | No-credit deterministic printable covers/placeholders |
| `assembly-diagram-svg` | local SVG | Exact stitch/assembly helper diagrams where AI must not invent details |

## Workflow rule

Use the right lane:

1. **Need realism?** Use `realistic-finished-project` or `crochet-texture-photo`.
2. **Need polished brand/design?** Use `pattern-cover-recraft`.
3. **Need readable text?** Use `text-label-graphic`.
4. **Need exact stitch counts, piece order, or printable instructions?** Use `assembly-diagram-svg`.
5. **Paid image backend blocked?** Use `local-pattern-cover-svg` for a clean local cover/placeholder.

AI-generated crochet/knit images still need Crafties-eye review. If Nath has a real sample photo or a physical pattern sheet, that remains the ground truth.

## Safety note for candle patterns

For Team Crafties candle crafts, prompt and write them as real poured wax candle crafts when appropriate: heat-safe jar, melted candle wax, cotton wick, pour/cure/trim, and removable decorations/labels that come off before lighting.
