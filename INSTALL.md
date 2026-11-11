# 全宇宙恒等系统 · 安装说明

**当前版本** v1.6.95 · `index.html` 1,343,152 字节 · md5 `cfb802b29f58e49bec9cd4701f74835d`
**Service Worker** `ues-v1.6.950` · **PWA** `display: standalone`（可安装、可离线启动）
**适用端** Android / iPhone / iPad / HarmonyOS / Windows / macOS / Linux / 云主机 / ARM 工控板

> 本文所有命令、路径、参数都与仓库里的 `deploy/` 目录实际内容一致；改动代码后请同步更新版本号与 md5。

---

## 0. 先选一种装法（30 秒判断）

| 你的目标 | 用哪一节 | 需要准备什么 |
|---|---|---|
| 只想马上用起来 | [§1 直接打开](#1-直接打开零安装) | 一个浏览器 |
| 想在手机/电脑桌面有独立图标、能离线 | [§2 安装为 App（PWA）](#2-安装为-apppwa) | 浏览器 + HTTPS（线上地址已满足） |
| 想在断网的内网/工控板上跑 | [§3 本地静态运行](#3-本地静态运行内网工控板) | Python 3 或 Caddy/Nginx |
| 想装到自己的 Linux 服务器 / Docker | [§4 服务器与 Docker](#4-linux-服务器与-docker) | root 或 docker |
| 想更新到各云平台（Surge/CF/阿里云…） | [§5 云平台一键部署](#5-云平台一键部署发布者用) | 各平台凭据 |

**系统结构只有 5 类文件**，没有任何构建步骤、没有后端必须自建：

```
deploy/
├── index.html          # 整站前端（单文件，约 1.3 MB）
├── sw.js               # Service Worker（离线缓存 + 版本淘汰）
├── manifest.json       # PWA 清单（名称/图标/独立窗口）
├── icons/              # icon-192 / icon-512 / maskable / apple-touch-icon
├── assets/             # qrcode.min.js、JsBarcode.all.min.js、jsQR.js（本地化，不走外网 CDN）
├── deploy.sh           # Linux/ARM 一键部署（systemd）
├── Dockerfile          # 多架构镜像（caddy:2-alpine）
├── Caddyfile           # 静态站点 + PWA 缓存头
├── deploy_stable.sh    # 多平台发布 + 校验
└── aliyun_deploy.py    # 阿里云 OSS 发布器
```

---

## 1. 直接打开（零安装）

浏览器输入下面任一地址，等启动序列（BIOS → NET → BOOT）跑完即进入控制台。**不用注册、不用装任何东西。**

| 用途 | 地址 |
|---|---|
| 主入口（推荐） | `https://universal-system-final.surge.sh/` |
| 备用 1/2/3/4 | `https://universal-system-latest.surge.sh/`、`https://universal-system.surge.sh/`、`https://universal-system-deploy.surge.sh/`、`https://universal-equality.surge.sh/` |
| GitHub Pages | `https://littlezombie241314.github.io/universal-system-v2/`（CNAME 指向主入口） |
| Cloudflare Pages | `https://universal-system.pages.dev/` |
| Cloudflare Workers | `https://universal-equality.universal-equality.workers.dev/` |
| Netlify | `https://universal-system-v2.netlify.app/` |
| Vercel | `https://universal-system-v2.vercel.app/` |
| 豆包应用版 | `https://xb4r414nb9.doubaoapps.com/app/app_17f4htz1kfy/` |
| 阿里云 OSS | `https://universal-system.oss-cn-hangzhou.aliyuncs.com/index.html`（**只下载、不渲染**，见 §5.3） |

任一口打不开就换下一个，内容完全一致（同一版本、同一 md5）。

**首次打开后**核心资源会进入 Service Worker 缓存，之后断网也能启动；页面上的实时数据项（天气、空气质量、经济/支付等跨域接口）在断网时会取不到最新值，本地功能照常运行。

---

## 2. 安装为 App（PWA）

前提：**HTTPS 站点**（上面的线上地址都满足），或 `http://localhost`。纯 HTTP 的局域网 IP 不满足浏览器安全要求，装不了（见 §3.3）。

### 2.1 Android / HarmonyOS

1. 用 Chrome 或系统浏览器打开主入口地址
2. 等页面加载完（约 3–10 秒）
3. 右上角菜单 → **「添加到主屏幕」/「安装应用」**
4. 桌面出现「全宇宙恒等」图标，点开是独立窗口（没有地址栏）

### 2.2 iPhone / iPad

必须用 **Safari**（微信/QQ 内置浏览器不行）：

1. Safari 打开地址
2. 底部 **分享** 按钮 → 向上滑 → **「添加到主屏幕」** → 添加
3. 图标来自 `icons/apple-touch-icon.png`

### 2.3 Windows / macOS / Linux 桌面

Chrome / Edge：

- 地址栏右侧出现「安装」图标 → 点它；或
- 菜单（⋮ / …）→ **「安装全宇宙恒等系统…」/「将此站点作为应用安装」**

安装后从开始菜单/程序坞启动，窗口独立，可离线打开。

### 2.4 装完怎么确认真的装上了

| 检查项 | 期望结果 |
|---|---|
| 窗口形态 | 独立窗口，无地址栏、无标签页 |
| 开发者工具 → Application → Manifest | 名称「全宇宙恒等系统 · UNIVERSAL EQUALITY SYSTEM」，图标 192/512 正常 |
| Application → Service Workers | `sw.js` 状态 **activated and is running**，版本 `ues-v1.6.950` |
| 断网测试 | 关掉 Wi-Fi 再点图标，仍能进入控制台 |

### 2.5 更新与"一直是旧版"

- 页面导航走**网络优先**：联网打开就是最新版；离线才回退缓存。
- 更新生效靠 `sw.js` 里的 `VERSION`（当前 `ues-v1.6.950`）变化触发：新版本号 → 安装新缓存 → 删除旧缓存。
- 若仍看到旧版：关掉所有该站标签页重开；或 DevTools → Application → Service Workers → **Unregister** → 刷新两次。

---

## 3. 本地静态运行（内网/工控板）

### 3.1 最快：Python 起一个静态服务

```bash
cd deploy
python3 -m http.server 8080 --bind 0.0.0.0
# 打开 http://127.0.0.1:8080/
```

手机同 Wi-Fi 时用 `http://<电脑IP>:8080/` 打开（能看能用，但因非 HTTPS 无法"安装为 App"）。

### 3.2 不要用 `file://` 双击打开

`index.html` 双击能用大部分功能，但 **Service Worker 不会注册**（浏览器禁止 `file://` 下注册），因此没有离线缓存、也不能安装。请始终用本地 HTTP 服务。

### 3.3 想在局域网也能安装（HTTPS）

两条路：

- 用 Caddy 直接跑（自动 HTTPS 需要域名）：
  ```bash
  caddy run --config Caddyfile   # 仓库已带 Caddyfile，:80 静态托管 + PWA 缓存头
  ```
- 或者把 `deploy/` 整个放到任意支持 HTTPS 的静态托管（§5），手机访问那个地址再安装。

### 3.4 必带的缓存头（自己配 Nginx/Caddy 时）

| 路径 | Cache-Control | 原因 |
|---|---|---|
| `sw.js` | `no-cache, no-store, must-revalidate` | 否则新版本永远不生效 |
| `index.html`、`/` | `no-cache` | 保证拿到最新页面 |
| `manifest.json` | `max-age=300` | 改了图标能较快生效 |
| `assets/*`、`icons/*`、`favicon*` | `public, max-age=86400` | 静态资源可长缓存 |

`Caddyfile` 已按上表配好，直接复用即可。

---

## 4. Linux 服务器与 Docker

### 4.1 一键脚本（x86_64 / ARM64 / ARMv7 通用）

支持鲲鹏 920、飞腾 2000、树莓派 4/5、RK3588、阿里云倚天、AWS Graviton 等，脚本自动识别架构，无需改参数。

```bash
scp -r deploy/ root@<服务器IP>:/root/
ssh root@<服务器IP>
cd /root/deploy
chmod +x deploy.sh
sudo ./deploy.sh                 # 安装到 /opt/universal-system，端口 8080
# 或自定义：
sudo PORT=9000 INSTALL_DIR=/srv/ues ./deploy.sh
```

脚本行为：

- 复制站点文件到 `INSTALL_DIR`
- 按可用性选择 `caddy` → `nginx` → `python3 http.server` 兜底
- root + systemd 环境下写入 `/etc/systemd/system/universal-system.service` 并启动
- 自动验证 `/`、`/manifest.json`、`/sw.js`、`/assets/qrcode.min.js`、`/icons/icon-192.png` 均返回 200

管理命令：

```bash
systemctl status universal-system
systemctl restart universal-system
journalctl -u universal-system -n 50
```

### 4.2 Docker（多架构）

```bash
# 单架构构建并运行
docker build -t universal-system .
docker run -d --restart=always -p 8080:80 --name universal-system universal-system
# 打开 http://<服务器IP>:8080/
```

多架构镜像（amd64 + arm64 + armv7）：

```bash
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t <你的仓库>/universal-system:1.6.95 --push .
```

镜像基于 `caddy:2-alpine`，内置 `Caddyfile`（含 PWA 缓存头与 `Service-Worker-Allowed: /`），自带健康检查。

### 4.3 上公网前的两件事

1. **HTTPS**：PWA 安装与 Service Worker 都要求安全上下文，绑定域名后让 Caddy 自动签发证书，或在前置反代（Nginx/CDN）终止 TLS。
2. **别把 `sw.js` 交给长缓存**：CDN/反代上给 `sw.js` 设 `no-store`，否则用户长期停在旧版本。

---

## 5. 云平台一键部署（发布者用）

> 这一节是"把新版本发到线上"，普通安装用户不需要看。

### 5.1 依赖

| 依赖 | 用途 | 安装 |
|---|---|---|
| `bash` / `curl` / `md5sum` | 脚本主体与校验 | 系统自带 |
| `python3` + `oss2` | 阿里云 OSS 发布 | `pip install --user oss2`（实测 2.19.1） |
| Node.js + `wrangler` | Cloudflare Workers / Pages | `npm i -g wrangler` |
| `lark-cli` | doubaoapps 发布 | 按 html Skill 的 CLI 安装方式 |
| `surge` | Surge×5 | `npm i -g surge` |

### 5.2 命令表（`deploy_stable.sh`）

```bash
bash deploy_stable.sh              # 全平台（surge → github → doubaoapps → cloudflare → verify）
bash deploy_stable.sh --surge      # Surge 5 个站点
bash deploy_stable.sh --github     # master + gh-pages
bash deploy_stable.sh --doubaoapps # 豆包应用（内部轮询 release 到 finished）
bash deploy_stable.sh --cloudflare # Workers（打印版本 id 与流量占比）
bash deploy_stable.sh --aliyun     # 阿里云 OSS（需先 source 凭据，见 5.3）
bash deploy_stable.sh --verify     # 只校验，不改线上
```

脚本特性：每一步带指数退避重试；`curl` 用 `--noproxy` 直连绕缓存；发布后按 `md5` 逐站比对，失败项会明确列出。

发布前把 `deploy/index.html`、`deploy/sw.js` 更新到最新，并确认版本号一致：

```bash
grep -c "v1.6.95" deploy/index.html     # 期望 5
grep -o "ues-v1.6.950" deploy/sw.js     # 期望 1
md5sum deploy/index.html                # 期望 cfb802b2...
```

**注意**：`--verify` 的阿里云 md5 校验需要显式给出站点地址，否则只做状态提示：

```bash
export ALIYUN_SITE_URL="https://universal-system.oss-cn-hangzhou.aliyuncs.com/index.html"
bash deploy_stable.sh --verify
```

### 5.3 阿里云 OSS 通道

准备工作：

1. 阿里云账号已**开通 OSS**（控制台 → 对象存储 → 立即开通）
2. 创建 AccessKey：RAM 控制台 → 用户 → 创建 AccessKey（建议 RAM 子账号 + `AliyunOSSFullAccess`；主账号 AK 权限过大，仅作应急）
3. 凭据写进本机文件，不要进仓库：

```bash
umask 077
cat > ~/.ues_aliyun_env <<'EOF'
export ALIYUN_ACCESS_KEY_ID='<你的 AK ID>'
export ALIYUN_ACCESS_KEY_SECRET='<你的 AK Secret>'
export ALIYUN_REGION='cn-hangzhou'
export ALIYUN_OSS_BUCKET='universal-system'
EOF
chmod 600 ~/.ues_aliyun_env
```

发布：

```bash
source ~/.ues_aliyun_env
bash deploy_stable.sh --aliyun
# 或单独跑发布器：
python3 aliyun_deploy.py --dir /tmp/uv2_publish --bucket universal-system --region cn-hangzhou
```

发布器会做四件事，缺一不可：

| 步骤 | 说明 |
|---|---|
| 建 bucket | 不存在则创建（`public-read`） |
| **关闭「阻止公共访问」** | 阿里云新建 bucket 默认开启，开着会匿名 403 `AccessDenied ... because of bucket acl` |
| 设公共读 | `put_bucket_acl(PUBLIC_READ)` |
| 开静态网站托管 | `BucketWebsite(index_file="index.html", error_file="index.html")` |

**两个必须知道的事实：**

- 站点地址是 `https://<bucket>.oss-<region>.aliyuncs.com/index.html`。
  `https://<bucket>.<region>.aliyuncs.com` 这种写法 **DNS 不存在（NXDOMAIN）**，不要用。
- 阿里云 **默认域名对 HTML 强制下载**（响应头 `Content-Disposition: attachment`、`x-oss-force-download: true`）。要"打开就是网页"，必须绑定**已备案的自定义域名**并 CNAME 到该 bucket；未备案域名 / 邮箱域（如 `onaliyun.com`）都不行。

### 5.4 其它平台凭据

| 平台 | 凭据位置 |
|---|---|
| Cloudflare（Workers + Pages） | `deploy_stable.sh` 内的 `CF_TOKEN` / `CF_ACCOUNT`；Pages 另需 export `CLOUDFLARE_API_TOKEN`、`CLOUDFLARE_ACCOUNT_ID` 后 `wrangler pages deploy` |
| Surge | 首次 `surge login`，之后本机保存 token |
| GitHub | 本机 `deploy/` 仓库已配好远端，`git push` 即可 |
| doubaoapps | `lark-cli` 已登录（`app_id: app_17f4htz1kfy`） |
| Netlify | 网页端登录后拖拽 zip 上传（CLI 未登录时的稳妥路径） |
| Vercel | GitHub 集成自动部署，看 Deployments 里 Production 行的 commit + Ready |

---

## 6. 安装后验证清单

按顺序做，每项都能独立判断：

1. **资源可达**（不触发任何业务逻辑）
   ```bash
   for p in / /manifest.json /sw.js /assets/qrcode.min.js /icons/icon-192.png; do
     printf "%s -> %s\n" "$p" "$(curl -s -o /dev/null -w '%{http_code}' --noproxy '*' "https://universal-system-final.surge.sh$p")"
   done
   ```
   期望全部 200。
2. **版本指纹**：页面内 `v1.6.95` 出现 5 处；`index.html` md5 `cfb802b2…`、大小 1,343,152 B。
3. **PWA**：DevTools → Application，Manifest 无报错、Service Worker 为 activated；断网后仍能打开。
4. **界面真实点击**：点顶部的「☁️ 云平台部署状态」里的阿里云卡片，应弹出
   `阿里云已发布 · https://universal-system.oss-cn-hangzhou.aliyuncs.com/index.html（默认域名强制下载）`，
   卡片状态为「✅ 已发布」。
5. **全平台一致性**：`bash deploy_stable.sh --verify`，结尾必须是「全平台验证完成，无失败项」。
6. 太阳风暴模块**只做资源可达性检查**，不要点"模拟风暴"来验证。

---

## 7. 常见问题

| 现象 | 原因 | 处理 |
|---|---|---|
| 打开一片黑/一直转圈 | 首次加载 1.3 MB，弱网慢 | 等 10–20 秒；换备用域名 |
| 改了代码线上没变 | `sw.js` 被缓存 / 版本号没改 | 改 `VERSION` → 重新发布 → 强刷或 Unregister SW |
| 没有「安装」按钮 | 非 HTTPS、非 localhost，或浏览器不支持 | 用线上 HTTPS 地址；iOS 必须 Safari 手动添加 |
| iOS 添加到主屏幕后没图标 | `apple-touch-icon.png` 缺失或路径错 | 确认 `icons/apple-touch-icon.png` 返回 200 |
| 手机上打不开局域网地址 | 防火墙/不同网段 | 确认同 Wi-Fi、端口放行 |
| 阿里云 403 `because of bucket acl` | bucket 开着「阻止公共访问」 | `put_bucket_public_access_block(block_public_access=False)` + 公共读 |
| 阿里云打开就下载文件 | 默认域名强制下载 | 绑定已备案自定义域名；否则只能下载 |
| 阿里云域名 NXDOMAIN | 用了 `bucket.region.aliyuncs.com` 错误形态 | 改用 `bucket.oss-region.aliyuncs.com` |
| `systemctl` 找不到服务 | 非 root 或非 systemd 环境 | 用 `PORT=9000 ./deploy.sh`，日志在 `$INSTALL_DIR/server.log` |
| Docker 起来但页面 404 | 构建上下文缺文件 | 在 `deploy/` 目录内构建，确保 `assets/`、`icons/` 存在 |

---

## 8. 卸载 / 回滚

```bash
# systemd 安装
sudo systemctl stop universal-system && sudo systemctl disable universal-system
sudo rm -rf /opt/universal-system /etc/systemd/system/universal-system.service

# Docker
docker rm -f universal-system && docker rmi universal-system
```

回滚到上一版：在 `deploy/` 仓库 `git checkout <上一个 commit> -- index.html sw.js`，同步把 `sw.js` 的 `VERSION` 改回，再按 §5 重新发布并 `--verify`。

---

*文档与 v1.6.95 同步。旧版说明保留在 `INSTALL_legacy_2026-10-09.md`（v1.3.0 时期，仅作历史参考）。*
