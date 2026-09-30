#!/usr/bin/env bash
# ============================================================
# 全宇宙恒等系统 · 防网络抖动全平台部署脚本
# 特性:
#   - 每次网络/部署命令失败自动重试（指数退避）
#   - curl 验证用 --noproxy 直连（绕过代理缓存抖动）
#   - 部署后强制校验内容一致性（md5 / 关键词）
#   - 幂等：任何一步失败只重试该步，不重复已成功步骤
# 用法:
#   ./deploy_stable.sh               # 部署全部平台
#   ./deploy_stable.sh --surge       # 只部署 Surge×5
#   ./deploy_stable.sh --github      # 只推送 GitHub
#   ./deploy_stable.sh --doubaoapps  # 只发布 doubaoapps
#   ./deploy_stable.sh --cloudflare  # 只更新 Cloudflare Workers
#   ./deploy_stable.sh --verify      # 只做全平台验证
# ============================================================
set -u

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
PUBLISH_DIR="/tmp/uv2_publish"
LOCAL_HTML="$APP_DIR/index.html"
EXPECTED_MD5="${EXPECTED_MD5:-$(md5sum "$LOCAL_HTML" 2>/dev/null | awk '{print $1}')}"
CF_TOKEN="${CF_TOKEN:-cfut_0fC32gyeeBWhTtZ81NNcY9YDc3wD1VA8LOJRpZep9000634a}"
CF_ACCOUNT="46d9f2f07b15e133ac141b593d60f241"
CF_WORKER="universal-equality"
DOUBAO_APP_ID="app_17f4htz1kfy"
SURGE_DOMAINS="universal-system-final universal-system-latest universal-system universal-system-deploy universal-equality"

G() { echo -e "\033[32m[OK]\033[0m $*"; }
Y() { echo -e "\033[33m[..]\033[0m $*"; }
R() { echo -e "\033[31m[FAIL]\033[0m $*"; }

# ---------- 防抖动工具函数 ----------
# 带重试执行命令：retry_cmd <次数> <间隔秒> <命令...>
retry_cmd() {
  local max="$1" wait="$2"; shift 2
  local attempt=0
  while [ "$attempt" -lt "$max" ]; do
    attempt=$((attempt+1))
    "$@" && return 0
    if [ "$attempt" -lt "$max" ]; then
      Y "第${attempt}次失败，${wait}s 后重试: $*"
      sleep "$wait"
      wait=$((wait*2))   # 指数退避
    fi
  done
  R "重试 ${max} 次仍失败: $*"
  return 1
}

# 防抖动 curl 下载：curl_retry <输出文件> <URL...>
curl_retry() {
  local out="$1"; shift
  local attempt=0
  while [ "$attempt" -lt 5 ]; do
    attempt=$((attempt+1))
    curl -sL --compressed --noproxy "*" --connect-timeout 15 --max-time 90 "$@" -o "$out" 2>/dev/null
    if [ -s "$out" ]; then return 0; fi
    [ "$attempt" -lt 5 ] && { Y "下载失败(第${attempt}次)，3s 后重试"; sleep 3; }
  done
  R "下载失败 5 次: $*"
  return 1
}

# ---------- 步骤 0: 准备发布目录 ----------
prepare() {
  Y "准备发布目录..."
  mkdir -p "$PUBLISH_DIR"
  rsync -a --exclude '.git' --exclude '.gitignore' --exclude 'index_backup_wormhole.html' --exclude '.github' "$APP_DIR/" "$PUBLISH_DIR/"
  local md5
  md5="$(md5sum "$PUBLISH_DIR/index.html" | awk '{print $1}')"
  if [ "$md5" != "$EXPECTED_MD5" ]; then
    R "发布目录 md5 不一致: $md5 != $EXPECTED_MD5"
    return 1
  fi
  G "发布目录就绪: ${PUBLISH_DIR}/index.html ($(stat -c %s "$PUBLISH_DIR/index.html") bytes, md5 ${md5:0:8})"
}

