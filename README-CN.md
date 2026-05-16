# WinOptimizer - Windows 系统优化工具

基于 Python + PySide6 开发的综合 Windows 系统优化工具。

## 功能特性

### 1. 系统优化
- 151项注册表优化设置，涵盖7大分类
- 外观/资源管理器优化
- 性能优化设置
- 安全设置
- Edge浏览器优化
- 系统设置
- Windows更新设置
- 隐私设置
- 基础/深度优化预设

### 2. 垃圾清理
- 缓存文件清理（8项）
- 系统文件清理（6项）
- 临时文件清理（7项）

### 3. Office管理
- 在线安装 Office（支持365/2024/2021/2019版本）
- 卸载 Office（C2R版本）

### 4. 系统激活
- Windows 系统激活（MAS工具）

### 5. Appx管理
- 动态加载UWP应用列表
- 批量卸载UWP应用

### 6. 安全中心
- Windows Defender 禁用/启用
- Edge浏览器组件管理（Edge/WebView/Core卸载）

### 7. 配置管理
- 注册表优化备份与还原
- 配置备份管理

### 8. 设置
- 多语言支持：中文 / 英文 / 西班牙文
- 管理员权限管理
- 优化前自动备份注册表

## 项目结构

```
WinOptimizer/
├── main.py                    # 主程序入口（管理员提权 + 首次运行配置）
├── config.json                # 默认配置文件
├── requirements.txt           # 依赖文件
├── WinOptimizer.spec          # PyInstaller 打包配置文件
├── erweima/                   # 捐赠二维码图片目录
├── README.md                  # 英文说明书
├── README-CN.md               # 中文说明书
└── src/
    ├── __init__.py
    ├── core/                  # 核心功能模块
    │   ├── __init__.py
    │   ├── optimizer.py       # 优化引擎（151项注册表优化）
    │   ├── cleaner.py         # 清理引擎（21条清理命令）
    │   ├── services_manager.py # 服务管理器
    │   ├── activator.py       # 激活器
    │   ├── config_manager.py  # 配置管理器
    │   └── uwp_manager.py     # UWP应用管理
    ├── i18n/                  # 国际化模块
    │   ├── __init__.py        # 翻译引擎
    │   ├── zh.json            # 中文翻译
    │   ├── en.json            # 英文翻译
    │   └── es.json            # 西班牙文翻译
    ├── ui/                    # UI界面模块
    │   ├── __init__.py
    │   ├── main_window.py     # 主窗口（12项侧边栏导航）
    │   └── pages/             # 功能页面
    │       ├── home_page.py          # 主页
    │       ├── optimization_page.py  # 系统优化
    │       ├── cleanup_page.py       # 垃圾清理
    │       ├── office_page.py        # Office管理
    │       ├── activation_page.py    # 系统激活
    │       ├── appx_page.py          # Appx管理
    │       ├── defender_page.py      # 安全中心
    │       ├── edge_page.py          # Edge管理
    │       ├── backup_page.py        # 还原选项
    │       ├── faq_page.py           # 疑难解答
    │       ├── settings_page.py      # 设置
    │       └── about_page.py         # 关于软件
    └── utils/                 # 工具函数
        ├── __init__.py
        ├── system_utils.py    # 系统工具
        └── registry_utils.py  # 注册表工具
```

## 安装与运行

### 1. 安装依赖

```bash
cd WinOptimizer
pip install -r requirements.txt
```

### 2. 运行程序（需要管理员权限）

```bash
python main.py
```

程序会自动检测权限，若非管理员运行会弹出 UAC 提权对话框。

### 3. 打包为 EXE

```bash
pyinstaller --onefile --windowed --name WinOptimizer ^
    --add-data "config.json;." ^
    --add-data "erweima;erweima" ^
    --add-data "src/i18n/zh.json;src/i18n" ^
    --add-data "src/i18n/en.json;src/i18n" ^
    --add-data "src/i18n/es.json;src/i18n" ^
    main.py
```

打包后的文件位于 `dist/WinOptimizer.exe`。

## 系统要求

- Windows 10/11
- Python 3.8+
- PySide6 >= 6.8.0

## 配置文件

配置文件存储在 `%APPDATA%/WinOptimizer/config.json`：

```json
{
    "app": {
        "name": "WinOptimizer",
        "version": "1.0.0",
        "author": "lorime",
        "email": "lorime@126.com"
    },
    "language": "en",
    "languages": ["zh", "en", "es"],
    "settings": {
        "require_admin": true,
        "auto_backup_before_optimize": true
    }
}
```

- **language**：首次运行默认为 "en"（英文），可通过设置页面或编辑配置文件修改
- **require_admin**：设为 true 时，启动自动请求 UAC 提权
- **auto_backup_before_optimize**：设为 true 时，优化前自动备份注册表

## 注意事项

1. 大多数功能需要管理员权限才能运行
2. 优化前建议使用"还原选项"备份注册表
3. 激活功能需要联网才能使用
4. 语言更改将在下次启动时生效

## 作者

- **lorime**
- 邮箱：lorime@126.com

## 捐献支持

如果您觉得这个工具对您有帮助，欢迎通过以下方式捐献支持开发：

- **XMR**：`4DSQMNzzq46N1z2pZWAVdeA6JvUL9TCB2bnBiA3ZzoqEdYJnMydt5akCa3vtmapeDsbVKGPFdNkzzqTcJS8M8oyK7WGj5qMvNZRw61w6wMF`
- **USDT (TRC20)**：`TG6DCBoQszDxc64owRZKkSHqZfcAQrqR8uM`
- **USDT (ERC20)**：`0x4323d39BA9b6Bd0570920e63a8D3a192b4459330`

## 许可证

MIT License