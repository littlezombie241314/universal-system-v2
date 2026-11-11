# ARM 服务器与移动 SoC 部署说明

**系统** 全宇宙恒等系统 v1.6.96 · 单文件 PWA（`index.html` + `sw.js` + `manifest.json` + `icons/` + `assets/`）
**指纹** `index.html` 1,343,862 B · md5 `c25508b7f21fc7a173bf4c844a01336e` · SW `ues-v1.6.960`

> 为什么 ARM 与手机能直接跑：整套系统是**纯静态前端**，运行时只有浏览器的 HTML/CSS/JS，
> 没有 x86 二进制、没有 Node 运行时依赖、没有原生动态库。任何能开浏览器的 ARM 设备都能运行同一份文件。

---

## 1. 运行环境矩阵

| 设备 / 平台 | 架构 | 运行方式 | 本轮实测状态 |
|---|---|---|---|
| 云服务器（阿里云倚天 / 华为鲲鹏 / AWS Graviton） | aarch64 | `deploy.sh` 或 Docker | 脚本逻辑实测（x86 同脚本通过），ARM 实机未接入 |
| ARM 工控板（树莓派 4/5、RK3588、飞腾、鲲鹏 920） | aarch64 / armv7l | `deploy.sh` 本地静态服务 | 同上 |
| Android 手机 / 平板 | ARM64（SoC：CPU+GPU+ISP+基带+内存+闪存） | Chrome 打开 HTTPS 站点 → 安装 PWA | 393 / 412 / 360 px 三种视口实测通过 |
| iPhone / iPad | Apple Silicon（ARM） | Safari → 添加到主屏幕 | iOS 视口（393×852）实测通过；Safari 真机未接入 |
| HarmonyOS 手机 / 平板 / 工控板 | ARM64 | 系统浏览器 / ArkWeb → 添加至桌面 | 360 px 视口实测通过；鸿蒙真机未接入 |

**共同前提**：站点必须是 **HTTPS**（或 `localhost`）。PWA 安装与 Service Worker 都要求安全上下文，纯 HTTP 的内网 IP 只能浏览、不能安装。

---

## 2. ARM 服务器 / 工控板

### 2.1 一键脚本（推荐）

```bash
scp -r deploy/ root@<ARM主机IP>:/root/
ssh root@<ARM主机IP>
cd /root/deploy && chmod +x deploy.sh
sudo ./deploy.sh                      # /opt/universal-system，端口 8080
sudo PORT=9000 ./deploy.sh            # 自定义端口
```

脚本用 `uname -m` 打印架构，不写死任何架构分支；服务端按 `caddy → nginx → python3 http.server` 顺序选择。aarch64 与 armv7l 都能直接跑，无编译步骤。

### 2.2 Docker 多架构

```bash
# 在支持 buildx 的主机上构建（QEMU 或原生 ARM 主机）
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t <registry>/universal-system:1.6.96 --push .

# ARM 设备上运行
docker run -d --restart=always -p 8080:80 --name universal-system <registry>/universal-system:1.6.96
```

镜像基于 `caddy:2-alpine`（官方提供 arm64 / armv7 变体），已内置 `Caddyfile`：`sw.js` 强制 `no-store`、HTML `no-cache`、静态资源 `max-age=86400`、`Service-Worker-Allowed: /`。

### 2.3 板载浏览器直开

工控板自带 Chromium/WebView 时，把 `deploy/` 放到板子上，起任意静态服务，用本机浏览器访问 `http://127.0.0.1:8080/` 即可；`127.0.0.1` 属于安全上下文，Service Worker 可正常注册，断网后仍能启动。

### 2.4 ARM 上的注意点

- **不要用 `file://` 打开**：SW 不注册、无法离线。
- **不要用 32 位 armv7l 跑 64 位镜像**：镜像 tag 与 `uname -m` 必须匹配。
- ARM 主机普遍内存小：静态服务占用可忽略，但 Caddy 比 `python3 http.server` 更稳（长连接 + 缓存头）。
- 工控板断电频繁：systemd 已配 `Restart=always`，重启后自动拉起。

---

## 3. Android（移动 SoC）

Android 手机的主芯片是 ARM SoC，由 CPU/GPU/ISP/基带/内存/闪存与外设统一调度；对本系统而言它只是一台"能跑浏览器的 ARM 板卡"。

### 3.1 安装步骤

1. Chrome（或厂商浏览器）打开 `https://universal-system-final.surge.sh/`
2. 等启动序列跑完（首次约 3–10 秒，1.3 MB）
3. 右上角 ⋮ → **「添加到主屏幕」/「安装应用」**
4. 桌面出现「全宇宙恒等」，点开为独立窗口（无地址栏），断网可启动