# ---------- 步骤 1: Surge×5 ----------
deploy_surge() {
  Y "部署 Surge×5..."
  cd "$PUBLISH_DIR" || return 1
  local ok=0
  for domain in $SURGE_DOMAINS; do
    Y "  部署 $domain.surge.sh"
    if retry_cmd 4 5 surge ./ "$domain.surge.sh" >/dev/null 2>&1; then
      # 部署后直连校验（绕过代理缓存）
      local md5=""
      for i in 1 2 3; do
        md5="$(curl -sL --compressed --noproxy "*" --connect-timeout 15 --max-time 90 "https://$domain.surge.sh/index.html?v=$(date +%s%N)" 2>/dev/null | md5sum | awk '{print $1}')"
        [ "$md5" = "$EXPECTED_MD5" ] && break
        Y "  校验不一致(第${i}次, ${md5:0:8}≠${EXPECTED_MD5:0:8})，10s 后重查"
        sleep 10
      done
      if [ "$md5" = "$EXPECTED_MD5" ]; then
        G "  $domain.surge.sh 部署成功并校验一致"
        ok=$((ok+1))
      else
        R "  $domain.surge.sh 部署成功但校验不一致(md5=${md5:0:8})"
        return 1
      fi
    else
      R "  $domain.surge.sh 部署失败(重试后)"
      return 1
    fi
  done
  G "Surge×5 全部部署完成 ($ok/5)"
}

# ---------- 步骤 2: GitHub ----------
deploy_github() {
  Y "推送 GitHub master + gh-pages..."
  cd "$APP_DIR" || return 1
  if ! retry_cmd 3 5 git push origin master >/dev/null 2>&1; then
    R "master 推送失败"
    return 1
  fi
  G "master 推送成功"
  if ! retry_cmd 3 5 git push origin gh-pages >/dev/null 2>&1; then
    R "gh-pages 推送失败"
    return 1
  fi
  G "gh-pages 推送成功"
  # 校验 Pages 线上（CDN 有延迟，最多等 90s）
  local md5="" ok=0
  for i in $(seq 1 9); do
    md5="$(curl -sL --compressed --noproxy "*" --connect-timeout 15 --max-time 90 "https://littlezombie241314.github.io/universal-system-v2/?v=$(date +%s)" 2>/dev/null | md5sum | awk '{print $1}')"
    if [ "$md5" = "$EXPECTED_MD5" ]; then ok=1; break; fi
    Y "  Pages CDN 同步中(第${i}次, ${md5:0:8})，10s 后重查"
    sleep 10
  done
  if [ "$ok" = "1" ]; then
    G "GitHub Pages 线上校验一致"
  else
    Y "GitHub Pages 线上仍在 CDN 缓存中（分支已推送，稍后会同步）"
  fi
}

# ---------- 步骤 3: doubaoapps ----------
deploy_doubaoapps() {
  Y "发布 doubaoapps..."
  cd "$PUBLISH_DIR" || return 1
  local rel_id=""
  for i in 1 2 3; do
    rel_id="$(lark-cli apps +deploy --file-path ./index.html --app-id "$DOUBAO_APP_ID" 2>&1 | python3 -c "
import json,sys
raw = sys.stdin.read()
try:
    start = raw.index('{')
    d = json.loads(raw[start:])
    print(d.get('data',{}).get('release_id',''))
except: print('')
")"
    [ -n "$rel_id" ] && break
    Y "  发布受理失败(第${i}次)，5s 后重试"
    sleep 5
  done
  if [ -z "$rel_id" ]; then R "doubaoapps 发布受理失败"; return 1; fi
  Y "  release_id: $rel_id，轮询中..."
  for i in $(seq 1 12); do
    local status=""
    status="$(lark-cli apps +release-get --app-id "$DOUBAO_APP_ID" --release-id "$rel_id" 2>&1 | python3 -c "
import json,sys
raw = sys.stdin.read()
try:
    start = raw.index('{')
    d = json.loads(raw[start:])
    print(d.get('data',{}).get('status',''))
except: print('')
")"
    if [ "$status" = "finished" ]; then
      G "doubaoapps 发布完成"
      return 0
    fi
    if [ "$status" = "failed" ]; then R "doubaoapps 发布失败"; return 1; fi
    sleep 5
  done
  R "doubaoapps 发布超时"
  return 1
}

