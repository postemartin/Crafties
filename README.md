# 🦛 Crafties — Free patterns, kind ideas, handmade joy

> A cozy arts-and-crafts community built by Nath. Free patterns, beginner-friendly, zero sales pressure.

![Crafties hippo mascot](assets/crafties-hippo-logo-192.png)

## ✨ What is Crafties?

Crafties is a warm, welcoming website for makers of all skill levels — especially beginners. It features:

- 🧶 **99 free beginner patterns** across 9 craft categories
- 📸 **Enhanced finished-project photo previews** for every pattern (AI-generated previews, ready to replace with real community photos later)
- 💜 **Kind community spirit** — positive feedback only, no sales pressure
- 🌐 **Bilingual (EN/FR)** homepage and featured starter-pattern pages; the full 99-page library is ready for deeper translation as Crafties grows
- 🦛 **Nath's purple hippo mascot** — inspired by her real tattoo

## 🗂️ Structure

```
Crafties/
├── index.html                  ← Homepage (all sections)
├── patterns/                   ← 99 individual pattern pages
│   ├── chunky-crochet-heart.html
│   └── ... (98 more)
├── assets/
│   ├── gallery/                ← approved public gallery images copied in after moderation
│   ├── product-photos/         ← 99 enhanced finished-project previews + manifest.json
│   ├── crafties-hippo-logo-64.png
│   ├── crafties-hippo-logo-192.png
│   ├── crafties-hippo-logo-512.png
│   └── crafties-hippo-logo-lilac.png
├── data/
│   └── approved-gallery.json   ← curated public gallery cards rendered on the homepage
├── docs/
│   ├── gallery-moderation-workflow.md
│   └── pattern-image-toolkit.md        ← local usage guide for Nath's pattern assets
├── scripts/
│   ├── generate-photos.py              ← Pollinations AI batch photo generator
│   ├── pattern-image-toolkit.py        ← preset-based FAL/Recraft/diagram toolkit
│   └── pattern-image-presets.json      ← Team Crafties image preset config
├── thanks.html                 ← post-submit thank-you page for gallery uploads
├── netlify.toml                ← Netlify deployment config
└── README.md                   ← This file
```

## 🎨 Categories

| Category | Patterns | Emoji |
|----------|----------|-------|
| Yarn | 19 | 🧶 |
| Painting | 10 | 🎨 |
| Sewing | 10 | 🪡 |
| Drawing | 10 | ✏️ |
| Wood | 10 | 🪵 |
| Jewelry | 10 | 📿 |
| Soap | 10 | 🫧 |
| Candles | 10 | 🕯️ |
| Cards | 10 | 💌 |

## 🚀 Deploy to Cloudflare Pages

The live Crafties site at https://teamcrafties.com is served by **Cloudflare Pages** — not Netlify. The Netlify project still exists for gallery form intake only (the `gallery-submission` form lands in Netlify Forms → manual approval → `data/approved-gallery.json`).

Current verified deployment flow:

1. Make changes in this repo (commit them)
2. Confirm wrangler is installed and logged in:
   ```bash
   npm install -g wrangler          # one-time
   wrangler whoami                  # must show postenathalie@gmail.com
   ```
3. Run the deploy (a `package.json` shortcut exists, or use the raw command):
   ```bash
   npm run deploy                    # uses wrangler under the hood
   # ...which is equivalent to:
   wrangler pages deploy . --project-name=team-crafties --branch=main --commit-hash=$(git rev-parse HEAD)
   ```
4. Verify it landed:
   ```bash
   npm run deploy:status             # lists the most recent deployments
   curl -sS -I -L https://teamcrafties.com | head -5   # should return 200 + server: cloudflare
   ```

Useful notes:
- Publish directory: `.` (root)
- Build command: none needed — it's pure HTML/CSS/JS
- CF Pages project: `team-crafties` (Pages subdomain: `team-crafties-czq.pages.dev`)
- **Git Provider = "No"** — pushing to GitHub `main` does NOT trigger a deploy. Deployments are CLI-direct via `wrangler pages deploy`.
- Auth lives at `~/Library/Preferences/.wrangler/config/default.toml` (macOS). If `wrangler login` ever expires, just re-run it — never run `wrangler logout`.
- Use `npm run deploy:dry-run` to validate a deploy without shipping (prints the file plan).

### About Netlify (secondary, form-intake only)

Netlify still owns the gallery form handler. Do NOT run `netlify unlink` or you'll break the form. The Netlify project id (for reference) is `e307063d-6faf-424f-94ee-737d1c9b3168`.

## 🖼️ Regenerating Photo Previews

If you want to refresh the AI-generated photos:

```bash
cd /path/to/Crafties
python3 scripts/generate-photos.py
```

Requirements: Python 3, `requests` library (`pip install requests`).
Photo previews are fetched from [Pollinations AI](https://pollinations.ai) — free, no API key needed — then gently enhanced locally for brightness, color, contrast, and sharpness.

## 🧰 Pattern Image Toolkit

For Nath's current pattern workflow, use the local toolkit instead of hand-picking a model every time:

```bash
npm run toolkit:check
npm run toolkit:list
```

It provides presets for realistic finished-project images, yarn/crochet texture photos, Recraft-style pattern covers, text/label graphics, social squares, and deterministic SVG assembly diagrams. AI drafts are saved under `.crafties-toolkit/` and ignored by Git/Netlify until an approved asset is copied into the public site.

Full usage: `docs/pattern-image-toolkit.md`.

## 💜 Community features status

The current version is a **launch preview** with one real community step already live:

- ✅ Real **private gallery intake** via Netlify form upload
- ✅ Real **approved public gallery wall** rendered from `data/approved-gallery.json`
- 🚧 Member accounts & profiles are still demo-only
- 🚧 Kind comments & cheers are still demo-only
- 🚧 Artist of the Day nominations are still demo-only
- 🚧 Weekly challenge board is still demo-only

### Private-intake → approved-wall workflow

1. A maker submits the private `gallery-submission` form
2. The submission lands in Netlify Forms for review
3. Nath approves only the safe, consented projects
4. Approved cards are added manually to `data/approved-gallery.json`
5. The homepage gallery fetches that JSON file on load

See `docs/gallery-moderation-workflow.md` for the exact checklist and JSON entry format.

## 🦛 About the mascot

The Crafties hippo is Nath's design — a round, sweet, purple-lilac hippopotamus with a teal flower and sparkles, based on her real tattoo. She's the heart of the community.

---

Made with 💜 by Nath & Team Crafties
