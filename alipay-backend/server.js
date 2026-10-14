/**
 * 全宇宙恒等系统 - 真实支付宝转账后端（沙箱/生产双模式）
 * 部署：onrender / vercel / 任意 Node 云主机
 * 环境变量（生产/沙箱二选一，由 ALIPAY_MODE 切换）：
 *   ALIPAY_MODE=sandbox|prod
 *   ALIPAY_APP_ID=        应用APPID（沙箱/生产各自）
 *   ALIPAY_PRIVATE_KEY=   应用私钥（RSA2，PKCS8，换行用 \n）
 *   【公钥模式】ALIPAY_PUBLIC_KEY= 支付宝公钥（沙箱环境取沙箱公钥）
 *   【证书模式】ALIPAY_APP_CERT=应用公钥证书 / ALIPAY_ALIPAY_CERT=支付宝公钥证书 / ALIPAY_ROOT_CERT=根证书
 *   ALIPAY_UID=           收款方支付宝UID（可选，若用固定收款账户）
 *   TRANSFER_AMOUNT_LIMIT=单笔限额（元，默认 100000）
 */
const express = require('express');
const cors = require('cors');
const AlipaySdkModule = require('alipay-sdk');
// 兼容不同版本导出：命名导出 AlipaySdk / default / 直接构造函数
const AlipaySdk = AlipaySdkModule.AlipaySdk || AlipaySdkModule.default || AlipaySdkModule;

const app = express();
app.use(cors());
app.use(express.json());

const fs = require('fs');
const path = require('path');

const MODE = process.env.ALIPAY_MODE || 'sandbox';
const APP_ID = process.env.ALIPAY_APP_ID || '';
const PRIVATE_KEY = (process.env.ALIPAY_PRIVATE_KEY || '').replace(/\\n/g, '\n');
const ALIPAY_PUBLIC_KEY = (process.env.ALIPAY_PUBLIC_KEY || '').replace(/\\n/g, '\n');
// 证书优先取环境变量；未配置时尝试从仓库 certs/ 目录读取（证书为公开公钥材料）
const certDir = path.join(__dirname, 'certs');
const readCert = (name) => {
  const fromEnv = process.env['ALIPAY_' + name];
  if (fromEnv) return fromEnv.replace(/\\n/g, '\n');
  try { return fs.readFileSync(path.join(certDir, name.toLowerCase() + '.pem'), 'utf8').trim(); }
  catch (e) { return ''; }
};
const APP_CERT = readCert('APP_CERT');
const ALIPAY_CERT = readCert('ALIPAY_CERT');
const ROOT_CERT = readCert('ROOT_CERT');
const LIMIT = parseFloat(process.env.TRANSFER_AMOUNT_LIMIT || '100000');
const GATEWAY = MODE === 'prod'
  ? 'https://openapi.alipay.com/gateway.do'
  : 'https://openapi.alipaydev.com/gateway.do';

const certMode = !!(APP_CERT && ALIPAY_CERT && ROOT_CERT);

let alipay = null;
if (APP_ID && PRIVATE_KEY && (ALIPAY_PUBLIC_KEY || certMode)) {
  try {
    const sdkCfg = {
      appId: APP_ID,
      keyType: 'PKCS8', // 应用私钥为 PKCS8 格式（-----BEGIN PRIVATE KEY-----），避免 SDK 默认按 PKCS1 重写导致 DECODER 失败
      privateKey: PRIVATE_KEY,
      gateway: GATEWAY,
      signType: 'RSA2',
      timeout: 15000,
    };
    if (certMode) {
      // 证书模式：应用公钥证书 + 支付宝公钥证书 + 根证书
      sdkCfg.appCertContent = APP_CERT;
      sdkCfg.alipayPublicCertContent = ALIPAY_CERT;
      sdkCfg.alipayRootCertContent = ROOT_CERT;
    } else {
      sdkCfg.alipayPublicKey = ALIPAY_PUBLIC_KEY;
    }
    alipay = new AlipaySdk(sdkCfg);
    console.log('[支付宝] SDK 已初始化，模式 =', MODE, '· 加签方式 =', certMode ? '证书' : '公钥');
  } catch (e) {
    console.error('[支付宝] SDK 初始化失败:', e.message);
  }
}

const cfgOk = () => !!(alipay && APP_ID && PRIVATE_KEY && (ALIPAY_PUBLIC_KEY || certMode));

app.get('/api/alipay/status', (req, res) => {
  res.json({
    success: true,
    configured: cfgOk(),
    mode: MODE,
    certMode,
    appId: APP_ID ? APP_ID.slice(0, 8) + '****' : '',
    gateway: GATEWAY,
    limit: LIMIT,
    message: cfgOk() ? '✅ 支付宝真实通道已就绪' : '⚠ 未配置凭证（APPID/私钥 + 公钥或证书三件），请在环境变量中配置',
  });
});

