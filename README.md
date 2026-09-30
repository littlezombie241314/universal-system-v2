# 全宇宙恒等系统 · 跨平台部署手册

> **目标**: 把这套 `UNIVERSAL EQUALITY SYSTEM v∞` 跑在云服务器、节点、ARM 工控板、Android / iOS / 鸿蒙手机与平板上，全部可运行、可安装、可离线启动。

---

## 0. 这份部署包做了什么

原站是一个自包含的单页前端（约 790 KB），后端 API 已跑在 `universal-pay-backend.onrender.com`。为了做到"全宇宙可部署"，本包做了三件事：

| 改造 | 说明 |
|---|---|
| **CDN 本地化** | `qrcode.min.js`、`JsBarcode.all.min.js` 从 cdnjs/jsdelivr 拉到本地 `assets/`，不再依赖外网 CDN |
| **PWA 化** | 新增 `manifest.json` + `sw.js` + 各尺寸图标，支持「添加到主屏幕」、离线启动、独立窗口运行 |
| **多架构分发** | 提供 Dockerfile（amd64/arm64/armv7）、ARM 一键脚本、Caddy 静态配置 |

> ⚠️ 后端 API（经济、太阳风暴、复活、天气、空气）仍指向原 `onrender.com` 服务。要把后端也搬走，参考 §7。

---

## 1. 云服务器部署（最快路径）

任选一家，把整个 `deploy/` 目录上传即可。

### 1.1 已有云服务器（阿里云 / 腾讯云 / AWS / 华为云，x86_64 或 ARM 实例均可）

```bash
# 上传
scp -r deploy/ root@<你的服务器IP>:/root/
ssh root@<服务器IP>
cd /root/deploy
chmod +x deploy.sh
./deploy.sh            # 默认端口 8080, 部署到 /opt/universal-system
```

浏览器打开 `http://<服务器IP>:8080/` 即可。

**ARM 云实例**：华为云鲲鹏（km920）、阿里云倚天（g8y）、AWS Graviton 同样可用，无需改脚本——脚本自动识别架构。

### 1.2 Serverless 静态托管（免服务器）

| 平台 | 操作 |
|---|---|
| **Surge.sh**（原站已用） | `npm i -g surge && surge ./deploy` |
| **Cloudflare Pages** | Git 仓库 → 连接 → 构建命令留空，输出目录 `/` |
| **Vercel** | `npx vercel deploy ./deploy` |
| **Netlify** | `npx netlify deploy --dir=deploy --prod` |
| **GitHub Pages** | 推到 `gh-pages` 分支即可 |

这些平台全球都有边缘节点，自动 CDN 到离用户最近的机房。

---

## 2. ARM 工控板 / 嵌入式板卡

### 2.1 硬件兼容表

| 板卡 | 架构 | 本包是否开箱 |
|---|---|---|
| 树莓派 4 / 5（4GB/8GB） | aarch64 | ✅ |
| 树莓派 3 / Zero 2 | armv7l / aarch64 | ✅ |
| 瑞芯微 RK3588 / RK3566（NanoPC、Firefly） | aarch64 | ✅ |
| 飞腾 D2000 / 鲲鹏 920 工控机 | aarch64 | ✅ |
| 华为 Atlas / 麒麟工控板 | aarch64 | ✅ |
| 龙芯 3A5000 | loongarch64 | ⚠️ 走 python3 兜底 |
| 全志 H3 / H6（Orange Pi 老款） | armv7l | ✅ |

### 2.2 部署步骤（树莓派示例）

```bash
# 1. 把 deploy/ 整个 scp 到树莓派
scp -r deploy/ pi@<树莓派IP>:/home/pi/
ssh pi@<树莓派IP>

# 2. 安装 caddy（ARM 官方仓库支持）
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update && sudo apt install -y caddy

# 3. 跑部署脚本
cd /home/pi/deploy
chmod +x deploy.sh
sudo ./deploy.sh
```

板子本身就是一台低功耗嵌入式板卡：CPU 多核调度、内存、闪存、网口/ WiFi 全在主芯片 SoC 上，和用户描述的"高性能低功耗嵌入式板卡"工作模式完全一致。

---

## 3. 移动 SoC 上运行（Android / iOS / 鸿蒙）

移动 SoC（CPU 多核 + GPU + ISP + 基带 + 内存 + 闪存 + 外设驱动）跑的不是 Linux 桌面，而是 Android（Linux 内核）/ iOS（Darwin）/ 鸿蒙（LiteOS/Linux 内核混合）。

**关键点**：因为本系统是 PWA，移动 SoC 上**不需要单独编译 APK/IPA**，用浏览器就能跑，并可"安装"到桌面像原生应用一样。

### 3.1 Android（手机 / 平板 / 车机 / Android 工控机）

1. 用 Chrome / Edge / 华为浏览器打开部署后的地址
2. 菜单 → **「添加到主屏幕」** / **「安装应用」**
3. 桌面会出现"全宇宙恒等系统"图标，点击后**独立窗口运行**（无浏览器地址栏）
4. 首次加载后 service worker 缓存核心资源，**离线也能打开**