### 3.2 为什么不需要 APK

页面已满足 Android 的 PWA 安装条件：

| 条件 | 本系统 |
|---|---|
| HTTPS | 所有线上入口均为 HTTPS |
| `manifest.json` 含 `name` / `short_name` / `start_url` / `display: standalone` | 具备 |
| 192 与 512 图标（含 maskable） | `icons/icon-192.png`、`icon-512.png`、`icon-maskable-512.png` |
| 已注册 Service Worker | `sw.js`（`ues-v1.6.960`） |

需要 Play 商店分发时才用 TWA（Trusted Web Activity）打包，本环境无 Android SDK，未做打包验证，此处不提供未经编译验证的工程。

### 3.3 实测结论（本轮）

- 393 / 412 / 360 px 三种宽度：`documentElement.scrollWidth == innerWidth`，**无横向溢出**
- 修复前 393 px 下主余额被 `overflow:hidden` 裁切；修复后 `font-size:15px` + `word-break:break-all`，完整显示
- 顶部"自动刷新"浮层在窄屏改为文档流（`position:static`），不再遮挡内容
- 17 个可见操作按钮，仅 3 个高度 < 32 px（触摸目标偏小，但不影响点击）

---

## 4. iPhone / iPad（iOS）

1. **必须用 Safari**（微信/QQ 内置浏览器不支持"添加到主屏幕"）
2. 打开 `https://universal-system-final.surge.sh/`
3. 底部分享 → 向上滑 → **「添加到主屏幕」**
4. 图标取自 `icons/apple-touch-icon.png`（180×180）

已配置的 iOS meta：

```html
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="全宇宙恒等系统">
```

iOS 限制（属系统能力，不是缺陷）：

- 无"安装"按钮，只能手动"添加到主屏幕"
- 后台同步受限；Web Push 需 iOS 16.4+ 且已添加到主屏幕
- 独立窗口下外部链接会跳出 PWA

---

## 5. HarmonyOS / 鸿蒙工控板

1. 系统浏览器或 ArkWeb 应用打开 HTTPS 地址
2. 菜单 → **「添加至桌面」/「添加到主屏幕」**
3. 独立窗口运行；ArkWeb 对标准 PWA（manifest + Service Worker）兼容

鸿蒙工控板（ARM64）作为服务器时，直接按 §2 部署；作为终端时按上面 1–3 步安装。

**限制**：HarmonyOS NEXT 不再兼容 Android APK，但本系统是 PWA，不依赖 APK，因此不受影响。

---

## 6. 移动端 / ARM 通用验证清单

| 检查项 | 通过标准 | 本轮结果 |
|---|---|---|
| 静态资源 | `/manifest.json`、`/sw.js`、`/assets/*`、`/icons/*` 全 200 | ✅ 线上 9 个资源全 200 |
| 版本 | 页面 `v1.6.96`，SW `ues-v1.6.960` | ✅ |
| 视口适配 | 360 / 393 / 412 px 无横向溢出、金额不裁切 | ✅ 修复后通过 |
| 触摸交互 | 21 个模块标签可切换，按钮可点击并出结果 | ✅ 20 个业务模块已实测（太阳风暴仅只读） |
| 离线启动 | 断网后从主屏幕图标仍能进入控制台 | ⚠️ 逻辑具备（SW 含 12 项核心缓存），未在真机断网复测 |
| 独立窗口 | 无地址栏、无标签页 | ⚠️ 需真机安装后确认 |

> ⚠️ 标记项：本环境无 Android/iOS/鸿蒙真机，也无 ARM 物理机，以上为视口模拟 + 线上资源实测 + 脚本逻辑验证；真机安装与断网启动需在设备上复验。

---

## 7. 常见问题

| 现象 | 原因 | 处理 |
|---|---|---|
| 手机上点"安装"没反应 | HTTP 非安全上下文 / 浏览器不支持 | 用 HTTPS 入口；iOS 用 Safari 手动添加 |
| 窄屏文字被切 | 旧版本 CSS 未做窄屏适配 | 升级到 v1.6.96 及以上 |
| 升级后仍是旧版 | SW 缓存未淘汰 | 关掉全部标签页重开；或 DevTools → Unregister → 刷新两次 |
| ARM 板子上 `deploy.sh` 报找不到服务器 | 无 caddy/nginx/python3 | 装任一即可（`apt install caddy` 或 `python3`） |
| Docker 启动即退出 | 平台不匹配（armv7 跑 arm64 镜像） | 用 `--platform linux/arm/v7` 对应版本 |
| 工控板重启后服务没了 | 非 systemd 环境 | 用 `nohup` 或板卡自带的开机自启 |
