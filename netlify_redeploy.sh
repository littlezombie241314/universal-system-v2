#!/usr/bin/env bash
# Netlify 一键补发：额度一旦恢复（或升级账号后），直接跑本脚本即可把 v1.6.99 推上生产。
# 用法：
#   export NETLIFY_AUTH_TOKEN=<后台 Personal access token>
#   bash netlify_redeploy.sh [站点目录]
# 说明：脚本只在 /tmp 生成临时 zip，不落项目目录；上传后立即删除。

set -euo pipefail

SITE_ID="${NETLIFY_SITE_ID:-70c4047d-bbbd-4a28-b651-af9391259dbb}"
SITE_URL="https://universal-system-v2.netlify.app"
EXPECTED_MD5="${EXPECTED_MD5:-c0540f947a4a1366e810a24e1058b07a}"
SITE_DIR="${1:-$(cd "$(dirname "$0")/../site_v1.6.99" && pwd)}"

[ -n "${NETLIFY_AUTH_TOKEN:-}" ] || { echo "缺少 NETLIFY_AUTH_TOKEN，先在 Netlify 后台生成 Personal access token"; exit 1; }
[ -f "$SITE_DIR/index.html" ] || { echo "站点目录不存在: $SITE_DIR"; exit 1; }

MD5="$(md5sum "$SITE_DIR/index.html" | awk '{print $1}')"
echo "index.html md5=$MD5 size=$(wc -c < "$SITE_DIR/index.html")"
[ "$MD5" = "$EXPECTED_MD5" ] || { echo "本地 md5 与预期 $EXPECTED_MD5 不一致，停止上传"; exit 1; }

ZIP="$(mktemp -d)/site.zip"
( cd "$SITE_DIR" && zip -qr "$ZIP" . )
echo "打包完成 $(wc -c < "$ZIP") B"

RESP="$(curl -sS --max-time 300 -H "Authorization: Bearer $NETLIFY_AUTH_TOKEN" \
  -H "Content-Type: application/zip" \
  --data-binary "@$ZIP" \
  "https://api.netlify.com/api/v1/sites/$SITE_ID/deploys")"
rm -rf "$(dirname "$ZIP")"
echo "提交结果: $RESP"

DEPLOY_ID="$(printf '%s' "$RESP" | python3 -c 'import sys,json;print(json.load(sys.stdin).get("id",""))' 2>/dev/null || true)"
if [ -z "$DEPLOY_ID" ]; then
  echo "未拿到 deploy id：多为账号额度拦截（credits exceeded），需等计费周期重置或升级付费档"
  exit 2
fi

for i in $(seq 1 40); do
  ST="$(curl -sS -H "Authorization: Bearer $NETLIFY_AUTH_TOKEN" \
    "https://api.netlify.com/api/v1/deploys/$DEPLOY_ID" | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d.get("state",""))')"
  echo "  [$i] $ST"
  case "$ST" in
    ready|current) break ;;
    error|failed) echo "部署失败"; exit 3 ;;
  esac
  sleep 6
done

echo "线上核对:"
curl -sSL --max-time 120 "$SITE_URL/index.html" -o /tmp/netlify_live.html
LIVE_MD5="$(md5sum /tmp/netlify_live.html | awk '{print $1}')"
echo "  live md5=$LIVE_MD5 size=$(wc -c < /tmp/netlify_live.html)"
[ "$LIVE_MD5" = "$EXPECTED_MD5" ] && echo "  Netlify 已与全平台一致 ✅" || echo "  Netlify 仍不一致 ❌"
rm -f /tmp/netlify_live.html
