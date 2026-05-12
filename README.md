# 🦛 Crafties — Free patterns, kind ideas, handmade joy

> A cozy arts-and-crafts community built by Nath. Free patterns, beginner-friendly, zero sales pressure.

![Crafties hippo mascot](assets/crafties-hippo-logo-192.png)

## ✨ What is Crafties?

Crafties is a warm, welcoming website for makers of all skill levels — especially beginners. It features:

- 🧶 **91 free beginner patterns** across 9 craft categories
- 📸 **Enhanced finished-project photo previews** for every pattern (AI-generated previews, ready to replace with real community photos later)
- 💜 **Kind community spirit** — positive feedback only, no sales pressure
- 🌐 **Bilingual (EN/FR)** homepage and featured starter-pattern pages; the full 91-page library is ready for deeper translation as Crafties grows
- 🦛 **Nath's purple hippo mascot** — inspired by her real tattoo

## 🗂️ Structure

```
Crafties/
├── index.html                  ← Homepage (all sections)
├── patterns/                   ← 91 individual pattern pages
│   ├── chunky-crochet-heart.html
│   └── ... (90 more)
├── assets/
│   ├── product-photos/         ← 91 JPG enhanced finished-project previews + manifest.json
│   ├── crafties-hippo-logo-64.png
│   ├── crafties-hippo-logo-192.png
│   ├── crafties-hippo-logo-512.png
│   └── crafties-hippo-logo-lilac.png
├── scripts/
│   └── generate-photos.py      ← Pollinations AI batch photo generator
├── netlify.toml                ← Netlify deployment config
└── README.md                   ← This file
```

## 🎨 Categories

| Category | Patterns | Emoji |
|----------|----------|-------|
| Yarn | 11 | 🧶 |
| Painting | 10 | 🎨 |
| Sewing | 10 | 🪡 |
| Drawing | 10 | ✏️ |
| Wood | 10 | 🪵 |
| Jewelry | 10 | 📿 |
| Soap | 10 | 🫧 |
| Candles | 10 | 🕯️ |
| Cards | 10 | 💌 |

## 🚀 Deploy to Netlify

This repo is linked to the live Crafties site at https://teamcrafties.com.

Current deployment flow:

1. Push changes to `main`
2. GitHub Actions triggers the Netlify production deploy hook
3. Netlify publishes the updated static site

Useful notes:
- Publish directory: `.` (root)
- Build command: none needed — it's pure HTML/CSS/JS
- Local/manual fallback: `netlify deploy --prod --dir .`

You can still drag-and-drop the entire folder to [netlify.com/drop](https://app.netlify.com/drop) for a one-off preview deploy.

## 🖼️ Regenerating Photo Previews

If you want to refresh the AI-generated photos:

```bash
cd /path/to/Crafties
python3 scripts/generate-photos.py
```

Requirements: Python 3, `requests` library (`pip install requests`).
Photo previews are fetched from [Pollinations AI](https://pollinations.ai) — free, no API key needed — then gently enhanced locally for brightness, color, contrast, and sharpness.

## 💜 Community features (coming soon)

The current version is a **launch preview** — pattern browsing works fully now. These features are prototyped and clearly marked as "demo" until the backend is ready:

- Real photo uploads & sharing
- Member accounts & profiles
- Kind comments & cheers
- Artist of the Day nominations
- Weekly challenge board

## 🦛 About the mascot

The Crafties hippo is Nath's design — a round, sweet, purple-lilac hippopotamus with a teal flower and sparkles, based on her real tattoo. She's the heart of the community.

---

Made with 💜 by Nath & Team Crafties
