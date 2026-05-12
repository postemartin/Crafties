#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const PATTERN_MANIFEST = path.join(ROOT, 'patterns', 'pattern-manifest.json');
const PHOTO_DIR = path.join(ROOT, 'assets', 'product-photos');
const PHOTO_MANIFEST = path.join(PHOTO_DIR, 'manifest.json');
const INDEX = path.join(ROOT, 'index.html');
const VERSION = 'finished-local-20260503-4';

const categoryMeta = {
  Yarn: { emoji: '🧶', color: '#f4b4ff', ink: '#53138f', tag: 'Yarn' },
  Painting: { emoji: '🎨', color: '#9cddff', ink: '#096eb3', tag: 'Painting' },
  Sewing: { emoji: '🪡', color: '#ff9cc7', ink: '#b31262', tag: 'Sewing' },
  Drawing: { emoji: '✏️', color: '#ffed72', ink: '#8a6100', tag: 'Drawing' },
  Wood: { emoji: '🪵', color: '#ffbd72', ink: '#8a4d12', tag: 'Wood' },
  Jewelry: { emoji: '📿', color: '#85f2bf', ink: '#087548', tag: 'Jewelry' },
  Soap: { emoji: '🫧', color: '#86ecff', ink: '#007f99', tag: 'Soap' },
  Candles: { emoji: '🕯️', color: '#ffbd5a', ink: '#9b4d00', tag: 'Candles' },
  Cards: { emoji: '💌', color: '#b7abff', ink: '#4d39b8', tag: 'Cards' }
};

function escapeXml(value) {
  return String(value).replace(/[&<>"']/g, ch => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;'
  }[ch]));
}

function slugify(title) {
  return title
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/&/g, ' and ')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}

function findExistingAssetSlug(title) {
  const ideal = slugify(title);
  const files = fs.readdirSync(PHOTO_DIR).filter(file => file.endsWith('.svg'));
  if (files.includes(`${ideal}.svg`)) return ideal;
  const collapsedIdeal = ideal.replace(/macrame/g, 'macram');
  const match = files.find(file => file.replace(/\.svg$/, '') === collapsedIdeal);
  return match ? match.replace(/\.svg$/, '') : ideal;
}

function findPatternPageSlug(assetSlug) {
  const files = fs.readdirSync(path.join(ROOT, 'patterns')).filter(file => file.endsWith('.html'));
  if (files.includes(`${assetSlug}.html`)) return assetSlug;
  const macram = assetSlug.replace(/macrame/g, 'macram');
  if (files.includes(`${macram}.html`)) return macram;
  return assetSlug;
}

function seedFor(text) {
  let seed = 0;
  for (let i = 0; i < text.length; i += 1) seed = (seed * 31 + text.charCodeAt(i)) % 9973;
  return seed;
}

function titleLine(title) {
  if (title.length <= 28) return escapeXml(title);
  const parts = title.split(' ');
  let line = '';
  for (const part of parts) {
    if ((line + ' ' + part).trim().length > 28) break;
    line = (line + ' ' + part).trim();
  }
  return escapeXml(line || title.slice(0, 26));
}

