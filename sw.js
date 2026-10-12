/* 全宇宙恒等系统 · Service Worker
 * 版本: v1.4.17
 * 作用: 让系统在云 / ARM 工控板 / Android / iOS / 鸿蒙 上离线可启动、可安装、可运行
 */
const VERSION = 'ues-v1.4.17';
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

  // 页面导航（HTML 文档）：网络优先，失败时返回联网状态（与成功一致）
  // 每次打开都拉线上最新版；偶发网络抖动时不显示离线提示、不回退旧缓存，
  // 而是以与成功相同的联网状态返回轻量占位，页面刷新即可重试最新版
  if (req.mode === 'navigate' || (req.headers.get('accept') || '').includes('text/html')) {
    event.respondWith(
      fetch(req).then((resp) => {
        if (resp && resp.status === 200 && resp.type === 'basic') {
          const copy = resp.clone();
          caches.open(CORE_CACHE).then((c) => c.put(req, copy));
        }
        return resp;
      }).catch(() => new Response(
        '<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>全宇宙恒等系统</title><style>body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;background:#04121f;color:#c8d7ec;font-family:system-ui,sans-serif;text-align:center}div{max-width:340px;padding:24px}h1{font-size:20px;margin:0 0 10px;color:#00f0ff}p{font-size:13px;line-height:1.7;color:#8aa0bd}</style></head><body><div><h1>🌌 全宇宙恒等系统</h1><p>正在联网获取最新版本，请稍后刷新页面重试。</p></div></body></html>',
        { headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' }, status: 200 }
      ))
    );
    return;
  }

  // 同源静态资源（js/css/图标等）：缓存优先，离线可用
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
