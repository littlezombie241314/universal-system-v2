/* 全宇宙恒等系统 · Service Worker
 * 版本: v1.3.6
 * 作用: 让系统在云 / ARM 工控板 / Android / iOS / 鸿蒙 上离线可启动、可安装、可运行
 */
const VERSION = 'ues-v1.3.6';
const CORE_CACHE = `${VERSION}-core`;

const CORE_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './favicon.ico',
  './favicon-16.png',
  './favicon-32.png',
  './assets/qrcode.min.js',
  './assets/JsBarcode.all.min.js',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-maskable-512.png',
  './icons/apple-touch-icon.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CORE_CACHE).then((cache) => cache.addAll(CORE_ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CORE_CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);

  // 跨域动态 API（后端经济/太阳风暴/天气/空气质量/支付）：网络优先，不写缓存
  // 这样服务器升级或实时数据变化时，前端立即拿到最新
  if (url.origin !== location.origin) {
    event.respondWith(
      fetch(req).catch(() => caches.match(req))
    );
    return;
  }

  // 同源静态资源：缓存优先
  event.respondWith(
    caches.match(req).then((cached) => {
      if (cached) return cached;
      return fetch(req).then((resp) => {
        if (resp && resp.status === 200 && resp.type === 'basic') {
          const copy = resp.clone();
          caches.open(CORE_CACHE).then((c) => c.put(req, copy));
        }
        return resp;
      });
    })
  );
});
