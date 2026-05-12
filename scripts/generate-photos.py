#!/usr/bin/env python3
"""
Generate photorealistic finished-product photos for all 90 Crafties patterns
using Pollinations AI (free, no API key needed).
"""

import urllib.request
import urllib.parse
import json
import os
import time

OUTPUT_DIR = "/Users/posty/Documents/New project/Crafties/assets/product-photos"

# Photorealistic prompt template — warm craft photography style
BASE_STYLE = (
    "photorealistic photo, warm natural light, cozy craft table, "
    "soft bokeh background, handmade aesthetic, beautiful craft photography, "
    "high quality, close-up, pastel wood surface"
)

# Per-pattern prompts — specific and descriptive
PATTERNS = [
    # === YARN ===
    ("chunky-crochet-heart", "a finished handmade chunky crochet heart in soft pink yarn, lying on a wooden table, " + BASE_STYLE),
    ("beginner-granny-square", "a finished crochet granny square in multicolour yarn, pastel colors, flat lay on linen, " + BASE_STYLE),
    ("soft-yarn-bookmark", "a soft handmade yarn tassel bookmark resting on an open book, pastel ribbon, " + BASE_STYLE),
    ("macrame-keychain-loop", "a handmade macramé keychain with boho knots and fringe, hanging from fingers, cream cotton cord, " + BASE_STYLE),
    ("tiny-knit-coaster", "a tiny hand-knitted round coaster in soft wool yarn under a warm mug, " + BASE_STYLE),
    ("pom-pom-flower", "a cheerful handmade pom-pom flower in colorful yarn petals, tied with ribbon, " + BASE_STYLE),
    ("crochet-cup-cozy", "a finished crocheted cup cozy wrapped around a coffee cup, cozy morning scene, " + BASE_STYLE),
    ("braided-yarn-bracelet", "a handmade braided yarn friendship bracelet in pastel colors on a wrist, " + BASE_STYLE),
    ("mini-tassel-garland", "a tiny handmade yarn tassel garland hanging on a wall, pastel rainbow colors, " + BASE_STYLE),
    ("simple-yarn-wrapped-letter", "a handmade yarn-wrapped decorative letter in pastel purple yarn on a shelf, " + BASE_STYLE),

    # === PAINTING ===
    ("kindness-painted-pebble", "smooth river pebbles hand-painted with colorful kindness words and flowers, on a wooden surface, " + BASE_STYLE),
    ("watercolor-bloom-card", "a delicate handmade watercolor floral greeting card with soft pink and lavender blooms, " + BASE_STYLE),
    ("acrylic-dot-rainbow", "a small canvas with a cheerful acrylic dot-art rainbow painting, mandala dots, " + BASE_STYLE),
    ("painted-jar-lantern", "a glass jar hand-painted with flowers used as a lantern with warm candlelight inside, " + BASE_STYLE),
    ("ceramic-mug-practice-motif", "a white ceramic mug hand-painted with a simple flower and dot motif, " + BASE_STYLE),
    ("glass-window-flower-cling", "colourful handmade gel flower window clings on a sunny window, translucent petals, " + BASE_STYLE),
    ("wood-slice-mini-painting", "a small wooden slice with a tiny hand-painted landscape scene, wildflowers, " + BASE_STYLE),
    ("painted-plant-pot-band", "a terracotta plant pot with a hand-painted floral band decoration, succulents inside, " + BASE_STYLE),
    ("sunset-color-swatch", "a beautiful hand-painted watercolor sunset color swatch card in warm oranges and purples, " + BASE_STYLE),
    ("teal-flower-thank-you-tag", "a hand-painted teal flower gift tag on kraft paper with twine, " + BASE_STYLE),

    # === SEWING ===
    ("sweet-patch-pocket", "a cute handmade fabric patch pocket sewn onto denim, embroidered flowers, " + BASE_STYLE),
    ("felt-heart-ornament", "a tiny handmade felt heart ornament with button details and ribbon loop, hanging, " + BASE_STYLE),
    ("scrap-fabric-bookmark", "a handmade fabric scrap bookmark with stitched edges and ribbon tail, resting on a book, " + BASE_STYLE),
    ("beginner-drawstring-pouch", "a small handmade fabric drawstring pouch in floral cotton print, tied shut, " + BASE_STYLE),
    ("tiny-lavender-sachet", "a tiny handmade lavender sachet bag in white linen with dried lavender sprig tied with ribbon, " + BASE_STYLE),
    ("embroidered-name-patch", "a handmade embroidered name patch on white fabric with colorful stitching, " + BASE_STYLE),
    ("simple-button-flower", "a charming handmade button flower brooch with layered fabric petals, " + BASE_STYLE),
    ("fabric-scrap-coaster", "a set of handmade patchwork fabric coasters in colorful cotton scraps on a table, " + BASE_STYLE),
    ("hand-stitched-mini-pillow", "a tiny handmade embroidered mini pillow with cross-stitch flowers, soft cotton, " + BASE_STYLE),
    ("no-waste-gift-bow", "a beautiful handmade fabric scrap gift bow on a wrapped present, zero-waste, " + BASE_STYLE),

    # === DRAWING ===
    ("tiny-doodle-garden", "a sweet hand-drawn pen and ink tiny garden doodle on white paper, flowers and plants, " + BASE_STYLE),
    ("kindness-quote-border", "a hand-lettered kindness quote with illustrated floral border on paper, " + BASE_STYLE),
    ("five-minute-flower-study", "a delicate hand-drawn botanical flower study sketch on cream paper, pencil and ink, " + BASE_STYLE),
    ("cozy-craft-room-sketch", "a charming hand-drawn cozy craft room interior sketch, pencil illustration, " + BASE_STYLE),
    ("beginner-mandala-circle", "a hand-drawn beginner mandala circle in black pen on white paper, geometric patterns, " + BASE_STYLE),
    ("little-hippo-practice-page", "a sweet hand-drawn baby hippo doodle sheet on paper with colored pencils nearby, " + BASE_STYLE),
    ("leaf-pattern-sampler", "a hand-drawn botanical leaf pattern sampler page with various leaf shapes in ink, " + BASE_STYLE),
    ("happy-house-doodle", "a charming hand-drawn cozy house doodle with garden and flowers, black pen on paper, " + BASE_STYLE),
    ("patterned-heart-sheet", "a hand-drawn sheet filled with doodled patterned hearts in various styles, black pen, " + BASE_STYLE),
    ("daily-tiny-object-prompt", "a collection of tiny hand-drawn everyday object sketches on a page, ink drawing, " + BASE_STYLE),

    # === WOOD ===
    ("little-twig-star", "a handmade star ornament made from small natural twigs tied with twine, rustic, " + BASE_STYLE),
    ("painted-wood-slice-tag", "handmade painted wood slice gift tags with flowers and handwritten text, " + BASE_STYLE),
    ("pallet-scrap-mini-sign", "a small rustic handmade wood pallet scrap sign with hand-painted words, " + BASE_STYLE),
    ("twig-photo-holder", "a handmade rustic twig photo holder standing up displaying a small photo, " + BASE_STYLE),
    ("simple-branch-mobile", "a beautiful handmade natural branch mobile with hanging crystals and feathers, " + BASE_STYLE),
    ("wood-bead-garland", "a handmade natural wood bead garland with cotton knots hanging decoratively, " + BASE_STYLE),
    ("rustic-plant-marker", "handmade rustic wooden stick plant markers with hand-painted herb names in a garden, " + BASE_STYLE),
    ("tiny-driftwood-boat", "a tiny handmade driftwood toy sailboat with fabric sail on a wooden surface, " + BASE_STYLE),
    ("scrap-wood-coaster", "a set of handmade scrap wood coasters with burned or painted designs, " + BASE_STYLE),
    ("nature-stick-loom", "a handmade nature stick frame loom with woven yarn in earthy colors, " + BASE_STYLE),

    # === JEWELRY ===
    ("friendship-bead-bracelet", "colorful handmade beaded friendship bracelets in pastel colors on a wrist, " + BASE_STYLE),
    ("simple-cord-necklace", "a simple handmade waxed cord necklace with a single natural stone pendant, " + BASE_STYLE),
    ("stretch-ring-stack", "a set of handmade beaded stretch rings stacked on fingers, delicate and colorful, " + BASE_STYLE),
    ("charm-safety-pin-brooch", "a handmade safety pin charm brooch with tiny colorful beads and charms, " + BASE_STYLE),
    ("macrame-wish-bracelet", "a delicate handmade macramé wish bracelet in cream cotton with a knot closure, " + BASE_STYLE),
    ("paper-bead-necklace", "a colorful handmade paper bead necklace with glossy rolled paper beads, " + BASE_STYLE),
    ("button-bracelet", "a fun handmade button bracelet with assorted colorful vintage buttons on elastic, " + BASE_STYLE),
    ("clay-look-bead-charm", "handmade air-dry clay bead charms with painted patterns on a keychain, " + BASE_STYLE),
    ("tiny-tassel-earrings", "a pair of handmade tiny thread tassel earrings in blush pink and gold, " + BASE_STYLE),
    ("memory-color-anklet", "a handmade colorful seed bead and thread memory anklet, summery and bright, " + BASE_STYLE),

    # === SOAP ===
    ("sweet-soap-wrap", "a handmade soap bar wrapped in kraft paper with a pretty ribbon and dried flower, " + BASE_STYLE),
    ("simple-soap-gift-band", "a handmade decorative paper band wrapped around a soap bar, stamped design, " + BASE_STYLE),
    ("dried-flower-soap-tag", "a beautiful handmade gift tag for soap with pressed dried flowers and twine, " + BASE_STYLE),
    ("beginner-melt-and-pour-heart", "a handmade pastel heart-shaped melt and pour soap with lavender buds inside, " + BASE_STYLE),
    ("soap-sample-envelope", "tiny handmade kraft paper envelopes holding soap sample slices tied with twine, " + BASE_STYLE),
    ("kindness-scent-label", "a handmade beautifully designed soap label with floral watercolor illustration, " + BASE_STYLE),
    ("mini-soap-basket", "a handmade gift basket with mini soaps, dried flowers, and ribbon, " + BASE_STYLE),
    ("washcloth-soap-pocket", "a handmade washcloth folded as a pocket holding a soap bar, tied with ribbon, " + BASE_STYLE),
    ("color-swirl-practice-bar", "a handmade colorful swirled cold process soap bar in pastel purple and cream, " + BASE_STYLE),
    ("spa-night-gift-sleeve", "a handmade spa gift sleeve with soap candle and bath salts in a cozy bundle, " + BASE_STYLE),

    # === CANDLES ===
    ("cozy-candle-label", "a glass jar candle with a beautiful handmade illustrated label, warm glow, " + BASE_STYLE),
    ("safety-gift-tag", "a handmade candle safety instruction gift tag tied to a candle jar with ribbon, " + BASE_STYLE),
    ("jar-candle-wrap-band", "a glass jar candle with a handmade decorative paper band wrap with pressed flowers, " + BASE_STYLE),
    ("pressed-flower-jar-collar", "a glass candle jar with a handmade pressed flower collar around the top, " + BASE_STYLE),
    ("cozy-scent-name-card", "a small handmade illustrated scent description card beside a candle, " + BASE_STYLE),
    ("tea-light-paper-tray", "handmade folded paper origami trays holding tea light candles, soft glow, " + BASE_STYLE),
    ("candle-care-mini-card", "a tiny handmade candle care instruction mini card with illustrations, " + BASE_STYLE),
    ("ribbon-wrapped-candle-gift", "a glass jar candle beautifully wrapped with ribbon and a handmade gift tag, " + BASE_STYLE),
    ("seasonal-candle-sticker", "handmade seasonal illustrated stickers on a candle jar, autumn or winter theme, " + BASE_STYLE),
    ("kindness-glow-gift-set", "a beautiful handmade candle gift set with cards, dried flowers, and ribbon, " + BASE_STYLE),

    # === CARDS ===
    ("thank-you-flower-card", "a handmade thank-you greeting card with pressed flowers and hand-lettering, " + BASE_STYLE),
    ("pop-up-heart-card", "a handmade pop-up paper heart card opened to reveal a 3D heart, " + BASE_STYLE),
    ("scrap-paper-rainbow-card", "a handmade rainbow card made from torn colorful paper scraps, cheerful, " + BASE_STYLE),
    ("beginner-birthday-banner-card", "a handmade birthday card with a tiny banner bunting and balloons, " + BASE_STYLE),
    ("kindness-pocket-note", "a tiny handmade folded pocket kindness note with flowers, ready to give, " + BASE_STYLE),
    ("pressed-leaf-card", "a handmade greeting card decorated with real pressed autumn leaves, " + BASE_STYLE),
    ("washi-tape-frame-card", "a handmade card with a washi tape decorative frame around a handwritten note, " + BASE_STYLE),
    ("mini-envelope-set", "a set of handmade tiny paper envelopes in pastel colors with mini cards inside, " + BASE_STYLE),
    ("painted-dot-greeting-card", "a handmade greeting card with cheerful painted dot art pattern, acrylic paint, " + BASE_STYLE),
    ("crafties-welcome-card", "a handmade beautifully decorated welcome card with flowers and warm colors, " + BASE_STYLE),
]

def generate_photo(slug, prompt, retries=3):
    encoded = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=900&height=680&nologo=true&seed={abs(hash(slug)) % 99999}"
    out_path = os.path.join(OUTPUT_DIR, f"{slug}.jpg")
    
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
                if len(data) > 5000:  # valid image
                    with open(out_path, 'wb') as f:
                        f.write(data)
                    return True, len(data)
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(3)
            else:
                return False, str(e)
    return False, "max retries"

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    total = len(PATTERNS)
    success = 0
    failed = []
    
    for i, (slug, prompt) in enumerate(PATTERNS, 1):
        print(f"[{i}/{total}] {slug}...", flush=True)
        ok, info = generate_photo(slug, prompt)
        if ok:
            print(f"  ✓ {info} bytes", flush=True)
            success += 1
        else:
            print(f"  ✗ FAILED: {info}", flush=True)
            failed.append(slug)
        time.sleep(1)  # be gentle
    
    print(f"\n=== DONE: {success}/{total} generated ===")
    if failed:
        print(f"Failed: {failed}")
