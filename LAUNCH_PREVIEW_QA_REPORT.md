# Crafties Launch Preview QA Report

Date: 2026-05-08
Scope: homepage, enhanced image pass, sample printable pattern pages, EN/FR toggles, search/filter interactions, image integrity, mobile overflow.

Update note (2026-05-12): Crafties now contains 91 pattern pages after adding `crochet-plant-pot-cover`. Historical measurements below reflect the original 2026-05-08 QA pass unless a line explicitly refers to the current state.

## Executive summary

Status: **Passed for launch-preview review**

- Blockers: 0
- High severity issues: 0
- Medium severity issues fixed during pass: 1
- Low/non-blocking notes: 1
- Launch-polish enhancements added during pass: 1

## What was tested

- Local server preview at `http://127.0.0.1:8787/index.html`
- Homepage first-visitor flow
- Pattern library search/filter behavior
- Homepage EN/FR language toggle
- Sample featured pattern EN/FR toggle
- Sample non-featured pattern pages
- Image loading and integrity
- Mobile overflow at 390px and 320px
- Console/page errors
- Duplicate IDs and missing hash anchors

## Deterministic checks

- HTML files checked: 91
- Image references checked: 366
- Missing image references: 0
- Product JPGs verified readable: 95
- Product JPGs polished: 95
- Broken product JPGs: 0
- Homepage pattern cards: 90
- Homepage cards with product photos: 90
- Gallery cards with photo previews: 4
- Duplicate IDs: 0
- Missing hash anchors: 0
- Console/page errors during Playwright QA: 0
- Mobile overflow at 390px: 0 tested pages
- Mobile overflow at 320px: 0 tested pages
- Pattern pages with enhanced preview badge: 90 / 90
- Pattern pages with FR toggle: 9 / 90 featured starter pages

## Fixes made during QA

### 1. Pattern library empty search was visually inconsistent

Severity: Medium  
Category: Functional / UX  
URL: `/index.html#library`

Problem:
- Searching for a nonsense query showed the empty-state message, but the enhanced image cards were still visible.
- Cause: `.pattern-card.has-product-image` had a later `display:grid` rule that overrode `.pattern-card.hide{display:none}`.

Fix:
- Added a stronger hide rule:
  - `.pattern-card.hide`
  - `.pattern-card.has-product-image.hide`
  - `.pattern-card.updated-product-card.hide`
  - all now use `display:none!important`.

Verified:
- Search `crochet` now shows 10 relevant cards.
- Search `zzzz-no-pattern` now shows 0 cards and the empty note.

### 2. README wording was too broad about bilingual coverage

Severity: Low  
Category: Content accuracy

Problem:
- README said bilingual content was available “throughout,” but only the homepage and the 9 featured starter-pattern pages currently include FR toggles.

Fix:
- Updated README to say:
  - “Bilingual (EN/FR) homepage and featured starter-pattern pages; the full 90-page library is ready for deeper translation as Crafties grows.”

### 3. Product photos received a warmer polish pass

Severity: Polish  
Category: Visual / Image quality  
URL: `/index.html#library` and `/patterns/*.html`

Enhancement:
- Added `scripts/polish-product-photos.py` for a repeatable non-logo photo polish pass.
- Applied gentle autocontrast, warmer saturation, mild contrast/brightness lift, and detail sharpening to all 95 product JPGs.
- Selectively lifted darker photos and softened a few very bright photos.
- Left mascot/logo files untouched so Nath’s corrected teal flower and lilac hippo colors stay safe.

Verified:
- 90 homepage library cards still resolve to matching product photos.
- 90 pattern pages still reference their finished-project photo previews.
- Product-photo manifest is updated to `photo-polish-2026-05-08`.
- Browser/Playwright QA found 0 broken loaded images and 0 bad image URL checks.

### 4. Homepage received a launch-polish pass

Severity: Polish  
Category: UX / Content clarity / First impression  
URL: `/index.html`

Enhancement:
- Simplified the top navigation from a long preview menu to 6 visitor-facing links.
- Rewrote the hero copy to explain Crafties immediately: free beginner-friendly patterns, project ideas, photo previews, and gentle encouragement.
- Reduced the hero CTAs to 3 clear choices: browse patterns, start here, and see the gallery.
- Added a three-card “Crafties at a glance” strip: Browse, Choose, Share kindly.
- Renamed the internal-sounding “Crafties launch preview” section to “What you’ll find on Crafties.”
- Changed the homepage library to a curated starter shelf: 12 pattern cards show first, with a “Show all 90 free patterns” button.
- Search and category filters still open the full shelf automatically.

Verified:
- Initial homepage library shows 12 visible pattern cards instead of dumping all 90 immediately.
- The “Show all 90 free patterns” button exists.
- Hero mascot remains `assets/crafties-hippo-logo-lilac.png`.
- Browser visual QA found a clearer first screen, no missing mascot, no obvious overlap, and no broken layout.
- Console after visual load: 0 messages / 0 JS errors.

## Non-blocking note

The full 90-page pattern library is visually polished and usable, but only 9 featured starter pattern pages currently have the richer EN/FR toggle. This is acceptable for launch preview if we describe it honestly; a future translation pass can expand FR content to all 90 pattern pages.

## Visual QA notes

Mobile 390px screenshot reviewed:
- No horizontal overflow visible.
- Text remains readable.
- Cards fit within viewport.
- No sticky-header overlap visible in the reviewed mobile screenshot.
- No image crop issue visible in the reviewed screenshot.

## Result

Crafties is ready for a human launch-preview review. Recommended next step: send/open the preview for Nath/family/friend feedback, then choose whether the next build pass should be **full French translation for all 90 pattern pages** or **real community-upload planning**.
