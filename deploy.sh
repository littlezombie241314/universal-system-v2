#!/usr/bin/env bash
# ============================================================
# 全宇宙恒等系统 · ARM / x86 Linux 一键部署脚本
# 支持:
#   - aarch64  (鲲鹏920 / 飞腾2000 / 树莓派4/5 / 瑞芯微 RK3588 / 华为云鲲鹏)
#   - armv7l   (树莓派3 / 老款 ARM 工控板)
#   - x86_64   (阿里云 / 腾讯云 / AWS / 华为云 x86)
#   - loongarch / mips 等若有 python3 也可走兜底方案
# 用法:
#   chmod +x deploy.sh
#   sudo ./deploy.sh            # 部署到 /opt/universal-system, 端口 8080
#   PORT=9000 ./deploy.sh       # 自定义端口(无需 sudo 时)
# ============================================================
set -e

APP_NAME="universal-system"
PORT="${PORT:-8080}"
INSTALL_DIR="${INSTALL_DIR:-/opt/universal-system}"
SRC_DIR="$(cd "$(dirname "$0")" && pwd)"

# 颜色
G() { echo -e "\033[32m$*\033[0m"; }
Y() { echo -e "\033[33m$*\033[0m"; }
R() { echo -e "\033[31m$*\033[0m"; }

G "==> 全宇宙恒等系统 · 跨架构部署"
G "    架构: $(uname -m)"
G "    端口: $PORT"
G "    目标: $INSTALL_DIR"

# 1. 拷贝文件
if [ "$(id -u)" -ne 0 ]; then
  Y "    (当前非 root, 若 /opt 不可写请加 sudo)"
  INSTALL_DIR="$HOME/$APP_NAME"
  G "    切换到用户目录: $INSTALL_DIR"
fi

mkdir -p "$INSTALL_DIR"
cp -r "$SRC_DIR"/index.html "$SRC_DIR"/manifest.json "$SRC_DIR"/sw.js \
      "$SRC_DIR"/favicon.ico "$SRC_DIR"/favicon-16.png "$SRC_DIR"/favicon-32.png \
      "$INSTALL_DIR"/
cp -r "$SRC_DIR"/assets "$SRC_DIR"/icons "$INSTALL_DIR"/

G "==> 文件已部署到 $INSTALL_DIR"
ls -la "$INSTALL_DIR"

# 2. 选静态服务器
SERVER=""
if command -v caddy >/dev/null 2>&1; then
  SERVER="caddy"
elif command -v nginx >/dev/null 2>&1; then
  SERVER="nginx"
elif command -v python3 >/dev/null 2>&1; then
  SERVER="python"
  Y "    未找到 caddy/nginx, 用 python3 http.server 兜底(生产建议装 caddy)"
else
  R "    找不到可用静态服务器, 请先安装: caddy 或 nginx 或 python3"
  exit 1
fi
G "==> 使用服务器: $SERVER"

# 3. 写 systemd unit (仅 root 且 systemd 可用时)
if [ "$(id -u)" -eq 0 ] && [ -d /etc/systemd/system ]; then
  UNIT=/etc/systemd/system/${APP_NAME}.service
  cat > "$UNIT" <<EOF
[Unit]
Description=Universal Equality System (跨 ARM/x86 静态站点)
After=network.target

[Service]
Type=simple
WorkingDirectory=$INSTALL_DIR
ExecStart=$(command -v $SERVER) $([ "$SERVER" = "python" ] && echo "-m http.server $PORT --bind 0.0.0.0 --directory $INSTALL_DIR" || echo "run --address :$PORT --root $INSTALL_DIR")
Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF
  systemctl daemon-reload
  systemctl enable --now "$APP_NAME"
  sleep 1
  G "==> systemd 服务已启动: $APP_NAME"
  systemctl --no-pager status "$APP_NAME" | head -10 || true
else
  # 用户态: nohup 后台跑
  PIDFILE="$INSTALL_DIR/run.pid"
  case "$SERVER" in
    python) nohup python3 -m http.server "$PORT" --bind 0.0.0.0 --directory "$INSTALL_DIR" >"$INSTALL_DIR/server.log" 2>&1 & ;;
    caddy)  nohup caddy run --address :$PORT --root $INSTALL_DIR >"$INSTALL_DIR/server.log" 2>&1 & ;;
  esac
  echo $! > "$PIDFILE"
  Y "==> 已在后台启动, PID=$(cat $PIDFILE), 日志: $INSTALL_DIR/server.log"
fi

# 4. 验证 (只检查 HTTP 200 与关键资源, 不触发任何业务/太阳风暴模拟)
sleep 1
G "==> 验证..."
for path in / /manifest.json /sw.js /assets/qrcode.min.js /icons/icon-192.png; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:$PORT$path" || echo "000")
  if [ "$code" = "200" ]; then
    G "    [OK] $path"
  else
    R "    [FAIL] $path -> HTTP $code"
  fi
done

echo
G "✅ 全宇宙恒等系统已部署完成"
G "   本机访问:   http://127.0.0.1:$PORT/"
G "   局域网访问: http://$(hostname -I 2>/dev/null | awk '{print $1}'):$PORT/"
echo
Y "   Android/iOS/鸿蒙: 用浏览器打开上面地址, 菜单选「添加到主屏幕」即可安装为 PWA"
Y "   本机服务器管理: systemctl status|restart|stop $APP_NAME"
