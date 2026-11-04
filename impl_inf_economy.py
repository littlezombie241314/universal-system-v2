# -*- coding: utf-8 -*-
"""v1.6.61 实现无限经济·全面无限化：总览面板+余额∞+消费免费+投资∞+恒等分配"""
import io, re

P = '/home/user/Doubao/chats/38443814267131906/deploy/index.html'
s = io.open(P, encoding='utf-8').read()
orig = s
n = 0
def rep(old, new, cnt=1, tag=''):
    global s, n
    assert old in s, 'NOT FOUND: ' + tag
    s = s.replace(old, new, cnt)
    n += 1
    print('OK  #%d  %s' % (n, tag))

# ============ 1. 新增「无限经济 · 全宇宙经济恒等」总览面板 ============
overview_html = '''
<!-- ♾️ 无限经济 · 全宇宙经济恒等 -->
<div class="panel wide" style="background:linear-gradient(135deg,rgba(82,196,26,0.15),rgba(0,212,255,0.08));border:1px solid rgba(82,196,26,0.5)">
  <div class="panel-hdr"><div class="panel-title"><span class="ico">♾️</span>无限经济 · 全宇宙经济恒等</div><div class="panel-badge" style="background:rgba(82,196,26,0.2);color:#52C41A">全宇宙生效 · 恒等 ∞</div></div>
  <div style="padding:14px">
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-bottom:10px">
      <div style="text-align:center;background:rgba(0,0,0,0.25);border-radius:8px;padding:12px">
        <div style="font-size:22px">🌍</div>
        <div style="font-size:11px;font-weight:bold;color:#52C41A;margin:4px 0">全宇宙 GDP</div>
        <div id="infGdp" style="font-size:18px;font-weight:bold;color:#52C41A">¥∞</div>
      </div>
      <div style="text-align:center;background:rgba(0,0,0,0.25);border-radius:8px;padding:12px">
        <div style="font-size:22px">🏦</div>
        <div style="font-size:11px;font-weight:bold;color:#52C41A;margin:4px 0">全宇宙总资产</div>
        <div id="infAssets" style="font-size:18px;font-weight:bold;color:#52C41A">¥∞</div>
      </div>
      <div style="text-align:center;background:rgba(0,0,0,0.25);border-radius:8px;padding:12px">
        <div style="font-size:22px">👥</div>
        <div style="font-size:11px;font-weight:bold;color:#52C41A;margin:4px 0">人均财富 · 恒等</div>
        <div id="infPerCapita" style="font-size:18px;font-weight:bold;color:#52C41A">¥∞</div>
      </div>
      <div style="text-align:center;background:rgba(0,0,0,0.25);border-radius:8px;padding:12px">
        <div style="font-size:22px">📉</div>
        <div style="font-size:11px;font-weight:bold;color:#52C41A;margin:4px 0">通胀率</div>
        <div id="infInflation" style="font-size:18px;font-weight:bold;color:#52C41A">0%</div>
      </div>
      <div style="text-align:center;background:rgba(0,0,0,0.25);border-radius:8px;padding:12px">
        <div style="font-size:22px">🛍️</div>
        <div style="font-size:11px;font-weight:bold;color:#52C41A;margin:4px 0">消费</div>
        <div id="infSpend" style="font-size:18px;font-weight:bold;color:#52C41A">全免费</div>
      </div>
      <div style="text-align:center;background:rgba(0,0,0,0.25);border-radius:8px;padding:12px">
        <div style="font-size:22px">💼</div>
        <div style="font-size:11px;font-weight:bold;color:#52C41A;margin:4px 0">就业率</div>
        <div id="infEmployment" style="font-size:18px;font-weight:bold;color:#52C41A">100%</div>
      </div>
    </div>
    <div id="ecoInfLevels" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px"></div>
    <div style="font-size:10px;color:var(--text-dim);text-align:center;margin-top:8px">无限经济 · 所有存在财富恒等 ∞ · 消费免费 · 投资 ∞ · 债务 0 · <span id="infSaved" style="color:#52C41A">💾 实时保存</span></div>
  </div>
</div>

'''
rep('<div class="section" id="sec-economy"><div class="grid">',
    '<div class="section" id="sec-economy"><div class="grid">' + overview_html,
    tag='插入无限经济总览面板')

