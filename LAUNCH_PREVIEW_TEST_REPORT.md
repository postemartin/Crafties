# Crafties Launch Preview Test Report

**Tested:** 2026-05-02 07:48:43 EDT  
**Tester:** Hermy  
**Target:** Local static Crafties site loaded from `file:///Users/posty/Documents/New project/Crafties/index.html`

Update note (2026-05-12): Crafties now contains 91 pattern pages after adding `crochet-plant-pot-cover`. The checklist values below are preserved as the original 2026-05-02 test snapshot.

## Summary

**Result:** Pass for small trusted preview.

No blocking bugs were found. Crafties is ready to show to 2–3 kind previewers for first impressions.

## Automated / Structural Checks

Homepage checks:

- [x] Homepage loads from local `file://` path.
- [x] Page title present: `Crafties — Free patterns, kind ideas, handmade joy`.
- [x] No duplicate IDs found.
- [x] No missing hash-anchor targets found.
- [x] 90 pattern cards found.
- [x] Images loaded successfully.
- [x] Desktop width has no horizontal overflow: `scrollWidth 1280`, `clientWidth 1280`.
- [x] English homepage text present on first load.
- [x] French toggle switches page language to `fr`.
- [x] French hero/search/start text appears after switching.
- [x] Search for `twig` returns 10 visible pattern cards.

Featured pattern page checks:

- [x] All 9 featured beginner pattern pages loaded in the 390px harness.
- [x] 390px harness result: `count: 9`, `failureCount: 0`.
- [x] All 9 featured beginner pattern pages loaded in the 320px harness.
- [x] 320px harness result: `count: 9`, `failureCount: 0`.
- [x] Pattern pages include required sections/links in the harness checks.
- [x] Headless Chrome stderr scan for the 320px rerun was empty.

## Visual QA Notes

Homepage visual inspection found no broken images, severe clipping, or major overlap.

Small non-blocking polish notes:

1. **Header navigation is a little crowded.** It works, but the number of top-level links makes the header feel busy.
2. **Homepage has many sections.** The Start Here path is clear, but first-time visitors may still see a lot of choices.
3. **Some small text may be hard to read.** Pattern-card/helper text could be slightly larger later.
4. **Category wording could be aligned later.** Example: “Cards” vs “Paper” in different areas.
5. **Demo/prototype actions could use stronger labels.** Forms are friendly, but some visitors may wonder whether submissions are real or preview-only.

None of these block a trusted preview.

## Screenshot Evidence

Homepage visual QA screenshot:

`/Users/posty/.hermes/cache/screenshots/browser_screenshot_094fb8e08744405f900224c15abbfecd.png`

## Preview Recommendation

Proceed with a small trusted preview.

Ask 2–3 people to answer:

1. What did you think Crafties was for within the first 10 seconds?
2. Was it obvious where to start?
3. Did the English/French toggle make sense?
4. Which of the 9 beginner projects would you actually try first?
5. Did anything feel confusing, too busy, or hard to read?
6. Did it feel warm and encouraging?
7. What one small thing would make it better?

## Suggested Next Fix After Preview

If previewers agree the site feels warm and clear, the next best polish task is likely:

**Make preview/demo actions more clearly labeled as preview-only**, especially forms for sharing, gallery, challenges, maker cards, and live table prompts.