/** 凭证诊断（不泄露完整密钥：仅回显长度/首尾/换行特征，排查部署环境变量格式） */
app.get('/api/alipay/diag', (req, res) => {
  const summarize = (s) => ({
    len: (s || '').length,
    head: (s || '').slice(0, 27),
    tail: (s || '').slice(-12),
    realNewlines: ((s || '').match(/\n/g) || []).length,
  });
  res.json({
    success: true,
    appId: APP_ID,
    certMode,
    privateKey: summarize(PRIVATE_KEY),
    alipayPublicKey: summarize(ALIPAY_PUBLIC_KEY),
    appCert: summarize(APP_CERT),
    alipayCert: summarize(ALIPAY_CERT),
    rootCert: summarize(ROOT_CERT),
    sdkCtorOk: typeof AlipaySdk === 'function',
  });
});

/** 余额查询（alipay.fund.account.query - 查询支付宝账户余额，需签约） */
app.get('/api/alipay/balance', async (req, res) => {
  if (!cfgOk()) return res.json({ success: false, configured: false, message: '支付宝通道未配置' });
  try {
    const r = await alipay.exec('alipay.fund.account.query', {
      bizContent: { alipayUserId: req.query.uid || process.env.ALIPAY_UID || '' },
    });
    res.json({ success: true, data: r });
  } catch (e) {
    res.json({ success: false, message: e.message || String(e) });
  }
});

/**
 * 真实转账到支付宝账户（alipay.fund.trans.uni.transfer - 单笔转账）
 * 入参：{ payeeAccount: 支付宝账号/手机号, payeeName: 姓名, amount: 金额, remark: 备注 }
 * 注意：需要支付宝开放平台已签约「转账到支付宝账户」产品
 */
app.post('/api/alipay/transfer', async (req, res) => {
  if (!cfgOk()) return res.json({ success: false, configured: false, message: '支付宝通道未配置，请先配置 APPID/私钥/支付宝公钥' });
  const { payeeAccount, payeeName, amount, remark } = req.body || {};
  if (!payeeAccount) return res.json({ success: false, message: '缺少收款方支付宝账号' });
  const amt = parseFloat(amount);
  if (!amt || amt <= 0) return res.json({ success: false, message: '金额无效' });
  if (amt > LIMIT) return res.json({ success: false, message: '超出单笔限额 ' + LIMIT + ' 元' });

  const outBizNo = 'UES' + Date.now().toString(36).toUpperCase() + Math.random().toString(36).slice(2, 8).toUpperCase();
  const identity = /^1\d{10}$/.test(payeeAccount)
    ? { identityType: 'ALIPAY_LOGON_ID', identity: payeeAccount, name: { full_name: payeeName || '' } }
    : { identityType: 'ALIPAY_USER_ID', identity: payeeAccount };

  try {
    const r = await alipay.exec('alipay.fund.trans.uni.transfer', {
      bizContent: {
        out_biz_no: outBizNo,
        trans_amount: amt.toFixed(2),
        product_code: 'TRANS_ACCOUNT_NO_PWD',
        biz_scene: 'DIRECT_TRANSFER',
        order_title: remark || '全宇宙恒等系统·真实转账',
        payee_info: identity,
      },
    });
    // 支付宝网关业务码：10000=成功；必须显式校验，否则业务失败会被误报为到账成功
    const code = r && (r.code || r.errorCode);
    if (code && code !== '10000') {
      return res.json({
        success: false,
        code,
        subCode: (r && (r.subCode || r.sub_code)) || '',
        message: (r && (r.subMsg || r.sub_msg || r.msg)) || '支付宝网关拒绝该请求',
        outBizNo,
      });
    }
    res.json({
      success: true,
      data: {
        orderId: outBizNo,
        outBizNo,
        status: 'SUCCESS',
        tradeNo: (r && (r.tradeNo || r.trade_no)) || '',
        payDate: (r && (r.payDate || r.pay_date)) || '',
        mode: 'real',
        channel: '支付宝官方·单笔转账',
        payeeAccount,
        amount: amt,
        remark: remark || '',
      },
    });
  } catch (e) {
    res.json({
      success: false,
      message: (e && (e.message || e.rawErrorMessage || e.subMsg)) || String(e),
      outBizNo,
    });
  }
});

/** 转账结果查询（alipay.fund.trans.common.query） */
app.get('/api/alipay/transfer/query', async (req, res) => {
  if (!cfgOk()) return res.json({ success: false, configured: false, message: '支付宝通道未配置' });
  const outBizNo = req.query.outBizNo;
  if (!outBizNo) return res.json({ success: false, message: '缺少 outBizNo' });
  try {
    const r = await alipay.exec('alipay.fund.trans.common.query', {
      bizContent: { out_biz_no: outBizNo, product_code: 'TRANS_ACCOUNT_NO_PWD', biz_scene: 'DIRECT_TRANSFER' },
    });
    res.json({ success: true, data: r });
  } catch (e) {
    res.json({ success: false, message: e.message || String(e) });
  }
});

app.get('/api/health', (req, res) => res.json({ success: true, status: 'ok', mode: MODE }));

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => console.log('[真实支付宝后端] 运行于 :' + PORT + ' · 模式=' + MODE + ' · configured=' + cfgOk()));
