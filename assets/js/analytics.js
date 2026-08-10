(function () {
  const ENDPOINT = '/.netlify/functions/pageview';
  const SESSION_KEY = 'teamcrafties_analytics_seen';

  function normalizePath(pathname) {
    if (!pathname || pathname === '/') return '__home';
    return pathname.replace(/^\/+|\/+$/g, '').replace(/[^a-zA-Z0-9/_-]+/g, '-').replace(/\//g, '__') || '__home';
  }

  function rememberPage(pathKey) {
    try {
      const raw = sessionStorage.getItem(SESSION_KEY);
      const seen = raw ? JSON.parse(raw) : {};
      if (seen[pathKey]) return false;
      seen[pathKey] = Date.now();
      sessionStorage.setItem(SESSION_KEY, JSON.stringify(seen));
      return true;
    } catch (_) {
      return true;
    }
  }

  function jsonFetch(url, options) {
    return fetch(url, Object.assign({
      cache: 'no-store',
      headers: { 'Content-Type': 'application/json' },
    }, options || {})).then(function (response) {
      if (!response.ok) throw new Error('Analytics request failed');
      return response.json();
    });
  }

  const pathKey = normalizePath(window.location.pathname);
  const shouldCount = rememberPage(pathKey);

  window.teamCraftiesAnalytics = {
    currentPageKey: pathKey,
    shouldCount: shouldCount,
    getCount: function (key) {
      return jsonFetch(ENDPOINT + '?path=' + encodeURIComponent(key), { method: 'GET' });
    },
    getSummary: function () {
      return jsonFetch(ENDPOINT, { method: 'GET' });
    }
  };

  if (!shouldCount) return;

  jsonFetch(ENDPOINT, {
    method: 'POST',
    body: JSON.stringify({
      path: pathKey,
      referrer: document.referrer || ''
    })
  }).catch(function () {
    /* fail quietly so the site still feels lovely */
  });
})();
