# 全宇宙恒等系统 · 多架构 Dockerfile
# 构建: docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t universal-system .
# 运行: docker run -d --restart=always -p 8080:80 --name universal-system universal-system
# 兼容: 云服务器(x86_64) / ARM 工控板(树莓派4/5、瑞芯微、飞腾、鲲鹏、麒麟) / 移动 SoC 跑 Linux 的设备

FROM caddy:2-alpine

# 工作目录
WORKDIR /srv

# 拷贝静态站点
COPY index.html ./
COPY manifest.json ./
COPY sw.js ./
COPY favicon.ico favicon-16.png favicon-32.png ./
COPY assets/ ./assets/
COPY icons/ ./icons/

# Caddy 配置
COPY Caddyfile /etc/caddy/Caddyfile

EXPOSE 80

# 健康检查: 拉首页
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1/ >/dev/null 2>&1 || exit 1
