const CACHE_NAME = 'vayucoupler-v36';
const ASSETS = [
  '/',
  '/?source=pwa',
  '/static/manifest.json?v=36',
  '/static/css/styles.css?v=36',
  '/static/css/mobile.css?v=36',
  '/static/icon-192.png?v=36',
  '/static/icon-512.png?v=36',
  '/static/icon-maskable-512.png?v=36',
  '/static/apple-touch-icon.png?v=36',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
  'https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.2/dist/confetti.browser.min.js',
  'https://cdn.tailwindcss.com',
  'https://unpkg.com/lucide@latest'
];

// Install: Cache critical assets, tolerating individual fetch failures for external CDNs
self.addEventListener('install', (e) => {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE_NAME).then(async (cache) => {
      for (const url of ASSETS) {
        try {
          const res = await fetch(url, { mode: 'cors' }).catch(() => fetch(url, { mode: 'no-cors' }));
          if (res && (res.status === 200 || res.type === 'opaque')) {
            await cache.put(url, res);
          }
        } catch (err) {
          console.warn('[VayuSW] Non-blocking cache skip for:', url, err);
        }
      }
    })
  );
});

// Activate: Purge old cache versions
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[VayuSW] Purging old cache:', key);
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Fetch Strategy:
// 1. Navigation (HTML): Network-first with instant offline cache fallback
// 2. Static assets & CDNs: Stale-While-Revalidate with offline cache-first
self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;

  const url = new URL(e.request.url);
  const isHtmlNavigation = e.request.mode === 'navigate' || 
                           (e.request.headers.get('accept') && e.request.headers.get('accept').includes('text/html'));

  if (isHtmlNavigation) {
    e.respondWith(
      fetch(e.request)
        .then((response) => {
          if (response && response.status === 200) {
            const responseClone = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(e.request, responseClone));
          }
          return response;
        })
        .catch(async () => {
          const cachedPage = await caches.match(e.request);
          if (cachedPage) return cachedPage;
          const rootFallback = await caches.match('/');
          if (rootFallback) return rootFallback;
          return new Response('Offline - VayuCoupler is running without network', {
            headers: { 'Content-Type': 'text/plain' }
          });
        })
    );
    return;
  }

  // Cross-origin CDN scripts, styles, fonts & local static assets
  e.respondWith(
    caches.match(e.request).then((cachedResponse) => {
      const fetchPromise = fetch(e.request)
        .then((networkResponse) => {
          if (networkResponse && (networkResponse.status === 200 || networkResponse.type === 'opaque')) {
            const responseClone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(e.request, responseClone));
          }
          return networkResponse;
        })
        .catch(() => cachedResponse);

      // Return cached response immediately if available, otherwise wait for network
      return cachedResponse || fetchPromise;
    })
  );
});
