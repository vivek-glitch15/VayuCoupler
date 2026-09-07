const CACHE_NAME = 'vayucoupler-v7';
const ASSETS = [
  '/',
  '/?source=pwa',
  '/static/index.html',
  '/static/manifest.json?v=7',
  '/static/css/styles.css?v=7',
  '/static/css/mobile.css?v=7',
  '/static/icon-192.png?v=7',
  '/static/icon-512.png?v=7',
  '/static/icon-maskable-512.png?v=7',
  '/static/apple-touch-icon.png?v=7'
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

self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request))
  );
});
