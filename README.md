# WinOptimizer - Windows System Optimization Tool

A comprehensive Windows system optimization tool built with Python + PySide6.

## Features

### 1. System Optimization
- 151 registry optimization items across 7 categories
- Appearance/Explorer optimization
- Performance optimization settings
- Security settings
- Edge browser optimization
- System settings
- Windows Update settings
- Privacy settings
- Basic/Deep optimization presets

### 2. System Cleanup
- Cache file cleanup (8 items)
- System file cleanup (6 items)
- Temporary file cleanup (7 items)

### 3. Office Management
- Online Office installation (supports 365/2024/2021/2019 versions)
- Uninstall Office (C2R version)

### 4. System Activation
- Windows system activation (MAS tool)

### 5. Appx Management
- Dynamic loading of UWP application list
- Batch uninstall of UWP applications

### 6. Security Center
- Windows Defender disable/enable
- Edge browser component management (Edge/WebView/Core uninstall)

### 7. Config Management
- Registry optimization backup & restore
- Configuration backup management

### 8. Settings
- Multi-language support: Chinese / English / Spanish
- Administrator privilege management
- Auto-backup registry before optimization

## Project Structure

```
WinOptimizer/
├── main.py                    # Entry point (admin elevation + first-run config)
├── config.json                # Default configuration
├── requirements.txt           # Dependencies
├── WinOptimizer.spec          # PyInstaller spec file
├── erweima/                   # QR code images for donation
├── README.md                  # English documentation
├── README-CN.md               # Chinese documentation
└── src/
    ├── __init__.py
    ├── core/                  # Core modules
    │   ├── __init__.py
    │   ├── optimizer.py       # Optimization engine (151 registry items)
    │   ├── cleaner.py         # Cleanup engine (21 commands)
    │   ├── services_manager.py # Service manager
    │   ├── activator.py       # Activation module
    │   ├── config_manager.py  # Config manager
    │   └── uwp_manager.py     # UWP app manager
    ├── i18n/                  # Internationalization
    │   ├── __init__.py        # Translation engine
    │   ├── zh.json            # Chinese translations
    │   ├── en.json            # English translations
    │   └── es.json            # Spanish translations
    ├── ui/                    # UI modules
    │   ├── __init__.py
    │   ├── main_window.py     # Main window (12-item sidebar navigation)
    │   └── pages/             # Feature pages
    │       ├── home_page.py          # Home
    │       ├── optimization_page.py  # System Optimization
    │       ├── cleanup_page.py       # System Cleanup
    │       ├── office_page.py        # Office Management
    │       ├── activation_page.py    # System Activation
    │       ├── appx_page.py          # Appx Management
    │       ├── defender_page.py      # Security Center
    │       ├── edge_page.py          # Edge Management
    │       ├── backup_page.py        # Restore Options
    │       ├── faq_page.py           # FAQ
    │       ├── settings_page.py      # Settings
    │       └── about_page.py         # About
    └── utils/                 # Utility functions
        ├── __init__.py
        ├── system_utils.py    # System utilities
        └── registry_utils.py  # Registry utilities
```

## Installation & Running

### 1. Install Dependencies

```bash
cd WinOptimizer
pip install -r requirements.txt
```

### 2. Run (requires administrator privileges)

```bash
python main.py
```

The program will automatically detect privileges and prompt for UAC elevation if not running as administrator.

### 3. Build EXE

```bash
pyinstaller --onefile --windowed --name WinOptimizer ^
    --add-data "config.json;." ^
    --add-data "erweima;erweima" ^
    --add-data "src/i18n/zh.json;src/i18n" ^
    --add-data "src/i18n/en.json;src/i18n" ^
    --add-data "src/i18n/es.json;src/i18n" ^
    main.py
```

The output will be at `dist/WinOptimizer.exe`.

## System Requirements

- Windows 10/11
- Python 3.8+
- PySide6 >= 6.8.0

## Configuration

Configuration is stored in `%APPDATA%/WinOptimizer/config.json`:

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

- **language**: Default "en" (English) on first run. Change via Settings page or editing config.
- **require_admin**: If true, auto-request UAC elevation on startup.
- **auto_backup_before_optimize**: Auto-create registry backup before optimization.

## Notes

1. Most features require administrator privileges
2. It is recommended to use "Restore" to back up the registry before optimization
3. The activation feature requires an internet connection
4. Language changes take effect on next launch

## Author

- **lorime**
- Email: lorime@126.com

## Donation Support

If you find this tool helpful, please consider supporting development:

- **XMR**: `4DSQMNzzq46N1z2pZWAVdeA6JvUL9TCB2bnBiA3ZzoqEdYJnMydt5akCa3vtmapeDsbVKGPFdNkzzqTcJS8M8oyK7WGj5qMvNZRw61w6wMF`
- **USDT (TRC20)**: `TG6DCBoQszDxc64owRZKkSHqZfcAQrqR8uM`
- **USDT (ERC20)**: `0x4323d39BA9b6Bd0570920e63a8D3a192b4459330`

## License

MIT License