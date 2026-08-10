const { connectLambda, getStore } = require('@netlify/blobs');

const STORE_NAME = 'team-crafties-analytics';
const SNAPSHOT_KEY = 'snapshot';
const SITE_HOST = 'teamcrafties.com';

function normalizePath(input) {
  if (!input || input === '/') return '__home';
  return String(input)
    .replace(/^\/+|\/+$/g, '')
    .replace(/[^a-zA-Z0-9/_-]+/g, '-')
    .replace(/\//g, '__') || '__home';
}

function normalizeSource(referrer) {
  if (!referrer) return null;

  try {
    const host = new URL(referrer).hostname.replace(/^www\./, '');
    if (!host || host === SITE_HOST) return 'direct_or_internal';
    return host;
  } catch (_) {
    return 'direct_or_internal';
  }
}

function baseSnapshot() {
  return {
    total: 0,
    pages: {},
    sources: {},
    updated_at: null,
  };
}

function response(statusCode, body) {
  return {
    statusCode,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    },
    body: JSON.stringify(body),
  };
}

exports.handler = async (event) => {
  connectLambda(event);
  const store = getStore(STORE_NAME);

  if (event.httpMethod === 'OPTIONS') {
    return response(204, { ok: true });
  }

  const snapshot = (await store.get(SNAPSHOT_KEY, { type: 'json' })) || baseSnapshot();

  if (event.httpMethod === 'GET') {
    const path = normalizePath(event.queryStringParameters && event.queryStringParameters.path);

    if (event.queryStringParameters && event.queryStringParameters.path) {
      return response(200, {
        path,
        value: snapshot.pages[path] || 0,
        total: snapshot.total || 0,
        updated_at: snapshot.updated_at,
      });
    }

    return response(200, snapshot);
  }

  if (event.httpMethod !== 'POST') {
    return response(405, { error: 'Method not allowed' });
  }

  let body = {};
  try {
    body = event.body ? JSON.parse(event.body) : {};
  } catch (_) {
    return response(400, { error: 'Invalid JSON body' });
  }

  const path = normalizePath(body.path);
  const source = normalizeSource(body.referrer);

  snapshot.total = Number(snapshot.total || 0) + 1;
  snapshot.pages[path] = Number(snapshot.pages[path] || 0) + 1;

  if (source) {
    snapshot.sources[source] = Number(snapshot.sources[source] || 0) + 1;
  }

  snapshot.updated_at = new Date().toISOString();

  await store.setJSON(SNAPSHOT_KEY, snapshot);

  return response(200, {
    ok: true,
    path,
    total: snapshot.total,
    page: snapshot.pages[path],
    source,
    updated_at: snapshot.updated_at,
  });
};
