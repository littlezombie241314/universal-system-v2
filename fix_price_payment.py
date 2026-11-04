# -*- coding: utf-8 -*-
"""v1.6.64 消费改为按商品价购买·无限钱包扣款（余额仍∞）"""
import io

P = '/home/user/Doubao/chats/38443814267131906/deploy/index.html'
s = io.open(P, encoding='utf-8').read()
n = 0
def rep(old, new, tag=''):
    global s, n
    assert old in s, 'NOT FOUND: ' + tag
    s = s.replace(old, new, 1); n += 1
    print('OK #%d %s' % (n, tag))

# 1. 总览面板：消费 全免费 -> 按价扣款
rep('<div id="infSpend" style="font-size:18px;font-weight:bold;color:#52C41A">全免费</div>',
    '<div id="infSpend" style="font-size:18px;font-weight:bold;color:#52C41A">按价扣款</div>',
    '总览·消费按价扣款')

# 2. 总览页脚
rep('无限经济 · 所有存在财富恒等 ∞ · 消费免费 · 投资 ∞ · 债务 0 · <span id="infSaved"',
    '无限经济 · 所有存在财富恒等 ∞ · 按商品价购买 · 无限钱包扣款 · 投资 ∞ · 债务 0 · <span id="infSaved"',
    '总览页脚·按商品价购买')

# 3. 扫码支付成功卡片
rep("""        '<div class="rc-row"><span>支付金额</span><span style="color:var(--amber);font-weight:bold">¥ ∞</span></div>'+
        '<div class="rc-row"><span>实付</span><span style="color:#52C41A;font-weight:bold">¥0.00 · 无限经济承担</span></div>'+
        '<div class="rc-row"><span>扣款账户</span><span>'+accNames[scanMethod]+'</span></div>'+""",
    """        '<div class="rc-row"><span>支付金额</span><span style="color:var(--amber);font-weight:bold">¥ '+amount.toLocaleString()+'</span></div>'+
        '<div class="rc-row"><span>扣款账户</span><span>无限钱包（'+accNames[scanMethod]+' · 全宇宙恒等APP）</span></div>'+""",
    '扫码支付·按实价+无限钱包扣款')

rep("'<div class=\"rc-row\"><span>当前余额</span><span>¥ 9×10³⁶ 万亿（已自动再生）</span></div></div>';",
    "'<div class=\"rc-row\"><span>当前余额</span><span style=\"color:#52C41A\">¥∞（扣款后仍无限 · 自动补足）</span></div></div>';",
    '扫码支付·当前余额∞扣后仍无限')

# 4. 扫码支付日志/提示
rep("""      log('支付成功 · ¥∞（实付 ¥0 · 无限经济承担）→ '+target+' · '+txid,'ok');
      toast('✓ 支付成功：¥∞（免费）→ '+target);""",
    """      log('支付成功 · 无限钱包扣款 ¥'+amount.toLocaleString()+' → '+target+' · '+txid,'ok');
      toast('✓ 支付成功：¥'+amount.toLocaleString()+' → '+target+'（无限钱包扣款）');""",
    '扫码支付·日志/提示按实价')

# 5. 商户收款：按实价入账
rep("  document.getElementById('merchantTodayAmount').textContent = '¥∞';",
    "  document.getElementById('merchantTodayAmount').textContent = '¥' + mAmount.toFixed(2);",
    '商户收款·按实价累计')

rep("""  line.textContent = '[✓' + new Date().toTimeString().slice(0,8) + '] 顾客扫码支付 ¥∞（实付 ¥0 · 无限经济承担）给「' + mName + '」 · 实时到账';""",
    """  line.textContent = '[✓' + new Date().toTimeString().slice(0,8) + '] 顾客扫码支付 ¥' + amt.toFixed(2) + ' 给「' + mName + '」 · 无限钱包扣款 · 实时到账';""",
    '商户收款·日志按实价+无限钱包扣款')

# 6. 星际娱乐旅行费用
rep('<div style="font-size:10px;color:#52C41A">免费（无限经济）</div>',
    '<div style="font-size:10px;color:#52C41A">按价扣款（无限钱包）</div>',
    '星际娱乐·旅行费用按价扣款')

# 7. 版本 v1.6.63 -> v1.6.64
for a, b in [('v1.6.63 · UES-OS', 'v1.6.64 · UES-OS'),
             ("var systemVersion = 'v1.6.63';", "var systemVersion = 'v1.6.64';")]:
    assert a in s
    s = s.replace(a, b)
print('OK #%d 版本升级 v1.6.64' % (n + 1))
io.open(P, 'w', encoding='utf-8').write(s)

P2 = '/home/user/Doubao/chats/38443814267131906/deploy/sw.js'
x = io.open(P2, encoding='utf-8').read()
assert '版本: v1.6.63' in x and "const VERSION = 'ues-v1.6.630';" in x
x = x.replace('版本: v1.6.63', '版本: v1.6.64').replace("const VERSION = 'ues-v1.6.630';", "const VERSION = 'ues-v1.6.640';")
io.open(P2, 'w', encoding='utf-8').write(x)
print('sw.js 升级 v1.6.64')