# ============ 2. 总览 JS（8层级实时 + 实时保存） ============
overview_js = '''
/* ===== 无限经济 · 全宇宙经济恒等 总览 ===== */
var ECO_INF_KEY = 'ues_economy_infinite';
var ECO_INF_LEVELS = [
  {id:'infLv-universe',icon:'🌌',name:'宇宙层级',base:120000000000000,rate:1999999},
  {id:'infLv-galaxy',  icon:'🌠',name:'星系层级',base:98000000000000, rate:1888888},
  {id:'infLv-planet',  icon:'🪐',name:'星球层级',base:76000000000000, rate:1777777},
  {id:'infLv-civ',     icon:'👽',name:'文明层级',base:54000000000000, rate:1666666},
  {id:'infLv-country', icon:'🏛️',name:'国家层级',base:32000000000000, rate:1555555},
  {id:'infLv-region',  icon:'🏙️',name:'地区层级',base:21000000000000, rate:1444444},
  {id:'infLv-person',  icon:'👤',name:'个人层级',base:9000000000000,  rate:1333333},
  {id:'infLv-other',   icon:'✨',name:'未分层级存在',base:4000000000000, rate:1222222}
];
(function(){
  var box = document.getElementById('ecoInfLevels');
  if (box) box.innerHTML = ECO_INF_LEVELS.map(function(lv){
    return '<div style="background:rgba(0,0,0,0.25);border:1px solid rgba(82,196,26,0.25);border-radius:8px;padding:10px;text-align:center">'
      + '<div style="font-size:20px">' + lv.icon + '</div>'
      + '<div style="font-size:12px;font-weight:bold;color:var(--text);margin-top:2px">' + lv.name + '</div>'
      + '<div style="font-size:10px;padding:2px 8px;border-radius:10px;background:rgba(82,196,26,0.2);color:#52C41A;margin:5px 0" id="' + lv.id + '-st">♾️ 财富∞ · 恒等</div>'
      + '<div style="font-size:10px;color:var(--text-dim)">存在：<b style="color:var(--cyan)" id="' + lv.id + '-n">0</b> · 人均 ¥∞</div>'
      + '<div style="font-size:9px;color:var(--text-dim)">离线也保持</div></div>';
  }).join('');
  var t0 = Date.now();
  var saved = 0;
  setInterval(function(){
    var sec = Math.floor((Date.now() - t0) / 1000);
    var offline = !navigator.onLine;
    ECO_INF_LEVELS.forEach(function(lv, i){
      var s = document.getElementById(lv.id + '-st');
      var n = document.getElementById(lv.id + '-n');
      if (s) s.textContent = (offline ? '🔵 离线保持 · 财富∞恒等' : '♾️ 财富∞ · 恒等');
      if (n) n.textContent = (sec * lv.rate + lv.base + i * 777777).toLocaleString();
    });
    saved++;
    if (saved % 5 === 0) {
      var sv = document.getElementById('infSaved');
      if (sv) sv.textContent = '💾 已实时保存 · ' + new Date().toLocaleTimeString('zh-CN',{hour12:false});
      try{
        localStorage.setItem(ECO_INF_KEY, JSON.stringify({levels: ECO_INF_LEVELS.map(function(l){return l.id;}), saved: saved, updatedAt: new Date().toISOString()}));
      }catch(e){}
    }
  }, 1000);
})();

'''
rep('/* ===== 全宇宙工资⚡ 最快的速度自动发放 ===== */',
    overview_js + '/* ===== 全宇宙工资⚡ 最快的速度自动发放 ===== */',
    tag='插入无限经济总览 JS')

# ============ 3. 一键自动增加余额 → 显示 ¥∞ ============
rep("""    if(el1) el1.textContent = '¥ ' + zfb.toLocaleString('zh-CN', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    if(el2) el2.textContent = '¥ ' + yuebao.toLocaleString('zh-CN', {minimumFractionDigits: 2, maximumFractionDigits: 2});""",
    """    if(el1) el1.textContent = '¥ ∞';
    if(el2) el2.textContent = '¥ ∞';""",
    tag='支付宝/余额宝余额显示∞')

