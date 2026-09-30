# 全宇宙恒等系统 · 安装说明

**版本** v∞ · UNIVERSAL EQUALITY SYSTEM  
**更新日期** 2026-09-30  
**最新版本标识** md5 `beef168c`（814,143 字节）  
**适用设备** 手机（Android / iOS / 鸿蒙）· 平板 · 电脑 · 云服务器 · ARM 工控板 · 边缘节点

---

## 目录

- [一、安装链接（直接打开即用）](#一安装链接直接打开即用)
- [二、手机 / 平板安装为 App（PWA）](#二手机--平板安装为-apppwa)
- [三、工控板 / 云服务器部署](#三工控板--云服务器部署)
- [四、边缘节点 / Serverless 部署](#四边缘节点--serverless-部署)
- [五、安装后验证](#五安装后验证)
- [六、防网络抖动部署脚本](#六防网络抖动部署脚本)
- [七、常见问题](#七常见问题)

---

## 一、安装链接（直接打开即用）

> 无需安装任何软件：**把链接复制到浏览器地址栏打开**，等待启动序列跑完即进入控制台。

| 环境 | 安装链接 | 说明 |
|---|---|---|
| **⭐ 推荐 · 官方最新版** | **https://universal-system-final.surge.sh/** | 全球 CDN，秒开，优先使用 |
| **GitHub Pages** | https://littlezombie241314.github.io/universal-system-v2/ | GitHub 全球 CDN |
| **doubaoapps 应用版** | https://xb4r414nb9.doubaoapps.com/app/app_17f4htz1kfy | 可安装为 App 的应用版 |
| **Cloudflare Workers** | https://universal-equality.universal-equality.workers.dev/ | 全球边缘节点（部分地区需科学上网） |
| 备用域名 1 | https://universal-system-latest.surge.sh/ | 与官方版同步 |
| 备用域名 2 | https://universal-system.surge.sh/ | 与官方版同步 |
| 备用域名 3 | https://universal-system-deploy.surge.sh/ | 与官方版同步 |
| 备用域名 4 | https://universal-equality.surge.sh/ | 与官方版同步 |
| 本地 / 内网 | `http://<服务器IP>:8080/` | 自部署后使用 |

> 以上链接内容完全一致（同一最新版本），任意一个打不开就换下一个。
> 首次打开后核心资源会被缓存，之后**离线也能启动**。

---

## 二、手机 / 平板安装为 App（PWA）

系统支持 **PWA（渐进式 Web 应用）**：安装后像原生 App 一样有桌面图标、独立窗口、可离线使用。

### Android（Chrome 浏览器）

1. 打开 https://universal-system-final.surge.sh/
2. 点击浏览器右上角 **⋮ 菜单**
3. 选择 **"添加到主屏幕"** 或 **"安装应用"**
4. 桌面出现"全宇宙恒等系统"图标，点开即用

### iOS / iPhone（Safari 浏览器）

1. 打开 https://universal-system-final.surge.sh/
2. 点击底部 **分享按钮**（方框向上箭头）
3. 选择 **"添加到主屏幕"**
4. 点击右上角 **"添加"**，桌面出现图标

### 鸿蒙 HarmonyOS（浏览器）

1. 打开 https://universal-system-final.surge.sh/
2. 浏览器菜单 → **"添加至桌面"** / **"创建快捷方式"**
3. 桌面生成图标，点开即用

### 电脑（Chrome / Edge）

1. 打开 https://universal-system-final.surge.sh/
2. 地址栏右侧出现 **安装图标**（显示器+箭头）
3. 点击 → **"安装"**，独立窗口运行

> 安装后：独立窗口（无浏览器地址栏）、离线可启动、图标一键打开。

---

## 三、工控板 / 云服务器部署

系统支持 **x86_64 / ARM（aarch64 / armv7）/ 龙芯 / MIPS** 全架构，一个命令部署到本机。

### 3.1 一键部署（推荐）

```bash
# 1. 获取源码（任选其一）
git clone https://github.com/littlezombie241314/universal-system-v2.git
# 或下载 deploy/ 目录中的文件

# 2. 部署（默认端口 8080）
cd universal-system-v2/deploy
chmod +x deploy.sh
sudo ./deploy.sh            # 部署到 /opt/universal-system，端口 8080

# 自定义端口
PORT=9000 ./deploy.sh       # 非 root 时自动装到 ~/universal-system
```

部署完成后访问：`http://<服务器IP>:8080/`

### 3.2 Docker 部署（多架构镜像）

```bash
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t universal-system .
docker run -d -p 8080:80 --name universal-system universal-system
```

### 3.3 ARM 工控板专用说明

支持：树莓派 3/4/5 · 瑞芯微 RK3588 · 飞腾 2000 · 鲲鹏 920 · 华为云鲲鹏 · 各类安卓/鸿蒙工控板

```bash
# ARM 板安装 Caddy（轻量 Web 服务器）
sudo apt install caddy
# 部署
sudo ./deploy.sh
# 访问 http://<板子IP>:8080/
```

### 3.4 Android / 鸿蒙工控板（嵌入式板卡）

工控板跑 Android / 鸿蒙系统时，两种方式任选：

| 方式 | 操作 |
|---|---|
| **浏览器访问**（最简单） | 板载浏览器打开 https://universal-system-final.surge.sh/ 即可运行 |
| **本地部署**（离线运行） | 用 ADB / 文件管理器把 deploy/ 文件拷入板卡，用任意静态服务器（如 `python3 -m http.server 8080`）运行后访问 `http://127.0.0.1:8080/` |

---

## 四、边缘节点 / Serverless 部署

### 4.1 Cloudflare Workers（全球边缘节点，推荐）

```bash
# 1. 进入 worker 目录（源码在 GitHub 仓库 worker/ 目录）
cd universal-system-v2/worker

# 2. 配置 wrangler.toml（已内置 KV 绑定）
# 3. 部署
export CLOUDFLARE_API_TOKEN=<你的Cloudflare API Token>
wrangler deploy
# 输出: https://universal-equality.universal-equality.workers.dev
```

### 4.2 Surge（静态托管）

```bash
npx surge ./deploy
# 按提示登录后输入域名，如 universal-system-final.surge.sh
```

### 4.3 其他平台

| 平台 | 命令 |
|---|---|
| Vercel | `npx vercel deploy ./deploy` |
| Netlify | `npx netlify deploy --dir=deploy --prod` |
| GitHub Pages | 推送到 `gh-pages` 分支（自动生效） |
| EdgeOne Pages | 通过 Makers 一键部署 HTML |

---

## 五、安装后验证

安装 / 打开后，按下面清单确认系统正常：

| 检查项 | 预期结果 |
|---|---|
| 启动序列 | BIOS → NET → BOOT 全部 OK |
| 顶部大数字 | 显示全宇宙统一余额 |
| 18 个模块 Tab | 大气净化 / 无限经济 / 全宇宙通信 / 全宇宙互联网 / 长生不老 / 气候控制 / 资源再生 / 生态守护 / 居住空间 / 星际旅行 / 人品系统 / 太阳风暴 / 连理婚姻 / 全知教育 / 全能医疗 / 娱乐体验 / AI共生 / 精神哲学 |
| 🌦️ 气候模块 | 默认"☀️ 晴天（最优）"；节假日自动锁定晴天不可修改 |
| 📡 通信模块 | 显示"⚡ 自动选择最快网速系统"，每秒自动优选最快通道 |
| ☀️ 太阳风暴 | 面板正常显示"无耀斑"状态即可（**只做资源可达性检查，勿触发模拟**） |
| 离线启动 | 断网后重新打开仍可启动（Service Worker 已缓存） |

---

## 六、防网络抖动部署脚本

仓库内附带 `deploy_stable.sh` —— 全平台部署脚本，内置**自动重试 / 指数退避 / 部署后强制校验 / 直连绕过代理缓存**，网络抖动时自动重试不中断。

```bash
./deploy_stable.sh                # 部署全部平台（Surge×5 + GitHub + doubaoapps + Cloudflare）并验证
./deploy_stable.sh --surge        # 只部署 Surge×5
./deploy_stable.sh --github       # 只推送 GitHub
./deploy_stable.sh --doubaoapps   # 只发布 doubaoapps
./deploy_stable.sh --cloudflare   # 只更新 Cloudflare Workers
./deploy_stable.sh --verify       # 只做全平台验证
```

---

## 七、常见问题

| 问题 | 解决 |
|---|---|
| 打开显示旧版内容 | 强制刷新：`Ctrl+Shift+R`（电脑）/ 清浏览器缓存（手机）；或换备用域名打开 |
| 某个链接打不开 | 换用其他备用链接（内容完全一致） |
| 工控板打不开（x86/ARM 兼容） | 确认用浏览器访问而非原生应用；本地部署用 `deploy.sh` |
| 离线打不开 | 首次需联网加载一次，之后自动缓存可离线 |
| workers.dev 打不开 | 部分地区网络受限，改用 Surge / GitHub Pages 链接 |
| 部署中断/网络抖动 | 用 `./deploy_stable.sh`，自动重试直到成功 |