function objectSvg(title, category, seed) {
  const lower = title.toLowerCase();
  const wobble = (seed % 13) - 6;
  const stripe = ['#9b3dff', '#ff4fa3', '#22d7a5', '#fff65c', '#35b7ff'][seed % 5];
  const purple = '#53138f';

  if (category === 'Yarn') {
    if (lower.includes('heart')) return `<g transform="translate(${wobble} 0)" filter="url(#objectShadow)"><path d="M454 239c-54-72-168-28-168 67 0 110 168 184 168 184s168-74 168-184c0-95-114-139-168-67z" fill="#ff4fa3" stroke="${purple}" stroke-width="18"/><path d="M342 318c74-45 137 36 226-16M362 382c68-34 119 27 184-12M416 455c42-18 78 10 118-8" fill="none" stroke="#fff" stroke-width="15" stroke-linecap="round" opacity=".82"/><circle cx="650" cy="420" r="62" fill="#f4b4ff" stroke="${purple}" stroke-width="13"/><path d="M610 419c35-31 67-31 99 0M623 383c20 34 41 67 60 105" fill="none" stroke="#fff" stroke-width="11" stroke-linecap="round"/></g>`;
    if (lower.includes('garland')) return `<g filter="url(#objectShadow)"><path d="M210 280c136 116 342 114 480 0" fill="none" stroke="${purple}" stroke-width="16" stroke-linecap="round"/><circle cx="260" cy="308" r="46" fill="#ff4fa3" stroke="${purple}" stroke-width="10"/><circle cx="370" cy="352" r="46" fill="#fff65c" stroke="${purple}" stroke-width="10"/><circle cx="494" cy="352" r="46" fill="#22d7a5" stroke="${purple}" stroke-width="10"/><circle cx="620" cy="310" r="46" fill="#9b3dff" stroke="${purple}" stroke-width="10"/><path d="M240 354v75M370 398v82M494 398v82M620 354v75" stroke="#fff" stroke-width="13" stroke-linecap="round"/></g>`;
    if (lower.includes('bookmark')) return `<g filter="url(#objectShadow)"><path d="M340 142h210v360l-105-76-105 76z" fill="#fff65c" stroke="${purple}" stroke-width="16"/><path d="M384 232h122M384 286h96" stroke="#ff4fa3" stroke-width="20" stroke-linecap="round"/><circle cx="444" cy="360" r="42" fill="#22d7a5" stroke="${purple}" stroke-width="11"/><path d="M446 141c-46 33-68 71-65 116" fill="none" stroke="#f4b4ff" stroke-width="14" stroke-linecap="round"/></g>`;
    if (lower.includes('cozy')) return `<g filter="url(#objectShadow)"><rect x="302" y="210" width="254" height="224" rx="46" fill="#f4b4ff" stroke="${purple}" stroke-width="16"/><path d="M314 292h228M314 358h228" stroke="#fff" stroke-width="15" stroke-linecap="round"/><path d="M557 272h46c48 0 48 104 0 104h-46" fill="none" stroke="${purple}" stroke-width="19"/><rect x="342" y="248" width="174" height="64" rx="26" fill="#ff4fa3" opacity=".72"/></g>`;
    return `<g filter="url(#objectShadow)"><rect x="318" y="180" width="248" height="248" rx="44" fill="#f4b4ff" stroke="${purple}" stroke-width="16"/><path d="M344 304h196M442 204v196M366 238l152 134M520 238L366 372" stroke="#fff" stroke-width="13" stroke-linecap="round" opacity=".76"/><rect x="372" y="234" width="136" height="136" rx="24" fill="${stripe}" stroke="${purple}" stroke-width="12" opacity=".94"/></g>`;
  }

  if (category === 'Painting') {
    if (lower.includes('jar')) return `<g filter="url(#objectShadow)"><rect x="338" y="152" width="226" height="340" rx="54" fill="#dffbff" stroke="${purple}" stroke-width="16"/><rect x="368" y="112" width="166" height="70" rx="22" fill="#fff65c" stroke="${purple}" stroke-width="13"/><path d="M383 315c48-70 103 20 148-44" fill="none" stroke="#22d7a5" stroke-width="20" stroke-linecap="round"/><circle cx="412" cy="255" r="30" fill="#ff4fa3"/><circle cx="492" cy="240" r="26" fill="#9b3dff"/><path d="M380 424h140" stroke="#fff" stroke-width="18" stroke-linecap="round"/></g>`;
    if (lower.includes('pebble')) return `<g filter="url(#objectShadow)"><path d="M256 380c14-96 111-147 218-126 111 21 178 83 148 163-27 75-127 102-237 82-92-17-142-51-129-119z" fill="#d7d1c8" stroke="${purple}" stroke-width="16"/><path d="M362 360c25-35 62 11 83 40 20-37 58-75 91-36 38 45-91 101-91 101s-117-55-83-105z" fill="#ff4fa3"/><path d="M330 330c70-45 153-31 220 18" fill="none" stroke="#fff" stroke-width="10" opacity=".64"/></g>`;
    return `<g filter="url(#objectShadow)"><rect x="274" y="138" width="306" height="314" rx="32" fill="#fff" stroke="${purple}" stroke-width="16"/><circle cx="362" cy="258" r="47" fill="#ff4fa3"/><circle cx="462" cy="236" r="42" fill="#35b7ff"/><path d="M334 390c62-98 153 20 202-84" fill="none" stroke="#22d7a5" stroke-width="25" stroke-linecap="round"/><path d="M555 405l94 76" stroke="#8a4d12" stroke-width="21" stroke-linecap="round"/><path d="M532 379l54 54" stroke="#fff65c" stroke-width="39" stroke-linecap="round"/></g>`;
  }

  if (category === 'Sewing') {
    if (lower.includes('bow')) return `<g filter="url(#objectShadow)"><path d="M436 316c-72-103-176-118-226-20 54 83 151 76 226 20z" fill="#ff9cc7" stroke="${purple}" stroke-width="16"/><path d="M466 316c72-103 176-118 226-20-54 83-151 76-226 20z" fill="#ff4fa3" stroke="${purple}" stroke-width="16"/><rect x="404" y="272" width="94" height="96" rx="24" fill="#fff65c" stroke="${purple}" stroke-width="13"/><path d="M284 295c45 19 81 22 116 13M504 308c37 9 75 5 116-13" stroke="#fff" stroke-width="11" stroke-linecap="round"/></g>`;
    return `<g filter="url(#objectShadow)"><path d="M286 192h250c62 0 104 44 104 104v130H260V218c0-15 11-26 26-26z" fill="#ff9cc7" stroke="${purple}" stroke-width="16"/><circle cx="404" cy="300" r="62" fill="#fff" stroke="${purple}" stroke-width="13"/><path d="M487 190c42-83 137-39 92 48" fill="none" stroke="${purple}" stroke-width="17" stroke-linecap="round"/><path d="M222 460h458" stroke="${purple}" stroke-width="16" stroke-linecap="round"/><path d="M342 426v-84M306 426v-54M488 426v-70" stroke="#fff" stroke-width="13" stroke-linecap="round"/></g>`;
  }

  if (category === 'Drawing') {
    return `<g filter="url(#objectShadow)"><rect x="292" y="126" width="284" height="376" rx="34" fill="#fff" stroke="${purple}" stroke-width="16"/><path d="M346 394c52-134 151-47 172-190" fill="none" stroke="#35b7ff" stroke-width="18" stroke-linecap="round"/><path d="M528 92l96 96-178 178-105 29 29-105z" fill="#fff65c" stroke="${purple}" stroke-width="16"/><path d="M568 130l28 28" stroke="#ff4fa3" stroke-width="21" stroke-linecap="round"/><circle cx="382" cy="236" r="18" fill="#22d7a5"/><circle cx="492" cy="438" r="18" fill="#ff4fa3"/></g>`;
  }

  if (category === 'Wood') {
    if (lower.includes('boat')) return `<g filter="url(#objectShadow)"><path d="M242 398h416c-38 70-106 108-208 108s-170-38-208-108z" fill="#c98745" stroke="${purple}" stroke-width="16"/><path d="M452 164v234" stroke="${purple}" stroke-width="15" stroke-linecap="round"/><path d="M466 188c74 42 112 100 114 174H466z" fill="#fff65c" stroke="${purple}" stroke-width="13"/><path d="M438 208c-68 46-104 96-108 154h108z" fill="#dffbff" stroke="${purple}" stroke-width="13"/></g>`;
    return `<g filter="url(#objectShadow)"><path d="M272 428c56-150 230-160 310 0z" fill="#ffbd72" stroke="${purple}" stroke-width="16"/><path d="M296 428h254M332 360h176M378 292h88" stroke="#8a4d12" stroke-width="15" stroke-linecap="round"/><path d="M510 178l122 122" stroke="#8a4d12" stroke-width="35" stroke-linecap="round"/><path d="M474 144l82 82" stroke="#c79d77" stroke-width="48" stroke-linecap="round"/><circle cx="430" cy="395" r="32" fill="${stripe}" opacity=".76"/></g>`;
  }

  if (category === 'Jewelry') {
    return `<g filter="url(#objectShadow)"><path d="M252 188c54 244 342 244 396 0" fill="none" stroke="${purple}" stroke-width="16" stroke-linecap="round"/><circle cx="270" cy="224" r="40" fill="#85f2bf" stroke="${purple}" stroke-width="12"/><circle cx="340" cy="354" r="48" fill="#fff65c" stroke="${purple}" stroke-width="12"/><circle cx="450" cy="390" r="50" fill="#ff4fa3" stroke="${purple}" stroke-width="12"/><circle cx="560" cy="354" r="48" fill="#35b7ff" stroke="${purple}" stroke-width="12"/><circle cx="630" cy="224" r="40" fill="#b7abff" stroke="${purple}" stroke-width="12"/><path d="M450 428l42 66-42 66-42-66z" fill="${stripe}" stroke="${purple}" stroke-width="12"/></g>`;
  }

  if (category === 'Soap') {
    return `<g filter="url(#objectShadow)"><rect x="268" y="250" width="360" height="184" rx="86" fill="#86ecff" stroke="${purple}" stroke-width="16"/><path d="M340 334c76-62 150 42 222-24" fill="none" stroke="#fff" stroke-width="22" stroke-linecap="round"/><circle cx="306" cy="184" r="46" fill="#fff" opacity=".9"/><circle cx="520" cy="158" r="34" fill="#fff" opacity=".86"/><circle cx="608" cy="220" r="24" fill="#fff" opacity=".82"/><rect x="356" y="430" width="190" height="54" rx="27" fill="#fff65c" stroke="${purple}" stroke-width="11"/></g>`;
  }

  if (category === 'Candles') {
    return `<g filter="url(#objectShadow)"><rect x="342" y="214" width="218" height="282" rx="54" fill="#fff" stroke="${purple}" stroke-width="16"/><path d="M452 190c-50-54 12-102 0-152 70 62 79 114 0 152z" fill="#ffd21f" stroke="#ff4fa3" stroke-width="13"/><path d="M384 314h134M394 388h114" stroke="#ffbd5a" stroke-width="22" stroke-linecap="round"/><path d="M342 270h218" stroke="${stripe}" stroke-width="28" opacity=".7"/></g>`;
  }

  return `<g filter="url(#objectShadow)"><rect x="302" y="130" width="288" height="376" rx="40" fill="#fff" stroke="${purple}" stroke-width="16"/><path d="M350 264c43-48 99 15 102 70 10-55 68-118 112-70 56 62-112 166-112 166S294 326 350 264z" fill="#ff4fa3"/><path d="M332 170l-82 66M592 492l70 56" stroke="#fff65c" stroke-width="22" stroke-linecap="round"/><path d="M362 204h164" stroke="#b7abff" stroke-width="14" stroke-linecap="round"/></g>`;
}

