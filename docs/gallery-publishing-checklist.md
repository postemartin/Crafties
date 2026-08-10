# Team Crafties approved gallery publishing checklist

Use this when Nath wants to move a real submission from the private intake queue into the public approved wall.

## Before you publish

Confirm all of these are true:

- The project photo is safe, kind, and clearly handmade.
- The maker gave permission for public display.
- No private personal information is visible in the image, filename, or note.
- The title and note feel encouraging and beginner-friendly.
- The image looks good enough to show on the public wall.

## Publish steps

1. Download the approved photo from the Netlify Forms submission.
2. Strip EXIF / device metadata before publishing.
   - Re-save the image with Preview, PIL, or another tool that removes camera metadata.
   - After re-saving, visually confirm the image is still upright. Some photos rely on orientation metadata and can appear sideways once that metadata is removed.
3. Rename it with a clean public filename.
   - Example: `approved-nath-flower-card.jpg`
4. Save it into:
   - `assets/gallery/`
5. Add a new object to:
   - `data/approved-gallery.json`
6. Fill in these fields:
   - `maker`
   - `type`
   - `title`
   - `note`
   - `image`
   - `alt`
   - `badge`
   - `cheers`
   - `tags`
   - `color`
7. Preview locally and confirm the card appears in the correct filter group.
8. Deploy the updated site.

## JSON starter template

```json
{
  "maker": "Maker name",
  "type": "Cards",
  "title": "Project title",
  "note": "A short kind note about the project.",
  "image": "assets/gallery/approved-project-photo.jpg",
  "alt": "Project title made by Maker name",
  "badge": "Approved by Team Crafties",
  "cheers": 0,
  "tags": ["paper", "cards"],
  "color": "#ffed72"
}
```

## Suggested craft type + tag guide

- Yarn → tags like `yarn`, `crochet`, `knitting`
- Sewing → tags like `sewing`, `embroidery`, `fabric`
- Painting → tags like `painting`, `watercolor`, `acrylic`
- Cards → tags like `paper`, `cards`
- Drawing → tags like `drawing`, `sketch`
- Jewelry → tags like `jewelry`, `beads`
- Soap → tags like `soap`, `gift`
- Candles → tags like `candles`, `label`
- Wood → tags like `wood`, `rustic`

## If you need to unpublish something

1. Remove the entry from `data/approved-gallery.json`.
2. Remove the public image from `assets/gallery/` if it should no longer stay in the site.
3. Redeploy the site.
4. Keep the original private submission only where appropriate.

## Notes

- Private submissions should never appear publicly by automation.
- The public wall is intentionally manual and consent-based.
- Starter examples can stay in the JSON file until enough real approved maker projects are ready.