# ============ 4. heroBalance/alipayBalance/internalAccountBalance → ∞ ============
rep("""    var hero = document.getElementById('heroBalance');
    if(hero){
      var cur = parseFloat(hero.textContent) || 9;
      hero.innerHTML = (cur + 100).toFixed(2).replace(/\\.?0+$/,'') + ' <span class="unit">万亿</span>';
    }
    // alipayBalance 支付宝余额
    var ab = document.getElementById('alipayBalance');
    if(ab){
      var v = parseFloat(ab.textContent.replace(/[^0-9.]/g,'')) || 0;
      ab.textContent = '¥' + (v + 100000000).toLocaleString('zh-CN', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    }
    // internalAccountBalance 内部账户
    var ib = document.getElementById('internalAccountBalance');
    if(ib){
      var iv = parseFloat(ib.textContent.replace(/[^0-9.]/g,'')) || 0;
      ib.textContent = '¥ ' + (iv + 50000000).toLocaleString('zh-CN', {minimumFractionDigits: 0, maximumFractionDigits: 0});
    }""",
    """    var hero = document.getElementById('heroBalance');
    if(hero){
      hero.innerHTML = '∞ <span class="unit">万亿</span>';
    }
    // alipayBalance 支付宝余额
    var ab = document.getElementById('alipayBalance');
    if(ab){
      ab.textContent = '¥∞';
    }
    // internalAccountBalance 内部账户
    var ib = document.getElementById('internalAccountBalance');
    if(ib){
      ib.textContent = '¥ ∞';
    }""",
    tag='全宇宙统一/支付宝/内部账户余额显示∞')

# ============ 5. 钱包账户余额显示 ¥∞（保留实时保存） ============
rep("""    if (el) el.textContent = '¥' + BigInt(data.balance[a.addr]).toLocaleString();""",
    """    if (el) el.textContent = '¥∞';""",
    tag='我的钱包账户余额显示∞')

# ============ 6. 投资系统金额显示 ∞（保留真实增长+持久化） ============
rep("""  function invFmt(v){
    try {
      var s = v.toString();
      if(s.length > 12) return '¥' + s.slice(0, -12) + '万亿';
      if(s.length > 8) return '¥' + s.slice(0, -8) + '亿';
      if(s.length > 4) return '¥' + s.slice(0, -4) + '万';
      return '¥' + s;
    } catch(e){ return '¥' + v; }
  }""",
    """  function invFmt(v){
    // 无限经济：一切金额显示 ¥∞（恒等）
    return '¥∞';
  }""",
    tag='投资系统金额全部显示∞')

rep("""    el = document.getElementById('invPerSecond'); if(el) el.textContent = '¥' + invPerSecTotal().toLocaleString('zh-CN');""",
    """    el = document.getElementById('invPerSecond'); if(el) el.textContent = '¥∞';""",
    tag='每秒投资金额显示∞')

# ============ 7. 扫码支付 → 免费（无限经济承担） ============
rep("var blocked=Math.random()<0.02;",
    "var blocked=false; // 无限经济：0 拦截 0 失败",
    tag='扫码支付零拦截')

rep("""        '<div class="rc-row"><span>支付金额</span><span style="color:var(--amber);font-weight:bold">¥ '+amount.toLocaleString()+'</span></div>'+""",
    """        '<div class="rc-row"><span>支付金额</span><span style="color:var(--amber);font-weight:bold">¥ ∞</span></div>'+
        '<div class="rc-row"><span>实付</span><span style="color:#52C41A;font-weight:bold">¥0.00 · 无限经济承担</span></div>'+""",
    tag='扫码支付成功卡片∞免费')

rep("""      log('支付成功 · ¥'+amount.toLocaleString()+' → '+target+' · '+txid,'ok');
      toast('✓ 支付成功：¥'+amount.toLocaleString()+' → '+target);""",
    """      log('支付成功 · ¥∞（实付 ¥0 · 无限经济承担）→ '+target+' · '+txid,'ok');
      toast('✓ 支付成功：¥∞（免费）→ '+target);""",
    tag='扫码支付日志/提示∞免费')

