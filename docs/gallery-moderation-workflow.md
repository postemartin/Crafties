# Team Crafties gallery moderation workflow

This site now uses a **real private intake form** plus a **manually curated public gallery JSON file**.

## Private intake

- Form name: `gallery-submission`
- Delivery: Netlify Forms private submission inbox
- Redirect after submit: `/thanks.html`
- The upload includes:
  - maker name
  - email
  - craft type
  - project title
  - finished project photo
  - kind project note
  - consent to review
  - optional consent to public display

## Public approved wall

The public wall is rendered from:

- `data/approved-gallery.json`

Nothing from the intake form is shown automatically. To publish a maker project publicly, Nath must approve it first and then add a new JSON entry manually.

## How to approve a new project

1. Open the Netlify form submission for `gallery-submission`.
2. Confirm the photo is kind, safe, on-theme, and clearly finished enough to share.
3. Confirm there is explicit consent for public display.
4. Strip EXIF / device metadata from the approved image, then save it into `assets/gallery/` with a clean filename.
5. Add a new object to `data/approved-gallery.json` using this shape:

```json
{
  "maker": "Nath",
  "type": "Cards",
  "title": "Purple Hippo Thank-You Card",
  "note": "A tiny card with a flower and a brave beginner message.",
  "image": "assets/gallery/purple-hippo-thank-you-card.jpg",
  "alt": "Purple Hippo Thank-You Card made by Nath",
  "badge": "Approved by Team Crafties",
  "cheers": 0,
  "tags": ["paper", "cards"],
  "color": "#ffed72"
}
```

6. Deploy the site again so the updated JSON file is live.

## Suggested moderation checklist

Approve only if all are true:

- The photo is the submitter's work or they clearly have permission to share it.
- The maker note is kind and beginner-safe.
- No private personal information is visible in the image or note.
- The project fits the Crafties tone: encouraging, handmade, and no selling pressure.
- The display consent box was checked or written permission was confirmed later.

## If a submission should stay private

Leave it in Netlify Forms only. Do not copy it into `data/approved-gallery.json`, and do not place the image in `assets/gallery/`.