# ---------- 步骤 4: Cloudflare ----------
deploy_cloudflare() {
  Y "更新 Cloudflare Workers..."
  cp "$PUBLISH_DIR/index.html" "$APP_DIR/../worker/public/index.html" || return 1
  cd "$APP_DIR/../worker" || return 1
  export CLOUDFLARE_API_TOKEN="$CF_TOKEN"
  if ! retry_cmd 3 8 wrangler deploy >/dev/null 2>&1; then
    R "wrangler deploy 失败(重试后)"
    return 1
  fi
  G "Cloudflare Worker 部署成功"
  # 通过 API 确认 100% 流量
  local ver=""
  for i in 1 2 3; do
    ver="$(curl -s --connect-timeout 15 --max-time 30 "https://api.cloudflare.com/client/v4/accounts/$CF_ACCOUNT/workers/scripts/$CF_WORKER/deployments" -H "Authorization: Bearer $CF_TOKEN" 2>/dev/null | python3 -c "
import json,sys
raw = sys.stdin.buffer.read()
try:
    d = json.loads(raw.decode('utf-8'))
    deps = d.get('result', {}).get('deployments', [])
    if deps:
        vs = deps[0].get('versions', [])
        if vs: print(vs[0].get('version_id','')[:12], vs[0].get('percentage',''))
except: print('')
")"
    [ -n "$ver" ] && break
    sleep 5
  done
  [ -n "$ver" ] && G "Cloudflare 线上版本: $ver% 流量" || Y "Cloudflare 版本确认超时（部署已成功）"
}

# ---------- 步骤 5: 全平台验证 ----------
verify_all() {
  Y "全平台最终验证（直连绕过代理缓存）..."
  local fail=0
  for domain in $SURGE_DOMAINS; do
    local md5=""
    curl_retry /tmp/v_surge.html "https://$domain.surge.sh/index.html?v=$(date +%s%N)"
    md5="$(md5sum /tmp/v_surge.html | awk '{print $1}')"
    if [ "$md5" = "$EXPECTED_MD5" ]; then G "  $domain.surge.sh ✅ ${md5:0:8}"; else R "  $domain.surge.sh ❌ ${md5:0:8}"; fail=1; fi
  done
  curl_retry /tmp/v_gh.html "https://littlezombie241314.github.io/universal-system-v2/?v=$(date +%s)"
  local gh_md5="$(md5sum /tmp/v_gh.html | awk '{print $1}')"
  if [ "$gh_md5" = "$EXPECTED_MD5" ]; then G "  GitHub Pages ✅ ${gh_md5:0:8}"; else Y "  GitHub Pages ⏳ ${gh_md5:0:8}（CDN 缓存中）"; fi
  curl_retry /tmp/v_doubao.html "https://xb4r414nb9.doubaoapps.com/app/app_17f4htz1kfy/"
  local climate="$(grep -c 'climateWeatherIcon' /tmp/v_doubao.html)"
  local speed="$(grep -c 'speedChannelList' /tmp/v_doubao.html)"
  [ "$climate" -ge 4 ] && [ "$speed" -ge 2 ] && G "  doubaoapps ✅ 气候=$climate 网速=$speed" || R "  doubaoapps ❌ 气候=$climate 网速=$speed"
  [ "$fail" = "0" ] && G "全平台验证完成，无失败项" || R "存在验证失败项"
  return "$fail"
}

# ---------- 主流程 ----------
MODE="${1:-all}"
case "$MODE" in
  --surge)      prepare && deploy_surge ;;
  --github)     prepare && deploy_github ;;
  --doubaoapps) prepare && deploy_doubaoapps ;;
  --cloudflare) prepare && deploy_cloudflare ;;
  --verify)     verify_all ;;
  *)            prepare && deploy_surge && deploy_github && deploy_doubaoapps && deploy_cloudflare && verify_all ;;
esac
