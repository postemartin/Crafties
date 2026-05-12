#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const PATTERN_DIR = path.join(ROOT, 'patterns');
const PHOTO_DIR = path.join(ROOT, 'assets', 'product-photos');
const INDEX = path.join(ROOT, 'index.html');
const PHOTO_MANIFEST = path.join(PHOTO_DIR, 'manifest.json');
const PATTERN_MANIFEST = path.join(PATTERN_DIR, 'pattern-manifest.json');

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exitCode = 1;
}

function ok(message) {
  console.log(`OK: ${message}`);
}

function stripQuery(src) {
  return src.split('?')[0];
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

const manifest = JSON.parse(fs.readFileSync(PHOTO_MANIFEST, 'utf8'));
const patternManifest = JSON.parse(fs.readFileSync(PATTERN_MANIFEST, 'utf8'));
const expectedTotal = patternManifest.total;
const items = Object.values(manifest.categories).flat();
const patternPages = fs.readdirSync(PATTERN_DIR).filter(file => file.endsWith('.html'));
const imageAssets = fs.readdirSync(PHOTO_DIR).filter(file => /\.(jpg|jpeg|png|webp|svg)$/i.test(file));
const manifestImageCount = items.filter(item => /\.(jpg|jpeg|png|webp|svg)$/i.test(item.file)).length;

if (patternPages.length === expectedTotal) ok(`${expectedTotal} pattern HTML pages found`);
else fail(`expected ${expectedTotal} pattern HTML pages, found ${patternPages.length}`);

if (manifest.total === expectedTotal) ok(`photo manifest total matches expected count (${expectedTotal})`);
else fail(`expected photo manifest total ${expectedTotal}, found ${manifest.total}`);

if (manifestImageCount === expectedTotal) ok(`manifest lists ${expectedTotal} product preview image assets`);
else fail(`expected manifest to list ${expectedTotal} preview images, found ${manifestImageCount}`);

if (items.length === expectedTotal) ok(`manifest lists ${expectedTotal} generated previews`);
else fail(`expected manifest to list ${expectedTotal} previews, found ${items.length}`);

const missingFiles = [];
const badPageRefs = [];
for (const item of items) {
  const assetPath = path.join(ROOT, item.file);
  const pagePath = path.join(ROOT, item.patternPage);
  if (!fs.existsSync(assetPath)) missingFiles.push(item.file);
  if (!fs.existsSync(pagePath)) {
    missingFiles.push(item.patternPage);
    continue;
  }
  const page = fs.readFileSync(pagePath, 'utf8');
  const expectedWithoutQuery = `../${item.file}`;
  const expectedWithQuery = `../${item.file}?v=${manifest.version}`;
  const alternateFile = item.file.replace('/macrame-', '/macram-');
  const alternateWithoutQuery = `../${alternateFile}`;
  const alternateWithQuery = `../${alternateFile}?v=${manifest.version}`;
  const pageHasImage = page.includes(expectedWithoutQuery) || page.includes(expectedWithQuery) || page.includes(alternateWithoutQuery) || page.includes(alternateWithQuery);
  if (!pageHasImage) badPageRefs.push(`${item.patternPage} -> ${expectedWithoutQuery}`);
}

if (missingFiles.length === 0) ok('all manifest files exist');
else fail(`missing files:\n${missingFiles.join('\n')}`);

if (badPageRefs.length === 0) ok('every pattern page references its matching image');
else fail(`pattern pages with missing matching image reference:\n${badPageRefs.join('\n')}`);

const index = fs.readFileSync(INDEX, 'utf8');
const cardMatches = [...index.matchAll(/<article class="[^"]*\bpattern-card\b[^"]*"[^>]*data-pattern="([^"]+)"[^>]*>([\s\S]*?)<\/article>/g)];
if (cardMatches.length === expectedTotal) ok(`homepage contains ${expectedTotal} pattern cards`);
else fail(`expected ${expectedTotal} homepage pattern cards, found ${cardMatches.length}`);

const byPageSlug = new Map(items.map(item => [path.basename(item.patternPage, '.html'), item]));
const byAssetSlug = new Map(items.map(item => [path.basename(item.file, path.extname(item.file)), item]));
const missingCardImages = [];
const unresolvedCardImages = [];
for (const [, dataPattern, body] of cardMatches) {
  const item = byPageSlug.get(dataPattern) || byAssetSlug.get(dataPattern) || byAssetSlug.get(dataPattern.replace(/^macram-/, 'macrame-'));
  if (!item) {
    missingCardImages.push(`${dataPattern}: no manifest entry`);
    continue;
  }
  const img = body.match(/<img class="product-img"[^>]*src="([^"]+)"/);
  if (!img) {
    missingCardImages.push(`${dataPattern}: no product image`);
    continue;
  }
  const src = stripQuery(img[1]);
  if (src !== item.file) missingCardImages.push(`${dataPattern}: expected ${item.file}, found ${img[1]}`);
  if (!fs.existsSync(path.join(ROOT, src))) unresolvedCardImages.push(`${dataPattern}: ${src}`);
}

if (missingCardImages.length === 0) ok('homepage cards reference the matching product photos');
else fail(`homepage cards with bad image references:\n${missingCardImages.join('\n')}`);

if (unresolvedCardImages.length === 0) ok('homepage card image files all resolve');
else fail(`homepage cards with missing files:\n${unresolvedCardImages.join('\n')}`);

const staleVersionRefs = [];
const expectedVersionPattern = new RegExp(`product-photos/[^"'\\s]+\\.(?:jpg|jpeg|png|webp|svg)\\?v=(?!${escapeRegExp(manifest.version)})([^"'\\s]+)`, 'gi');
for (const file of [INDEX, ...patternPages.map(file => path.join(PATTERN_DIR, file))]) {
  const html = fs.readFileSync(file, 'utf8');
  const stale = [...html.matchAll(expectedVersionPattern)].map(match => match[1]);
  if (stale.length) staleVersionRefs.push(`${path.relative(ROOT, file)}: ${[...new Set(stale)].join(', ')}`);
}

if (staleVersionRefs.length === 0) ok(`no stale preview cache-busting versions found; current version is ${manifest.version}`);
else fail(`stale preview versions found:\n${staleVersionRefs.join('\n')}`);

if (!process.exitCode) {
  console.log(`Verification complete: ${imageAssets.length} image files present, ${expectedTotal} manifest-backed previews consistent.`);
}
