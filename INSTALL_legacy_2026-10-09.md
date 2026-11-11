# 全宇宙恒等系统 · 全平台 / 全端安装教程

**版本** v∞ · UNIVERSAL EQUALITY SYSTEM  
**更新日期** 2026-10-09  
**最新版本标识** md5 `6b4e2a50`（814,970 字节）+ Service Worker v1.3.0  
**数据驱动** 宇宙恒等系统数据驱动（复活 / 气候 / 经济 / 太阳风暴 / 工资 / 覆盖众生均由系统自身持久化驱动，不依赖外部后端，持久化即同步）  
**适用设备** 手机（Android / iPhone / 鸿蒙）· 平板 · 电脑（Windows / Mac / Linux）· 云服务器（x86 / ARM）· 工控板 · 边缘节点

---

## 目录

- [〇、总览：每个平台 / 端的安装方式](#〇总览每个平台--端的安装方式)
- [一、直接打开使用（所有端通用）](#一直接打开使用所有端通用)
- [二、手机安装为 App](#二手机安装为-app)
- [三、平板安装为 App](#三平板安装为-app)
- [四、电脑端安装（Windows / Mac / Linux）](#四电脑端安装windows--mac--linux)
- [五、云服务器部署（x86 / ARM 云主机）](#五云服务器部署x86--arm-云主机)
- [六、ARM 工控板 / 嵌入式部署](#六arm-工控板--嵌入式部署)
- [七、边缘节点 / Serverless 部署](#七边缘节点--serverless-部署)
- [八、安装后验证清单](#八安装后验证清单)
- [九、防网络抖动部署脚本](#九防网络抖动部署脚本)
- [十、常见问题（FAQ）](#十常见问题faq)

---

## 〇、总览：每个平台 / 端的安装方式

| 端 / 平台 | 安装方式 | 安装地址 |
|---|---|---|
| 📱 Android 手机 | 浏览器打开 → 添加到主屏幕（PWA） | `https://universal-system-final.surge.sh/` |
| 🍎 iPhone / iPad | Safari 打开 → 添加到主屏幕（PWA） | `https://universal-system-final.surge.sh/` |
| 🔷 鸿蒙 HarmonyOS 手机/平板 | 浏览器打开 → 添加至桌面 | `https://universal-system-final.surge.sh/` |
| 💻 电脑 Windows / Mac / Linux | Chrome / Edge 安装应用（PWA） | `https://universal-system-final.surge.sh/` |
| 🖥️ 云服务器（x86 / ARM） | 下载源码 → 一键部署脚本 / Docker | `git clone` GitHub 仓库 |
| 🧩 ARM 工控板（树莓派 / RK3588 / 飞腾 / 鲲鹏） | 浏览器访问 或 本地静态部署 | 板载浏览器或 `deploy.sh` |
| 🌐 边缘节点（Cloudflare Workers） | `wrangler deploy` | `https://universal-equality.universal-equality.workers.dev/` |
| 📱 doubaoapps 应用版 | 打开链接直接运行（可安装） | `https://xb4r414nb9.doubaoapps.com/app/app_17f4htz1kfy/` |
| 🐙 GitHub Pages | 自动重定向到官方最新版 | `https://littlezombie241314.github.io/universal-system-v2/` |

**所有平台的页面内容完全一致（同一最新版 `6b4e2a50`）**，任意一个打不开就换下一个。首次打开后核心资源被缓存，**之后断网也能启动**。

---

## 一、直接打开使用（所有端通用）

> 最简单的方式：**把链接复制到浏览器地址栏打开**，等待启动序列（BIOS → NET → BOOT）跑完即进入控制台。无需安装任何软件。

| 环境 | 安装链接 | 说明 |
|---|---|---|
| **⭐ 推荐 · 官方最新版** | **https://universal-system-final.surge.sh/** | 全球 CDN，秒开，优先使用 |
| **备用域名 1** | https://universal-system-latest.surge.sh/ | 与官方版同步 |
| **备用域名 2** | https://universal-system.surge.sh/ | 与官方版同步 |
| **备用域名 3** | https://universal-system-deploy.surge.sh/ | 与官方版同步 |
| **备用域名 4** | https://universal-equality.surge.sh/ | 与官方版同步 |
| **doubaoapps 应用版** | https://xb4r414nb9.doubaoapps.com/app/app_17f4htz1kfy/ | 可安装为 App |
| **Cloudflare Workers** | https://universal-equality.universal-equality.workers.dev/ | 全球边缘节点 |
| **GitHub Pages** | https://littlezombie241314.github.io/universal-system-v2/ | 自动重定向到官方版 |
| 本地 / 内网 | `http://<服务器IP>:8080/` | 自部署后使用 |

---

## 二、手机安装为 App

系统支持 **PWA（渐进式 Web 应用）**：安装后像原生 App 一样有**桌面图标、独立窗口、可离线使用**。

### 2.1 Android 手机（Chrome 浏览器）

1. 打开 **https://universal-system-final.surge.sh/**（用 Chrome 或自带浏览器）
2. 点击浏览器右上角 **⋮ 菜单**
3. 选择 **"添加到主屏幕"**（或 **"安装应用"**，Android 新版本）
4. 弹出确认框 → 点击 **"添加"**
5. 桌面出现 **"全宇宙恒等系统"** 图标，点开即用（独立窗口、无地址栏）

> 华为 / 荣耀自带浏览器：菜单 → "添加到桌面" / "创建快捷方式"，步骤相同。

### 2.2 iPhone / iPad（Safari 浏览器）

1. 打开 **https://universal-system-final.surge.sh/**（必须用 **Safari**，其他浏览器不支持安装）
2. 点击底部 **分享按钮**（方框+向上箭头）
3. 选择 **"添加到主屏幕"**
4. 预览名称保持"全宇宙恒等系统" → 点击右上角 **"添加"**
5. 桌面出现图标，点开即用（独立全屏窗口、可离线）

### 2.3 鸿蒙 HarmonyOS（华为手机 / 平板）

1. 打开 **https://universal-system-final.surge.sh/**（华为浏览器）
2. 浏览器菜单（右下角 **⋮**）→ **"添加至桌面"** / **"创建快捷方式"**
3. 桌面生成图标，点开即用

> 系统已内置 `manifest.json`（图标 / 名称 / 主题色），所有手机端安装后都显示**正确图标和名称**。

---

## 三、平板安装为 App

| 平板 | 操作（同手机） |
|---|---|
| Android 平板 | Chrome 打开 → ⋮ → 添加到主屏幕 |
| iPad | Safari 打开 → 分享 → 添加到主屏幕 |
| 鸿蒙平板 | 华为浏览器 → 添加至桌面 |

平板打开后为**自适应布局**，横屏 / 竖屏均可完整使用。

---

## 四、电脑端安装（Windows / Mac / Linux）

### 4.1 Chrome / Edge（Windows / Mac / Linux 通用）

1. 打开 **https://universal-system-final.surge.sh/**
2. 地址栏右侧出现 **安装图标**（显示器+箭头），点击
3. 选择 **"安装"** → 确认
4. 系统以**独立窗口**运行，开始菜单 / 桌面出现应用图标

### 4.2 手动安装

- Chrome：地址栏右侧 ⋮ → **"安装全宇宙恒等系统"**
- Edge：地址栏右侧 ⋮ → **"应用" → "安装此网站作为应用"**

> 电脑端安装后：独立窗口、无浏览器地址栏、离线可启动、任务栏一键打开。

---

## 五、云服务器部署（x86 / ARM 云主机）

> 适用于：阿里云 / 腾讯云 / 华为云 / AWS / GCP / 自建机房服务器，x86_64 或 ARM（aarch64）均可。

### 5.1 一键部署（推荐）

```bash
# 1. 获取源码
git clone https://github.com/littlezombie241314/universal-system-v2.git
# 或直接下载 deploy/ 目录中的文件

# 2. 部署（默认端口 8080）
cd universal-system-v2/deploy
chmod +x deploy.sh
sudo ./deploy.sh            # 部署到 /opt/universal-system，端口 8080

# 自定义端口
PORT=9000 ./deploy.sh       # 非 root 时自动装到 ~/universal-system
```

部署完成后访问：`http://<服务器IP>:8080/`（配置域名 + HTTPS 后即可公网使用）

### 5.2 Docker 部署（多架构镜像）

```bash
# 构建 x86_64 + ARM64 + ARMv7 三架构镜像
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t universal-system .
# 运行
docker run -d -p 8080:80 --name universal-system universal-system
```

### 5.3 手动部署（任意静态服务器）

```bash
# Python
python3 -m http.server 8080 --directory deploy

# Nginx / Caddy / 宝塔面板：把 deploy/ 目录设为站点根目录即可
```

---

## 六、ARM 工控板 / 嵌入式部署

> 支持：树莓派 3/4/5 · 瑞芯微 RK3588 · 飞腾 2000 · 鲲鹏 920 · 华为云鲲鹏 · 各类 Android / 鸿蒙工控板 · 边缘盒子。

### 6.1 运行 Android / 鸿蒙系统的工控板

| 方式 | 操作 |
|---|---|
| **浏览器访问**（最简单） | 板载浏览器打开 `https://universal-system-final.surge.sh/` 即可运行 |
| **PWA 安装** | 浏览器菜单 → 添加到主屏幕（工控板触摸屏一键启动） |
| **本地部署**（离线运行） | 用 ADB / 文件管理器把 `deploy/` 文件拷入板卡 → 运行 `python3 -m http.server 8080` → 访问 `http://127.0.0.1:8080/` |

### 6.2 运行 Linux 的 ARM 板（树莓派等）

```bash
# 安装 Caddy（轻量 Web 服务器）
sudo apt install caddy

# 部署
sudo ./deploy.sh

# 访问
http://<板子IP>:8080/
```

> 系统为**纯前端单页应用**，无编译依赖、无原生组件，ARM 任何架构（aarch64 / armv7）均直接运行。

---

## 七、边缘节点 / Serverless 部署

### 7.1 Cloudflare Workers（全球边缘节点，无冷启动）

```bash
# 1. 进入 worker 目录（源码在 GitHub 仓库 worker/ 目录）
cd universal-system-v2/worker

# 2. 部署（已内置 KV 绑定）
export CLOUDFLARE_API_TOKEN=<你的Cloudflare API Token>
wrangler deploy

# 输出: https://universal-equality.universal-equality.workers.dev
```

### 7.2 Surge（静态托管）

```bash
npx surge ./deploy
# 按提示登录后输入域名，如 universal-system-final.surge.sh
```

### 7.3 其他平台

| 平台 | 命令 |
|---|---|
| Vercel | `npx vercel deploy ./deploy` |
| Netlify | `npx netlify deploy --dir=deploy --prod` |
| GitHub Pages | 推送到 `gh-pages` 分支（自动生效，本仓库已配置 CNAME 重定向） |
| EdgeOne Pages | 通过 Makers 一键部署 HTML |
| doubaoapps | `lark-cli apps +deploy --dir ./deploy --app-id app_17f4htz1kfy` |

---

## 八、安装后验证清单

安装 / 打开后，按下面清单确认系统正常：

| 检查项 | 预期结果 |
|---|---|
| 启动序列 | BIOS → NET → BOOT 全部 OK |
| 顶部大数字 | 显示全宇宙统一余额 |
| 18 个模块 Tab | 大气净化 / 无限经济 / 全宇宙通信 / 全宇宙互联网 / 长生不老 / 气候控制 / 资源再生 / 生态守护 / 居住空间 / 星际旅行 / 人品系统 / 太阳风暴 / 连理婚姻 / 全知教育 / 全能医疗 / 娱乐体验 / AI共生 / 精神哲学 |
| 🧬 复活系统 | 显示 **"已同步云端"（绿色）**，数据由宇宙恒等系统持久化驱动 |
| 🌦️ 气候模块 | 默认"☀️ 晴天（最优）"，状态"已同步云端"；节假日自动锁定晴天不可修改 |
| 📡 通信模块 | 显示"⚡ 自动选择最快网速系统" |
| ☀️ 太阳风暴 | 面板正常显示"无耀斑"状态（**只做资源可达性检查，勿触发模拟**） |
| 💰 无限经济 | 账户余额实时显示，多账户同步取最大金额，实时保存 |
| 离线启动 | 断网后重新打开仍可启动（Service Worker v1.3.0 已缓存） |

---

## 九、防网络抖动部署脚本

仓库内附带 **`deploy_stable.sh`** —— 全平台部署脚本，内置**自动重试 / 指数退避 / 部署后强制校验 / 直连绕过代理缓存**，网络抖动时自动重试不中断。

```bash
./deploy_stable.sh                # 部署全部平台（Surge×5 + GitHub + doubaoapps + Cloudflare）并验证
./deploy_stable.sh --surge        # 只部署 Surge×5
./deploy_stable.sh --github       # 只推送 GitHub
./deploy_stable.sh --doubaoapps   # 只发布 doubaoapps
./deploy_stable.sh --cloudflare   # 只更新 Cloudflare Workers
./deploy_stable.sh --verify       # 只做全平台验证
```

---

## 十、常见问题（FAQ）

| 问题 | 解决 |
|---|---|
| 打开显示旧版内容 | **完全退出应用重新进入**（Service Worker v1.3.0 会自动清缓存）；电脑端按 `Ctrl+Shift+R` 强制刷新 |
| 某个链接打不开 | 换用其他备用链接（内容完全一致） |
| iPhone 添加不到主屏幕 | 确认用的是 **Safari**（Chrome 等浏览器不支持 iOS PWA 安装） |
| 安装后无图标 / 名称不对 | 确认访问的是最新版（含 `manifest.json`） |
| 工控板打不开 | 用**浏览器**访问（非原生应用）；本地部署用 `deploy.sh` |
| 显示"本地模式" | 新版已改为**宇宙恒等系统数据驱动**：数据由系统自身持久化，恒显"已同步云端"，不再出现"本地模式" |
| 想配外部后端 | 工资模块切"真实转账模式"后手动填 API 地址并"测试连接"（可选功能，默认系统数据驱动无需配置） |
