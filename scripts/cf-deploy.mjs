#!/usr/bin/env node
// cf-deploy.mjs — Team Crafties Cloudflare Pages deploy helper.
//
// Modes:
//   ship      Deploy current working tree to CF Pages (production).
//   dry-run   Print the deploy plan without shipping anything.
//
// Usage:
//   npm run deploy              # ships (refuses if working tree is dirty)
//   npm run deploy:dry-run      # prints plan only
//   ALLOW_DIRTY=1 npm run deploy
//
// Requires:
//   - wrangler v4+ installed globally (npm i -g wrangler)
//   - wrangler login completed once (credentials in
//     ~/Library/Preferences/.wrangler/config/default.toml on macOS,
//     or the platform equivalent shown by `wrangler whoami`)
//   - git on PATH (for status + rev-parse)
//
// Account / project identifiers come from the verified 2026-08-09 setup:
//   account  = 65c1325111d76a6b9266856c84ce7d7a (postenathalie@gmail.com)
//   project  = team-crafties
//   branch   = main
//   pages subdomain = team-crafties-czq.pages.dev
//   custom domain   = teamcrafties.com

import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';

const PROJECT = 'team-crafties';
const BRANCH = 'main';
const ACCOUNT_ID = '65c1325111d76a6b9266856c84ce7d7a';
const DASHBOARD_URL =
  `https://dash.cloudflare.com/${ACCOUNT_ID}/pages/view/${PROJECT}`;

const mode = process.argv[2];
if (mode !== 'ship' && mode !== 'dry-run') {
  console.error('Usage: cf-deploy.mjs <ship|dry-run>');
  process.exit(2);
}

function run(cmd, args, opts = {}) {
  const r = spawnSync(cmd, args, { stdio: ['inherit', 'pipe', 'pipe'], encoding: 'utf8', ...opts });
  return {
    code: r.status ?? 0,
    stdout: (r.stdout || '').trim(),
    stderr: (r.stderr || '').trim(),
  };
}

function which(name) {
  const r = run('which', [name]);
  return r.code === 0 ? r.stdout : null;
}

// 1. Sanity checks.
const wranglerPath = which('wrangler');
if (!wranglerPath) {
  console.error('✘ wrangler not found on PATH. Install it once:');
  console.error('    npm install -g wrangler');
  console.error('    wrangler login');
  process.exit(1);
}
const gitPath = which('git');
if (!gitPath) {
  console.error('✘ git not found on PATH. cf-deploy.mjs needs git to capture commit SHA + status.');
  process.exit(1);
}

// 2. Confirm auth.
const whoami = run(wranglerPath, ['whoami']);
if (whoami.code !== 0) {
  console.error('✘ wrangler is not authenticated. Run:');
  console.error(`    ${wranglerPath} login`);
  process.exit(1);
}
if (!whoami.stdout.includes('postenathalie@gmail.com')) {
  console.warn('⚠ wrangler is logged in, but the account is NOT postenathalie@gmail.com.');
  console.warn('  Found:');
  for (const line of whoami.stdout.split('\n')) {
    if (line.trim()) console.warn('    ' + line.trim());
  }
  console.warn('  Deploying to the wrong CF account will still succeed but publish to the wrong project.');
  console.warn('  Press Ctrl-C within 5 seconds to abort.');
  for (let i = 5; i > 0; i--) {
    process.stdout.write(`  ${i}…\r`);
    run('sleep', ['1']);
  }
  process.stdout.write('        \r');
}

// 3. Capture git state.
const inGitRepo = existsSync('.git');
const sha = inGitRepo ? run(gitPath, ['rev-parse', 'HEAD']).stdout : '<no git repo>';
const shortSha = sha.slice(0, 7);
const status = inGitRepo ? run(gitPath, ['status', '--porcelain']).stdout : '';
const dirty = status.length > 0;
const changedFiles = dirty ? status.split('\n').filter(Boolean).length : 0;

// 4. Print plan.
console.log('─'.repeat(60));
console.log(`Target project : ${PROJECT}`);
console.log(`Branch         : ${BRANCH}`);
console.log(`Commit SHA     : ${sha}${dirty ? '  (dirty working tree!)' : ''}`);
console.log(`Changed files  : ${dirty ? changedFiles : 0}`);
console.log(`Publish dir    : . (project root)`);
console.log(`Dashboard      : ${DASHBOARD_URL}`);
console.log('─'.repeat(60));

if (mode === 'dry-run') {
  console.log('dry-run: no deploy sent.');
  if (dirty) {
    console.log('Uncommitted changes that would be shipped as a "dirty" deploy:');
    for (const line of status.split('\n').filter(Boolean)) console.log('  ' + line);
  }
  process.exit(0);
}

// 5. Refuse if dirty unless ALLOW_DIRTY=1.
if (dirty && process.env.ALLOW_DIRTY !== '1') {
  console.error('✘ Working tree is dirty (' + changedFiles + ' files). Commit first, or pass ALLOW_DIRTY=1 to ship anyway.');
  console.error('  First 20 changed paths:');
  for (const line of status.split('\n').filter(Boolean).slice(0, 20)) {
    console.error('    ' + line);
  }
  if (changedFiles > 20) console.error(`    …and ${changedFiles - 20} more.`);
  process.exit(1);
}

// 6. Ship.
const args = [
  'pages', 'deploy', '.',
  '--project-name', PROJECT,
  '--branch', BRANCH,
  '--commit-hash', sha,
];
console.log(`▸ ${wranglerPath} ${args.join(' ')}\n`);
const r = spawnSync(wranglerPath, args, { stdio: 'inherit' });
process.exit(r.status ?? 1);