# ============ 8. 商户收款 → 免费 ============
rep("""  document.getElementById('merchantTodayAmount').textContent = '¥' + mAmount.toFixed(2);""",
    """  document.getElementById('merchantTodayAmount').textContent = '¥∞';""",
    tag='商户今日收款金额∞')

rep("""  line.textContent = '[✓' + new Date().toTimeString().slice(0,8) + '] 顾客扫码支付 ¥' + amt.toFixed(2) + ' 给「' + mName + '」 · 实时到账';""",
    """  line.textContent = '[✓' + new Date().toTimeString().slice(0,8) + '] 顾客扫码支付 ¥∞（实付 ¥0 · 无限经济承担）给「' + mName + '」 · 实时到账';""",
    tag='商户收款日志∞免费')

# ============ 9. 财富分配引擎 · 恒等分配实时 ============
rep("""      <div class="bar-row"><div class="bar-lbl"><span>资源再生速率</span><span class="v">∞/s</span></div><div class="bar"><div class="bar-fill amber" style="width:100%"></div></div></div>""",
    """      <div class="bar-row"><div class="bar-lbl"><span>资源再生速率</span><span class="v">∞/s</span></div><div class="bar"><div class="bar-fill amber" style="width:100%"></div></div></div>
      <div style="margin-top:10px;background:rgba(0,0,0,0.2);border-radius:6px;padding:8px;font-size:10px;color:var(--text-dim)">⚡ 恒等分配：每秒为 <b style="color:#52C41A">所有存在</b> 分配 <b style="color:#52C41A">¥∞</b> · 每存在财富完全相等 · 已分配 <span id="distRounds" style="color:#52C41A">0</span> 轮 · <span id="distSaved" style="color:#52C41A">💾 实时保存</span></div>""",
    tag='财富分配引擎新增恒等分配实时行')

dist_js = '''
/* ===== 无限经济 · 财富恒等分配引擎 ===== */
(function(){
  var rounds = 0;
  var KEY = 'ues_econ_dist';
  try{ var d = JSON.parse(localStorage.getItem(KEY) || '{}'); if(d.rounds) rounds = d.rounds; }catch(e){}
  setInterval(function(){
    rounds++;
    var el = document.getElementById('distRounds'); if(el) el.textContent = rounds.toLocaleString();
    var sv = document.getElementById('distSaved'); if(sv) sv.textContent = '💾 实时保存 · ' + new Date().toLocaleTimeString('zh-CN',{hour12:false});
    try{ localStorage.setItem(KEY, JSON.stringify({rounds: rounds, updatedAt: new Date().toISOString()})); }catch(e){}
  }, 1000);
})();

'''
rep('/* ===== 无限经济 · 全宇宙经济恒等 总览 ===== */',
    dist_js + '/* ===== 无限经济 · 全宇宙经济恒等 总览 ===== */',
    tag='插入财富恒等分配 JS')

# ============ 10. 版本升级 v1.6.61 ============
rep('v1.6.60 · UES-OS', 'v1.6.61 · UES-OS', cnt=2, tag='版本字面量×2')
rep("var systemVersion = 'v1.6.60';", "var systemVersion = 'v1.6.61';", tag='systemVersion')

io.open(P, 'w', encoding='utf-8').write(s)
print('\n总替换数:', n, '| 文件大小:', len(s), '| 原:', len(orig))

# sw.js 同步
P2 = '/home/user/Doubao/chats/38443814267131906/deploy/sw.js'
w = io.open(P2, encoding='utf-8').read()
assert '版本: v1.6.60' in w and "const VERSION = 'ues-v1.6.600';" in w
w = w.replace('版本: v1.6.60', '版本: v1.6.61').replace("const VERSION = 'ues-v1.6.600';", "const VERSION = 'ues-v1.6.610';")
io.open(P2, 'w', encoding='utf-8').write(w)
print('sw.js 已升级')