**Android 工控板 / 车机**：如果希望开机自启、Kiosk 模式，可以装 **Fully Kiosk Browser** 或用 [Bubblewrap](https://github.com/nickersoft/bubblewrap) 把 PWA 打包成 TWA（Trust Web Activity）APK：

```bash
npm i -g @bubblewrap/cli
bubblewrap init --manifest https://<你的域名>/manifest.json
bubblewrap build    # 产出 universal-system.apk
```

### 3.2 iOS（iPhone / iPad）

1. 用 **Safari** 打开地址（必须是 Safari，Chrome on iOS 不支持添加 PWA）
2. 底部 **分享按钮** → **「添加到主屏幕」**
3. 桌面图标点击后独立全屏运行
4. 首次加载后离线可用

> iOS 对 service worker 的限制：需要 HTTPS（或 localhost）。如果用 IP 直连，建议走 §1.2 的 CDN 平台或加个域名 + Caddy 自动 HTTPS。

### 3.3 鸿蒙（HarmonyOS 手机 / 平板 / 鸿蒙工控板）

1. 用 **华为浏览器** 打开地址
2. 菜单 → **「添加至桌面」**
3. 鸿蒙 Next / 鸿蒙 4 浏览器支持 service worker，可离线启动
4. 鸿蒙工控板（如华为 Atlas 500、工控屏）同样可用

如果要做成鸿蒙原生元服务（ArkTS），需要把前端用 ArkWeb（鸿蒙 WebView）包一层——这属于二次开发，不在本部署包范围。

---

## 4. Docker 多架构一键部署（推荐生产）

```bash
# 在任意 x86_64 开发机上构建多架构镜像（需要 qemu + buildx）
docker buildx create --use --name multiarch
docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t <你的镜像仓库>/universal-system:v1.0.0 \
  --push ./deploy

# 目标机器上运行（不管是 x86 云、ARM 工控板、还是树莓派）
docker run -d --restart=always -p 8080:80 --name universal-system \
  <你的镜像仓库>/universal-system:v1.0.0
```

`caddy:2-alpine` 官方镜像同时提供 amd64 / arm64 / arm/v7，所以上面这一条 `docker run` 在所有架构上都能跑。

---

## 5. 部署架构图

```
                         ┌──────────────────────────────┐
                         │   全宇宙恒等系统 (PWA)        │
                         └──────────────┬───────────────┘
                                         │
        ┌────────────────────┬──────────┼──────────┬────────────────┐
        ▼                    ▼          ▼          ▼                ▼
  ┌──────────┐       ┌──────────┐ ┌─────────┐ ┌──────────┐  ┌──────────┐
  │ 云 x86    │       │ ARM 云   │ │ 树莓派 / │ │ Android  │  │ iOS /  鸿蒙│
  │ /阿里云   │       │ 鲲鹏/倚天│ │ RK3588  │ │ Chrome   │  │ Safari  │
  │ /AWS     │       │          │ │ 工控板   │ │ PWA 安装 │  │ PWA 安装 │
  └─────┬────┘       └────┬─────┘ └────┬────┘ └────┬─────┘  └────┬─────┘
        │                 │            │           │             │
        └─────────────────┴─────┬──────┴───────────┴─────────────┘
                                 │
                    同源静态资源 (index.html / assets / icons)
                                 │
                                 ▼
                    后端 API: universal-pay-backend.onrender.com
                    (经济 / 太阳风暴 / 复活 / 天气 / 空气)
```

---

## 6. 验证清单（部署后逐项检查）

> 部署脚本已自动跑前 5 项。**不要用"模拟太阳风暴"按钮来验证部署**——那是业务功能，验证部署只需确认 HTTP 200 与静态资源可达。

- [x] `http://<地址>/` 返回 200，页面有星空背景和启动动画
- [x] `/manifest.json` 返回 200（`Content-Type: application/manifest+json`）
- [x] `/sw.js` 返回 200
- [x] `/assets/qrcode.min.js`、`/assets/JsBarcode.all.min.js` 返回 200
- [x] `/icons/icon-192.png` 等图标返回 200
- [ ] Chrome DevTools → Application → Manifest 显示"Installed"
- [ ] Chrome DevTools → Application → Service Workers 显示 "activated and is running"
- [ ] 移动端浏览器"添加到主屏幕"后，桌面有独立图标
- [ ] 断网后刷新页面仍能打开核心 UI（PWA 离线生效）

---

## 7. 把后端也搬走（可选）

原后端在 `universal-pay-backend.onrender.com`。要实现"全宇宙私有部署"，需要把后端源码也部署到你自己的服务器：

1. **Node.js/Python 后端**：同样用 §4 的 Dockerfile 思路，多架构 buildx 出 arm64 镜像
2. **改前端 API 地址**：把 `index.html` 里所有 `universal-pay-backend.onrender.com` 替换成你自己的后端域名
3. **数据库**：后端依赖的 Redis/SQLite/PostgreSQL 容器化部署，ARM 版本用 `arm64v8/redis` 等官方多架构镜像

这一步需要后端源码，不在本次部署包内。

---

## 8. 文件清单

```
deploy/
├── index.html              # 主应用 (CDN 已本地化 + SW 注册)
├── manifest.json           # PWA 清单
├── sw.js                   # Service Worker
├── Caddyfile               # Caddy 静态配置
├── Dockerfile               # 多架构镜像定义
├── deploy.sh                # ARM/x86 一键部署脚本
├── favicon.ico / 16 / 32  # 站点图标
├── assets/
│   ├── qrcode.min.js
│   └── JsBarcode.all.min.js
└── icons/
    ├── icon-192.png
    ├── icon-512.png
    ├── icon-maskable-512.png
    └── apple-touch-icon.png
```

— 全宇宙恒等系统 · 跨平台部署手册 v1.0.0 —
