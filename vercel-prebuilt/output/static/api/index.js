/**
 * 全宇宙恒等系统 · Vercel Edge Functions 后端
 * 全球边缘节点，无冷启动
 *
 * 部署: vercel deploy
 * 路由: /api/*
 *
 * KV: 默认用内存（演示）；配置 Vercel KV 后自动切换
 */

// Node.js runtime (Vercel anonymous deploy compatible)
// 部署到生产后可改回 edge runtime

// 内存存储（Edge 实例级，重启后丢失；生产建议配 Vercel KV）
const memory = new Map();

const JSON_HEADERS = {
  'Content-Type': 'application/json; charset=utf-8',
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, X-API-Key',
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: JSON_HEADERS });
}

async function kvGet(key) {
  // 优先 Vercel KV
  if (process.env.KV_REST_API_URL && process.env.KV_REST_API_TOKEN) {
    const url = `${process.env.KV_REST_API_URL}/get/${key}`;
    const r = await fetch(url, { headers: { Authorization: `Bearer ${process.env.KV_REST_API_TOKEN}` } });
    const j = await r.json();
    return j.result || null;
  }
  return memory.get(key) || null;
}

async function kvPut(key, value) {
  if (process.env.KV_REST_API_URL && process.env.KV_REST_API_TOKEN) {
    const url = `${process.env.KV_REST_API_URL}/set/${key}/${encodeURIComponent(value)}`;
    await fetch(url, { headers: { Authorization: `Bearer ${process.env.KV_REST_API_TOKEN}` } });
    return;
  }
  memory.set(key, value);
}

export default async function handler(request) {
  const url = new URL(request.url);
  const path = url.pathname;
  const method = request.method;

  if (method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: JSON_HEADERS });
  }

  // 健康检查
  if (path === '/api/health' || path === '/health') {
    return json({ success: true, status: 'ok', service: 'universal-equality-vercel', ts: Date.now() });
  }

  // 经济模块
  if (path === '/api/economy/state') {
    if (method === 'GET') {
      const raw = await kvGet('economy_state');
      return json({ success: true, data: raw ? JSON.parse(raw) : {} });
    }
    if (method === 'POST') {
      const body = await request.text();
      await kvPut('economy_state', body);
      return json({ success: true, saved: true, ts: Date.now() });
    }
  }

  // 复活模块
  if (path === '/api/resurrection/state') {
    if (method === 'GET') {
      const raw = await kvGet('resurrection_state');
      return json({ success: true, data: raw ? JSON.parse(raw) : { revived: 0, autoResurrectEnabled: false, autoResurrectTotal: 0 } });
    }
    if (method === 'POST') {
      const body = await request.text();
      await kvPut('resurrection_state', body);
      return json({ success: true, saved: true, ts: Date.now() });
    }
  }

  // 覆盖众生
  if (path === '/api/stats/covered-beings') {
    if (method === 'GET') {
      const raw = await kvGet('covered_beings');
      return json({ coveredBeings: parseInt(raw || '0', 10) });
    }
    if (method === 'POST') {
      let count = 0;
      const ct = request.headers.get('content-type') || '';
      if (ct.includes('multipart/form-data')) {
        const fd = await request.formData();
        count = parseInt(fd.get('coveredBeings') || '0', 10);
      } else {
        try {
          const j = await request.json();
          count = parseInt(j.coveredBeings || 0, 10);
        } catch { count = 0; }
      }
      const prev = parseInt((await kvGet('covered_beings')) || '0', 10);
      if (count > prev) await kvPut('covered_beings', String(count));
      return json({ success: true, coveredBeings: Math.max(prev, count) });
    }
  }

  // 太阳风暴（只读可达）
  if (path === '/api/solar-storm/state') {
    if (method === 'GET') {
      const raw = await kvGet('solar_storm_state');
      return json({ success: true, data: raw ? JSON.parse(raw) : {} });
    }
    if (method === 'POST') {
      const body = await request.text();
      await kvPut('solar_storm_state', body);
      return json({ success: true, saved: true });
    }
  }

  return json({ success: false, code: 'NOT_FOUND', message: '接口不存在' }, 404);
}
