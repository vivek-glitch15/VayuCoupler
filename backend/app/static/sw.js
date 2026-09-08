const CACHE_NAME = 'vayucoupler-v27';
const ASSETS = [
  '/',
  '/?source=pwa',
  '/static/manifest.json?v=27',
  '/static/css/styles.css?v=27',
  '/static/css/mobile.css?v=27',
  '/static/icon-192.png?v=27',
  '/static/icon-512.png?v=27',
  '/static/icon-maskable-512.png?v=27',
  '/static/apple-touch-icon.png?v=27'
];

self.addEventListener('install', (e) => {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('Purging old cache:', key);
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Network-First for Navigation (HTML), Cache-First for static assets
self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;

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
        .catch(() => caches.match(e.request).then((res) => res || caches.match('/')))
    );
    return;
  }

  // Assets: Stale-While-Revalidate
  e.respondWith(
    caches.match(e.request).then((cachedResponse) => {
      const fetchPromise = fetch(e.request).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const responseClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(e.request, responseClone));
        }
        return networkResponse;
      }).catch(() => cachedResponse);

      return cachedResponse || fetchPromise;
    })
  );
});