function previewSvg(item) {
  const meta = categoryMeta[item.category];
  const seed = seedFor(item.title);
  const safeTitle = escapeXml(item.title);
  const title = titleLine(item.title);
  const object = objectSvg(item.title, item.category, seed);
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 680" role="img" aria-labelledby="title desc">
<title id="title">Finished ${safeTitle} project preview</title>
<desc id="desc">A large clear Crafties finished-project preview illustration for the ${escapeXml(item.category)} pattern ${safeTitle}, styled as a photographed craft on a tabletop card with texture, shadows, and highlights.</desc>
<defs>
  <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#fffdf8"/><stop offset=".42" stop-color="${meta.color}"/><stop offset="1" stop-color="#efe0ff"/></linearGradient>
  <linearGradient id="table" x1="0" x2="0" y1="0" y2="1"><stop stop-color="#fff8df"/><stop offset="1" stop-color="#f0d7ff"/></linearGradient>
  <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".72" numOctaves="3" seed="${(seed % 89) + 11}"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="table" tableValues="0 .07"/></feComponentTransfer></filter>
  <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="24" stdDeviation="20" flood-color="#53138f" flood-opacity=".18"/></filter>
  <filter id="objectShadow" x="-25%" y="-25%" width="150%" height="150%"><feDropShadow dx="0" dy="24" stdDeviation="18" flood-color="#321441" flood-opacity=".28"/></filter>
</defs>
<rect width="900" height="680" rx="72" fill="url(#table)"/>
<rect width="900" height="680" rx="72" fill="url(#bg)" opacity=".74"/>
<rect width="900" height="680" rx="72" filter="url(#grain)" opacity=".9"/>
<ellipse cx="454" cy="580" rx="330" ry="48" fill="#53138f" opacity=".14"/>
<rect x="84" y="58" width="732" height="550" rx="64" fill="#fffdf8" stroke="#ffffff" stroke-width="16" filter="url(#cardShadow)"/>
<path d="M142 124h604" stroke="#f1d6ff" stroke-width="9" stroke-linecap="round" opacity=".9"/>
<path d="M154 536h592" stroke="#fff65c" stroke-width="20" stroke-linecap="round" opacity=".64"/>
<circle cx="132" cy="122" r="34" fill="#fff65c" opacity=".96"/>
<circle cx="768" cy="142" r="25" fill="#22d7a5" opacity=".52"/>
<circle cx="738" cy="504" r="34" fill="#ff4fa3" opacity=".2"/>
${object}
<rect x="116" y="35" width="332" height="62" rx="31" fill="#53138f" opacity=".96"/>
<text x="282" y="75" text-anchor="middle" font-family="Verdana,Arial,sans-serif" font-size="22" font-weight="900" fill="#fff">${meta.emoji} Finished project</text>
<rect x="540" y="35" width="252" height="62" rx="31" fill="#fff65c" stroke="#53138f" stroke-width="5"/>
<text x="666" y="74" text-anchor="middle" font-family="Verdana,Arial,sans-serif" font-size="20" font-weight="900" fill="#53138f">Crafties preview</text>
<rect x="270" y="598" width="360" height="46" rx="23" fill="#ffffff" opacity=".92"/>
<text x="450" y="628" text-anchor="middle" font-family="Verdana,Arial,sans-serif" font-size="22" font-weight="900" fill="#321441">${title}</text>
</svg>
`;
}

function loadItems() {
  const manifest = JSON.parse(fs.readFileSync(PATTERN_MANIFEST, 'utf8'));
  const items = Object.entries(manifest.categories).flatMap(([category, titles]) =>
    titles.map(title => {
      const assetSlug = findExistingAssetSlug(title);
      return {
        title,
        category,
        assetSlug,
        pageSlug: findPatternPageSlug(assetSlug),
        file: `assets/product-photos/${assetSlug}.svg`
      };
    })
  );
  return { items, expectedTotal: manifest.total };
}

function writeAssets(items) {
  for (const item of items) {
    fs.writeFileSync(path.join(PHOTO_DIR, `${item.assetSlug}.svg`), previewSvg(item));
  }
  const grouped = {};
  for (const item of items) {
    grouped[item.category] ||= [];
    grouped[item.category].push({
      title: item.title,
      slug: item.assetSlug,
      patternPage: `patterns/${item.pageSlug}.html`,
      file: item.file,
      type: 'local-finished-project-preview-svg',
      version: VERSION
    });
  }
  fs.writeFileSync(PHOTO_MANIFEST, `${JSON.stringify({
    total: items.length,
    version: VERSION,
    generatedAt: '2026-05-03',
    generator: 'scripts/generate-finished-previews.cjs',
    note: 'Local SVG finished-project previews. No external APIs or credentials used.',
    categories: grouped
  }, null, 2)}\n`);
}

function updatePatternPages(items) {
  for (const item of items) {
    const file = path.join(ROOT, 'patterns', `${item.pageSlug}.html`);
    let html = fs.readFileSync(file, 'utf8');
    const rel = `../${item.file}?v=${VERSION}`;
    html = html.replace(/src="\.\.\/assets\/product-photos\/[^"]+\.svg\?v=[^"]+"/g, `src="${rel}"`);
    html = html.replace(/alt="[^"]*project preview"/g, `alt="Large finished ${escapeXml(item.title)} project preview"`);
    html = html.replace(/UPDATED v20[0-9-]+(?:-\d+)?/g, `UPDATED v${VERSION}`);
    fs.writeFileSync(file, html);
  }
}

function cardMarkup(item) {
  const src = `${item.file}?v=${VERSION}`;
  const alt = `Large finished ${escapeXml(item.title)} project preview`;
  return `<img class="product-img" loading="lazy" decoding="async" src="${src}" alt="${alt}"><span class="product-caption">finished project preview</span>`;
}

function updateIndex(items) {
  let html = fs.readFileSync(INDEX, 'utf8');
  const byPageSlug = new Map(items.map(item => [item.pageSlug, item]));
  const byAssetSlug = new Map(items.map(item => [item.assetSlug, item]));
  html = html.replace(/<article class="([^"]*\bpattern-card\b[^"]*)"([^>]*data-pattern="([^"]+)"[^>]*)>([\s\S]*?)<\/article>/g,
    (full, className, attrs, dataPattern, body) => {
      const item = byPageSlug.get(dataPattern) || byAssetSlug.get(dataPattern);
      if (!item) return full;
      const classes = new Set(className.split(/\s+/).filter(Boolean));
      classes.add('has-product-image');
      if (classes.has('updated-product-card')) classes.delete('updated-product-card');
      body = body
        .replace(/<img class="product-img"[^>]*>/g, '')
        .replace(/<span class="product-caption"[\s\S]*?<\/span>/g, '')
        .replace(/<span class="product-version"[\s\S]*?<\/span>/g, '');
      return `<article class="${Array.from(classes).join(' ')}"${attrs}>${cardMarkup(item)}${body}</article>`;
    });
  html = html.replace(/assets\/product-photos\/([a-z0-9-]+)\.svg\?v=[^"]+/g, `assets/product-photos/$1.svg?v=${VERSION}`);
  fs.writeFileSync(INDEX, html);
}

const { items, expectedTotal } = loadItems();
if (items.length !== expectedTotal) {
  throw new Error(`Expected ${expectedTotal} pattern items, found ${items.length}`);
}
writeAssets(items);
updatePatternPages(items);
updateIndex(items);
console.log(`Generated ${items.length} finished preview SVGs and updated references to ${VERSION}.`);
