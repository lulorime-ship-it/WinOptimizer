import winreg
import os
import json
import subprocess
from datetime import datetime
from pathlib import Path
from ..utils.registry_utils import RegistryUtils
from ..utils.system_utils import SystemUtils

class OptimizationItem:
    def __init__(self, item_id, name, description, category, item_type, **kwargs):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.category = category
        self.item_type = item_type
        self.kwargs = kwargs


class Optimizer:
    CATEGORY_EXPLORER = "外观/资源管理器"
    CATEGORY_XINGNENG = "性能优化设置"
    CATEGORY_SAFE = "安全设置"
    CATEGORY_EDGE = "Edge优化设置"
    CATEGORY_SYSTEM = "系统设置"
    CATEGORY_UPDATE = "更新设置"
    CATEGORY_YINSI = "隐私设置"

    BACKUP_DIR = Path(os.environ.get("APPDATA", ".")) / "WinOptimizer" / "backups"

    def __init__(self):
        self._items = {}
        self._categories = {}
        self._build_items()

    def _add_item(self, item_id, name, description, category, item_type, **kwargs):
        item = OptimizationItem(item_id, name, description, category, item_type, **kwargs)
        self._items[item_id] = item
        if category not in self._categories:
            self._categories[category] = []
        self._categories[category].append(item)
        return item

    def _build_items(self):
        self._build_explorer_items()
        self._build_xingneng_items()
        self._build_safe_items()
        self._build_edge_items()
        self._build_system_items()
        self._build_update_items()
        self._build_yinsi_items()

    def _build_explorer_items(self):
        cat = self.CATEGORY_EXPLORER

        self._add_item("explorer_01", "隐藏任务栏搜索框",
                       "隐藏任务栏上的搜索框，释放任务栏空间",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Search",
                       value_name="SearchboxTaskbarMode", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("explorer_02", "隐藏\"任务视图\"按钮",
                       "隐藏任务栏上的任务视图按钮",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                       value_name="ShowTaskViewButton", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("explorer_03", "始终在任务栏显示所有图标和通知",
                       "在任务栏通知区域始终显示所有图标",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Explorer",
                       value_name="EnableAutoTray", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("explorer_04", "任务栏窗口被占满时合并",
                       "仅在任务栏被占满时才合并任务栏按钮",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                       value_name="TaskbarGlomLevel", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("explorer_05", "提高前台程序的显示速度",
                       "调整处理器优先级以提高前台程序响应速度",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SYSTEM\CurrentControlSet\Control\PriorityControl",
                       value_name="Win32PrioritySeparation", value_data=38,
                       value_type=winreg.REG_DWORD)

        self._add_item("explorer_06", "不要显示窗口出现和消失动画",
                       "关闭窗口最小化和还原时的动画效果",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Control Panel\Desktop\WindowMetrics",
                       value_name="MinAnimate", value_data="0",
                       value_type=winreg.REG_SZ)

        self._add_item("explorer_07", "使「开始」菜单、任务栏、操作中心透明",
                       "启用开始菜单、任务栏和操作中心的透明效果",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                       value_name="EnableTransparency", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("explorer_08", "打开资源管理器时显示此电脑",
                       "打开文件资源管理器时默认显示\"此电脑\"",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                       value_name="LaunchTo", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("explorer_09", "总是从内存中卸载无用的DLL",
                       "程序退出时自动从内存中卸载不再使用的DLL",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer",
                       value_name="AlwaysUnloadDLL", value_data="1",
                       value_type=winreg.REG_SZ)

        self._add_item("explorer_10", "记事本启用自动换行",
                       "记事本默认启用自动换行功能",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Notepad",
                       value_name="fWrap", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("explorer_11", "记事本始终显示状态栏",
                       "记事本始终显示底部的状态栏",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Notepad",
                       value_name="StatusBar", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("explorer_12", "禁止跟踪损坏的快捷方式",
                       "禁止Windows跟踪和修复损坏的快捷方式",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer",
                       value_name="NoResolveTrack", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("explorer_13", "优化Windows文件列表刷新策略",
                       "禁止资源管理器自动搜索网络资源，加快文件夹刷新速度",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                       value_name="NoNetCrawling", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("explorer_14", "显示已知文件类型的扩展名",
                       "显示所有文件的扩展名，包括已知文件类型",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                       value_name="HideFileExt", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("explorer_15", "不要保留\"最近打开的文件\"历史记录",
                       "不在开始菜单中显示最近打开的文件",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                       value_name="Start_TrackDocs", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("explorer_16", "退出时清除\"最近打开的文件\"历史记录",
                       "退出系统时自动清除最近打开的文件记录",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                       value_name="ClearRecentDocsOnExit", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("explorer_17", "创建快捷方式时不添加\"快捷方式\"字样",
                       "创建快捷方式时不在名称前添加\"快捷方式\"前缀",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Explorer",
                       value_name="link", value_data=b'\x00\x00\x00\x00',
                       value_type=winreg.REG_BINARY)

        self._add_item("explorer_18", "禁止自动播放",
                       "禁止插入可移动设备时自动播放内容",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\AutoplayHandlers",
                       value_name="DisableAutoplay", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("explorer_19", "在单独的进程中打开文件夹窗口",
                       "每个文件夹窗口在独立的进程中运行，提高稳定性",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                       value_name="SeparateProcess", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("explorer_20", "标题栏显示完整路径",
                       "在资源管理器标题栏显示当前文件夹的完整路径",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\CabinetState",
                       value_name="FullPath", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("explorer_21", "快速访问不显示常用文件夹",
                       "不在快速访问中显示常用文件夹",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Explorer",
                       value_name="ShowFrequent", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("explorer_22", "快速访问不显示最近使用的文件",
                       "不在快速访问中显示最近使用的文件",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Explorer",
                       value_name="ShowRecent", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("explorer_23", "资源管理器崩溃时自动重启",
                       "当资源管理器崩溃时自动重新启动",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                       value_name="AutoRestartShell", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("explorer_24", "桌面显示此电脑",
                       "在桌面上显示\"此电脑\"图标",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel",
                       value_name="{20D04FE0-3AEA-1069-A2D8-08002B30309D}", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("explorer_25", "桌面显示回收站",
                       "在桌面上显示回收站图标",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel",
                       value_name="{645FF040-5081-101B-9F08-00AA002F954E}", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("explorer_26", "隐藏桌面上的\"了解此图片\"图标",
                       "隐藏桌面上\"了解此图片\"的图标",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\HideDesktopIcons\NewStartPanel",
                       value_name="{2cc5ca98-6485-489a-920e-b3e88a6ccce2}", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("explorer_27", "微软拼音默认为英文输入",
                       "将微软拼音输入法默认模式设置为英文输入",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\InputMethod\Settings\CHS",
                       value_name="EnglishModeEnabled", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("explorer_28", "关闭微软拼音云计算",
                       "关闭微软拼音输入法的云计算候选功能",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\InputMethod\Settings\CHS",
                       value_name="EnableCloudCandidate", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("explorer_29", "去除本地磁盘重复显示",
                       "在导航窗格中去除重复显示的本地磁盘",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                       value_name="HideDrivesWithNoMedia", value_data=1,
                       value_type=winreg.REG_DWORD)

    def _build_xingneng_items(self):
        cat = self.CATEGORY_XINGNENG

        self._add_item("xingneng_01", "优化进程数量",
                       "提高服务主机拆分阈值，优化系统进程数量",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SYSTEM\CurrentControlSet\Control",
                       value_name="SvcHostSplitThresholdInKB", value_data=5120000,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_02", "不允许在「开始」菜单显示建议",
                       "禁止在开始菜单中显示应用推荐和建议",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                       value_name="SubscribedContent-338388Enabled", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_03", "不要在应用商店中查找关联应用",
                       "禁止在应用商店中搜索关联的应用程序",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\Explorer",
                       value_name="NoUseStoreOpenWith", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_04", "关闭商店应用推广",
                       "禁止Microsoft Store静默安装推广应用",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                       value_name="SilentInstalledAppsEnabled", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_05", "禁止应用商店自动下载和安装更新",
                       "禁止Microsoft Store自动下载和安装应用更新",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\WindowsStore",
                       value_name="AutoDownload", value_data=2,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_06", "关闭锁屏时的Windows聚焦推广",
                       "关闭锁屏界面的Windows聚焦内容推广",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                       value_name="RotatingLockScreenOverlayEnabled", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_07", "关闭\"使用Windows时获取技巧和建议\"",
                       "关闭Windows使用过程中的技巧和建议提示",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                       value_name="SubscribedContent-338389Enabled", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_08", "禁止自动安装推荐的应用程序",
                       "禁止Windows自动安装推荐的应用",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                       value_name="SubscribedContent-338393Enabled", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_09", "关闭游戏录制工具",
                       "关闭Xbox Game Bar游戏录制功能",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"System\GameConfigStore",
                       value_name="GameDVR_Enabled", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_10", "关闭多嘴的小娜",
                       "禁用Cortana语音助手",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\Windows Search",
                       value_name="AllowCortana", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_11", "\"运行\"对话框不要显示历史记录",
                       "不记录运行对话框的使用历史",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                       value_name="Start_TrackProgs", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_12", "隐藏「开始」菜单中的\"推荐\"",
                       "隐藏开始菜单中的推荐内容区域",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\Explorer",
                       value_name="HideRecommendedSection", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_13", "隐藏「开始」菜单历史记录中推荐的网站",
                       "在开始菜单中隐藏最近添加的应用",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\Explorer",
                       value_name="HideRecentlyAddedApps", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_14", "加快关机速度",
                       "缩短等待无响应程序关闭的超时时间",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Control Panel\Desktop",
                       value_name="WaitToKillAppTimeout", value_data="2000",
                       value_type=winreg.REG_SZ)

        self._add_item("xingneng_15", "缩短关闭服务等待时间",
                       "缩短无响应程序的挂起超时时间",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Control Panel\Desktop",
                       value_name="HungAppTimeout", value_data="1000",
                       value_type=winreg.REG_SZ)

        self._add_item("xingneng_16", "关闭远程协助",
                       "禁止使用Windows远程协助功能",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SYSTEM\CurrentControlSet\Control\Remote Assistance",
                       value_name="fAllowToGetHelp", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_17", "禁用远程修改注册表",
                       "禁止远程访问和修改本机的注册表，并禁用RemoteRegistry服务",
                       cat, "multi",
                       actions=[
                           {"type": "reg", "hive": winreg.HKEY_LOCAL_MACHINE,
                            "path": r"SYSTEM\CurrentControlSet\Control\SecurePipeServers\winreg",
                            "value_name": "RemoteRegAccess", "value_data": 1,
                            "value_type": winreg.REG_DWORD},
                           {"type": "sc", "service_name": "RemoteRegistry",
                            "start_type": "disabled", "stop": True},
                       ])

        self._add_item("xingneng_18", "禁用诊断服务",
                       "禁用连接用户体验和遥测诊断服务(DiagTrack)",
                       cat, "sc",
                       service_name="DiagTrack", start_type="disabled", stop=True)

        self._add_item("xingneng_19", "禁用SysMain",
                       "禁用SysMain(Superfetch)服务以节省内存",
                       cat, "sc",
                       service_name="SysMain", start_type="disabled", stop=True)

        self._add_item("xingneng_20", "禁用Windows Search",
                       "禁用Windows Search索引服务",
                       cat, "sc",
                       service_name="WSearch", start_type="disabled", stop=True)

        self._add_item("xingneng_21", "禁用错误报告",
                       "禁止Windows发送错误报告",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Microsoft\Windows\Windows Error Reporting",
                       value_name="Disabled", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_22", "禁用家庭组",
                       "禁用家庭组相关服务以释放系统资源",
                       cat, "multi_sc",
                       services=[
                           {"service_name": "HomeGroupProvider", "start_type": "disabled"},
                           {"service_name": "HomeGroupListener", "start_type": "disabled"},
                       ])

        self._add_item("xingneng_23", "禁用客户体验改善计划",
                       "禁止参与Windows客户体验改善计划",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\SQMClient\Windows",
                       value_name="CEIPEnable", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_24", "禁用NTFS链接跟踪服务",
                       "禁用分布式链接跟踪客户端服务",
                       cat, "sc",
                       service_name="TrkWks", start_type="disabled")

        self._add_item("xingneng_25", "禁止自动维护计划",
                       "禁止Windows在空闲时自动执行系统维护任务",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\Maintenance",
                       value_name="MaintenanceDisabled", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_26", "启用大系统缓存以提高性能",
                       "启用大系统缓存模式以提高文件系统性能",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management",
                       value_name="LargeSystemCache", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_27", "禁止系统内核与驱动程序分页到硬盘",
                       "禁止将内核和驱动程序页面交换到磁盘，提高响应速度",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management",
                       value_name="DisablePagingExecutive", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_28", "增加文件管理系统缓存以提高性能",
                       "增加I/O页面锁定限制为256MB以提高磁盘性能",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management",
                       value_name="IoPageLockLimit", value_data=268435456,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_29", "启用高性能电源计划",
                       "将电源计划切换为高性能模式",
                       cat, "cmd",
                       command="powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c")

        self._add_item("xingneng_30", "禁用处理器的幽灵和熔断补丁",
                       "禁用Spectre和Meltdown漏洞的缓解措施以提高CPU性能",
                       cat, "multi_reg",
                       actions=[
                           {"hive": winreg.HKEY_LOCAL_MACHINE,
                            "path": r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management",
                            "value_name": "FeatureSettingsOverride", "value_data": 3,
                            "value_type": winreg.REG_DWORD},
                           {"hive": winreg.HKEY_LOCAL_MACHINE,
                            "path": r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management",
                            "value_name": "FeatureSettingsOverrideMask", "value_data": 3,
                            "value_type": winreg.REG_DWORD},
                       ])

        self._add_item("xingneng_31", "禁用保留的存储",
                       "禁用Windows保留的存储空间以释放磁盘空间",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\ReserveManager",
                       value_name="ShippedWithReserves", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_32", "优化处理器性能",
                       "启用资源策略以优化处理器性能分配",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SYSTEM\CurrentControlSet\Control\Session Manager",
                       value_name="ResourcePolicies", value_data="1",
                       value_type=winreg.REG_SZ)

        self._add_item("xingneng_33", "加快预读能力改善速度",
                       "启用系统和应用程序的预读取功能以加快启动速度",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters",
                       value_name="EnablePrefetcher", value_data=3,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_34", "禁止系统自动生成错误报告",
                       "禁止系统为崩溃的进程自动生成错误报告文件",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Microsoft\Windows\Windows Error Reporting",
                       value_name="Disabled", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_35", "禁用高精度事件定时器(HPET)",
                       "禁用HPET以提高游戏性能和减少延迟",
                       cat, "cmd",
                       command="bcdedit /set useplatformclock false")

        self._add_item("xingneng_36", "关闭系统自动调试功能",
                       "禁止显示Windows错误报告的用户界面",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\Windows Error Reporting",
                       value_name="DontShowUI", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_37", "关闭程序兼容性助手",
                       "禁用程序兼容性助手服务",
                       cat, "sc",
                       service_name="PcaSvc", start_type="disabled")

        self._add_item("xingneng_38", "启用自动完成设备设置",
                       "允许从网络获取设备元数据以完成设备设置",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Device Metadata",
                       value_name="PreventDeviceMetadataFromNetwork", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_39", "关闭Exploit Protection(乱序内存)",
                       "禁用控制流保护(CFG)以提升部分应用性能",
                       cat, "cmd",
                       command="powershell -Command \"Set-ProcessMitigation -System -Disable CFG\"")

        self._add_item("xingneng_40", "优化Windows Search和小娜的设置",
                       "禁止Windows Search使用位置信息",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\Windows Search",
                       value_name="AllowSearchToUseLocation", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_41", "关闭广告ID",
                       "通过组策略和用户设置双重关闭广告ID",
                       cat, "multi_reg",
                       actions=[
                           {"hive": winreg.HKEY_LOCAL_MACHINE,
                            "path": r"SOFTWARE\Policies\Microsoft\Windows\AdvertisingInfo",
                            "value_name": "DisabledByGroupPolicy", "value_data": 1,
                            "value_type": winreg.REG_DWORD},
                           {"hive": winreg.HKEY_CURRENT_USER,
                            "path": r"Software\Microsoft\Windows\CurrentVersion\AdvertisingInfo",
                            "value_name": "Enabled", "value_data": 0,
                            "value_type": winreg.REG_DWORD},
                       ])

        self._add_item("xingneng_42", "禁用磁盘空间不足警告",
                       "禁止在磁盘空间不足时显示警告通知",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer",
                       value_name="NoLowDiskSpaceChecks", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_43", "去除搜索页面信息流和热搜",
                       "关闭搜索页面的动态搜索框和热搜内容",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\SearchSettings",
                       value_name="IsDynamicSearchBoxEnabled", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_44", "关闭TSX漏洞补丁",
                       "禁用TSX(事务同步扩展)漏洞的缓解措施",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management",
                       value_name="FeatureSettingsOverride", value_data=3,
                       value_type=winreg.REG_DWORD)

        self._add_item("xingneng_45", "开启GPU硬件加速",
                       "启用WPF应用程序的GPU硬件加速",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Avalon.Graphics",
                       value_name="DisableHWAcceleration", value_data=0,
                       value_type=winreg.REG_DWORD)

    def _build_safe_items(self):
        cat = self.CATEGORY_SAFE

        self._add_item("safe_01", "UAC从不通知",
                       "将用户账户控制设置为从不通知级别",
                       cat, "multi_reg",
                       actions=[
                           {"hive": winreg.HKEY_LOCAL_MACHINE,
                            "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System",
                            "value_name": "EnableLUA", "value_data": 0,
                            "value_type": winreg.REG_DWORD},
                           {"hive": winreg.HKEY_LOCAL_MACHINE,
                            "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System",
                            "value_name": "ConsentPromptBehaviorAdmin", "value_data": 0,
                            "value_type": winreg.REG_DWORD},
                       ])

        self._add_item("safe_02", "内置管理员账户管理审批模式",
                       "对内置管理员账户启用管理审批模式",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System",
                       value_name="FilterAdministratorToken", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("safe_03", "以管理审批模式运行所有管理员",
                       "所有管理员均在管理审批模式下运行",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System",
                       value_name="ConsentPromptBehaviorAdmin", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("safe_04", "仅提升安全路径下的UIAccess程序",
                       "仅在安全路径下允许提升UIAccess程序权限",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System",
                       value_name="EnableUIADesktopToggle", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("safe_05", "允许UIAccess程序在非安全桌面上提升",
                       "允许UIAccess程序在非安全桌面上提升权限",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System",
                       value_name="EnableUIADesktopToggle", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("safe_06", "关闭SmartScreen",
                       "关闭Windows SmartScreen筛选器",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\System",
                       value_name="EnableSmartScreen", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("safe_07", "关闭打开程序的安全警告",
                       "将常见可执行文件类型添加到低风险文件列表，关闭安全警告",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Policies\Associations",
                       value_name="LowRiskFileTypes",
                       value_data=".exe;.bat;.cmd;.reg;.msi",
                       value_type=winreg.REG_SZ)

        self._add_item("safe_08", "关闭防火墙",
                       "关闭所有网络配置文件的Windows防火墙",
                       cat, "cmd",
                       command="netsh advfirewall set allprofiles state off")

        self._add_item("safe_09", "关闭内存完整性",
                       "禁用基于虚拟化的安全-内存完整性检查",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\HypervisorEnforcedCodeIntegrity",
                       value_name="Enabled", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("safe_10", "关闭虚拟化安全性",
                       "禁用基于虚拟化的安全性(VBS)",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\DeviceGuard",
                       value_name="EnableVirtualizationBasedSecurity", value_data=0,
                       value_type=winreg.REG_DWORD)

    def _build_edge_items(self):
        cat = self.CATEGORY_EDGE

        self._add_item("edge_01", "不要显示首次运行欢迎页面",
                       "Edge浏览器不显示首次运行的欢迎引导页面",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Edge",
                       value_name="HideFirstRunExperience", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("edge_02", "关闭后禁止继续运行后台应用",
                       "关闭Edge后不允许其继续在后台运行",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Edge",
                       value_name="BackgroundModeEnabled", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("edge_03", "禁用启动增强",
                       "禁用Edge浏览器的启动增强功能",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Edge",
                       value_name="StartupBoostEnabled", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("edge_04", "阻止必应搜索结果中的广告",
                       "阻止必应搜索结果中的侵入式广告",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Edge",
                       value_name="AdsSettingForIntrusiveAdsSites", value_data=2,
                       value_type=winreg.REG_DWORD)

        self._add_item("edge_05", "隐藏默认热门站点",
                       "在新标签页中隐藏默认的热门站点",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Edge",
                       value_name="NewTabPageHideDefaultTopSites", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("edge_06", "隐藏Edge浏览器边栏",
                       "隐藏Edge浏览器的侧边栏",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Edge",
                       value_name="HubsSidebarEnabled", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("edge_07", "关闭停止支持旧系统的通知",
                       "不显示关于旧操作系统不受支持的通知",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Edge",
                       value_name="SuppressUnsupportedOSWarning", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("edge_08", "不发送任何诊断数据",
                       "禁止Edge浏览器向微软发送诊断数据",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Edge",
                       value_name="DiagnosticsData", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("edge_09", "禁用标签页性能检测器",
                       "禁用Edge的标签页性能检测功能",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Edge",
                       value_name="PerformanceDetectorEnabled", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("edge_10", "禁用新选项卡页面上的微软资讯",
                       "在新标签页上禁用微软资讯内容",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Edge",
                       value_name="NewTabPageContentEnabled", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("edge_11", "禁用个性化广告和体验",
                       "禁止Edge进行个性化广告和相关体验",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Edge",
                       value_name="PersonalizationReportingEnabled", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("edge_12", "禁用不安全的下载警告",
                       "通过豁免域文件类型对来禁用不安全下载的警告",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Edge",
                       value_name="ExemptDomainFileTypePairsFromFileTypeDownloadWarnings",
                       value_data=1, value_type=winreg.REG_DWORD)

    def _build_system_items(self):
        cat = self.CATEGORY_SYSTEM

        self._add_item("system_01", "关闭休眠",
                       "关闭系统休眠功能并删除hiberfil.sys文件以释放磁盘空间",
                       cat, "cmd",
                       command="powercfg /h off")

        self._add_item("system_02", "弹出USB磁盘后彻底断开其电源",
                       "禁用USB选择性暂停，弹出后彻底断开USB设备电源",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SYSTEM\CurrentControlSet\Services\USB",
                       value_name="DisableSelectiveSuspend", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("system_03", "不要将VHD动态文件扩展到最大",
                       "挂载VHD时不自动扩展到最大大小",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SYSTEM\CurrentControlSet\Services\FsDepends\Parameters",
                       value_name="VirtualDiskExpandOnMount", value_data=4,
                       value_type=winreg.REG_DWORD)

        self._add_item("system_04", "蓝屏时自动重启",
                       "系统蓝屏崩溃后自动重新启动",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SYSTEM\CurrentControlSet\Control\CrashControl",
                       value_name="AutoReboot", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("system_05", "关闭系统自动调试功能",
                       "禁用崩溃转储文件生成",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SYSTEM\CurrentControlSet\Control\CrashControl",
                       value_name="CrashDumpEnabled", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("system_06", "磁盘错误检查等待时间缩短到五秒",
                       "有已登录用户时不自动重启电脑",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Policies\System",
                       value_name="NoAutoRebootWithLoggedOnUsers", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("system_07", "设备安装禁止创建系统还原点",
                       "安装设备驱动程序时不创建系统还原点",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Device Metadata",
                       value_name="DisableSystemRestore", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("system_08", "MSI软件安装禁止创建系统还原点",
                       "安装MSI软件时不创建系统还原点",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\Installer",
                       value_name="LimitSystemRestoreCheckpointing", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("system_09", "关闭系统还原",
                       "完全禁用系统还原功能",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\SystemRestore",
                       value_name="DisableSR", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("system_10", "根据语言设置隐藏字体",
                       "根据语言设置自动隐藏不适用的字体",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows NT\CurrentVersion\Font Management",
                       value_name="Inactive Fonts", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("system_11", "允许字体作为快捷方式安装",
                       "允许以快捷方式安装字体而非复制到Fonts文件夹",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts",
                       value_name="EnableFontShortcut", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("system_12", "崩溃时不写入调试信息",
                       "系统崩溃时不写入内存转储文件",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SYSTEM\CurrentControlSet\Control\CrashControl",
                       value_name="CrashDumpEnabled", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("system_13", "禁用账户登录日志报告",
                       "禁用登录时的详细状态消息",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System",
                       value_name="DisableStatusMessages", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("system_14", "禁用WfpDiag.ETL日志",
                       "禁用Windows过滤平台诊断ETL日志",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Microsoft\Windows\CurrentVersion\WINEVT\Channels\Microsoft-Windows-WFP",
                       value_name="Enabled", value_data=0,
                       value_type=winreg.REG_DWORD)

    def _build_update_items(self):
        cat = self.CATEGORY_UPDATE

        self._add_item("update_01", "自动安装无需重启的更新",
                       "自动下载并安排安装更新，无需用户交互",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU",
                       value_name="AUOptions", value_data=4,
                       value_type=winreg.REG_DWORD)

        self._add_item("update_02", "更新挂起时有用户登录不自动重启",
                       "有已登录用户时不自动重启以完成更新",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU",
                       value_name="NoAutoRebootWithLoggedOnUsers", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("update_03", "Windows更新不包括驱动程序",
                       "质量更新中排除驱动程序更新",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate",
                       value_name="ExcludeWUDriversInQualityUpdate", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("update_04", "禁止大版本更新",
                       "锁定当前Windows版本，禁止大版本功能更新",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate",
                       value_name="TargetReleaseVersion", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("update_05", "更新不包括恶意软件删除工具",
                       "Windows更新中不包含恶意软件删除工具(MRT)",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\MRT",
                       value_name="DontOfferThroughWUAU", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("update_06", "从不检查系统更新",
                       "禁用Windows自动更新检查",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU",
                       value_name="NoAutoUpdate", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("update_07", "不要显示\"新版本记事本已可用\"提示",
                       "关闭有关新版本记事本可用的通知",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Notifications\Settings",
                       value_name="NOC_GLOBAL_SETTING_ALLOW_NOTIFICATION_SOUND",
                       value_data=0, value_type=winreg.REG_DWORD)

    def _build_yinsi_items(self):
        cat = self.CATEGORY_YINSI

        self._add_item("yinsi_01", "禁用页面预测功能",
                       "禁用IE浏览器的页面预测功能",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Internet Explorer\Main",
                       value_name="DisablePagePrediction", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_02", "禁用SMS路由器服务",
                       "禁用SMS路由器服务以保护隐私",
                       cat, "sc",
                       service_name="SmsRouter", start_type="disabled")

        self._add_item("yinsi_03", "禁用活动收集",
                       "将遥测级别设置为0(安全性)，禁止活动数据收集",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
                       value_name="AllowTelemetry", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_04", "禁用应用启动跟踪",
                       "禁止应用通过语音激活来启动跟踪",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\AppPrivacy",
                       value_name="LetAppsActivateWithVoice", value_data=2,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_05", "禁用广告标识符",
                       "通过组策略禁用Windows广告标识符",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\AdvertisingInfo",
                       value_name="DisabledByGroupPolicy", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_06", "禁用应用访问文件系统",
                       "禁止应用访问文件系统",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\AppPrivacy",
                       value_name="LetAppsAccessFileSystem", value_data=2,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_07", "禁用应用访问文档",
                       "禁止应用访问文档库",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\AppPrivacy",
                       value_name="LetAppsAccessDocuments", value_data=2,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_08", "禁用应用访问日历",
                       "禁止应用访问日历信息",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\AppPrivacy",
                       value_name="LetAppsAccessCalendar", value_data=2,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_09", "禁用应用访问联系人",
                       "禁止应用访问联系人信息",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\AppPrivacy",
                       value_name="LetAppsAccessContacts", value_data=2,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_10", "禁用网站语言跟踪",
                       "禁止网站通过HTTP Accept-Language头跟踪语言偏好",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Control Panel\International\User Profile",
                       value_name="HttpAcceptLanguageOptOut", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_11", "禁用Windows欢迎体验",
                       "禁用Windows消费者功能和欢迎体验",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\CloudContent",
                       value_name="DisableWindowsConsumerFeatures", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_12", "禁用反馈频率",
                       "禁止显示Windows反馈通知",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
                       value_name="DoNotShowFeedbackNotifications", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_13", "禁用诊断数据收集",
                       "将遥测级别设置为0，完全禁用诊断数据收集",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
                       value_name="AllowTelemetry", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_14", "禁用写作习惯跟踪",
                       "禁止收集用户的书写和输入习惯数据",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\InputPersonalization",
                       value_name="RestrictImplicitTextCollection", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_15", "禁用设置应用建议",
                       "禁止在设置应用中显示建议内容",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                       value_name="SubscribedContent-338393Enabled", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_16", "禁用Bing搜索结果",
                       "禁止在开始菜单搜索中显示Bing网络搜索结果",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Search",
                       value_name="BingSearchEnabled", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_17", "禁用通讯录收集",
                       "禁止收集手写输入数据以保护隐私",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\InputPersonalization",
                       value_name="RestrictImplicitInkCollection", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_18", "禁用键入文本收集",
                       "禁止收集键盘键入的文本数据",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\InputPersonalization",
                       value_name="RestrictImplicitTextCollection", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_19", "禁用搜索历史",
                       "禁止在设备上保存搜索历史记录",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\SearchSettings",
                       value_name="IsDeviceSearchHistoryEnabled", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_20", "禁用赞助商应用安装",
                       "禁止静默安装赞助商推广的应用",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                       value_name="SilentInstalledAppsEnabled", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_21", "禁用自动连接热点",
                       "禁止自动连接到OEM配置的WiFi热点",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Microsoft\WcmSvc\wifinetworkmanager\config",
                       value_name="AutoConnectAllowedOEM", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_22", "禁用输入数据个性化",
                       "禁止硬件键盘文本预测功能",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Input\Tsf",
                       value_name="EnableHwkbTextPrediction", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_23", "禁用键入见解",
                       "禁止收集键入洞察数据",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\InputPersonalization",
                       value_name="RestrictImplicitTextCollection", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_24", "禁用预安装应用",
                       "禁用Windows消费者功能以阻止预安装应用",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\CloudContent",
                       value_name="DisableWindowsConsumerFeatures", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_25", "禁用.NET遥测",
                       "禁用.NET Framework的遥测数据收集",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full",
                       value_name="EnableDotNetTelemetry", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_26", "禁用PowerShell遥测",
                       "设置环境变量以禁用PowerShell遥测",
                       cat, "env",
                       env_var="POWERSHELL_TELEMETRY_OPTOUT", env_value="1")

        self._add_item("yinsi_27", "禁用遥测服务",
                       "禁用连接用户体验和遥测服务(DiagTrack)",
                       cat, "sc",
                       service_name="DiagTrack", start_type="disabled", stop=True)

        self._add_item("yinsi_28", "禁用语音激活(Cortana)",
                       "通过禁用Cortana来禁止语音激活功能",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\Windows Search",
                       value_name="AllowCortana", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_29", "禁用位置服务",
                       "完全禁用Windows位置服务",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\LocationAndSensors",
                       value_name="DisableLocation", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_30", "启用剪切板历史记录",
                       "启用Windows剪切板历史记录功能",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\System",
                       value_name="AllowClipboardHistory", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_31", "禁用定向广告",
                       "通过组策略禁用Windows定向广告",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Policies\Microsoft\Windows\AdvertisingInfo",
                       value_name="DisabledByGroupPolicy", value_data=1,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_32", "禁用Wi-Fi感知",
                       "禁用Wi-Fi感知共享凭据功能",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SOFTWARE\Microsoft\WcmSvc\wifinetworkmanager\features",
                       value_name="WiFiSenseCredShared", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_33", "禁用步骤记录器",
                       "禁止开始菜单记录程序运行历史",
                       cat, "reg",
                       hive=winreg.HKEY_CURRENT_USER,
                       path=r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                       value_name="Start_TrackProgs", value_data=0,
                       value_type=winreg.REG_DWORD)

        self._add_item("yinsi_34", "禁用写入调试信息",
                       "清空调试信息文件路径以禁用调试日志写入",
                       cat, "reg",
                       hive=winreg.HKEY_LOCAL_MACHINE,
                       path=r"SYSTEM\CurrentControlSet\Control\Session Manager",
                       value_name="DebugFilePath", value_data="",
                       value_type=winreg.REG_SZ)

    def get_optimization_items(self):
        result = {}
        category_order = [
            self.CATEGORY_EXPLORER,
            self.CATEGORY_XINGNENG,
            self.CATEGORY_SAFE,
            self.CATEGORY_EDGE,
            self.CATEGORY_SYSTEM,
            self.CATEGORY_UPDATE,
            self.CATEGORY_YINSI,
        ]
        for cat in category_order:
            if cat in self._categories:
                result[cat] = [
                    {
                        "id": item.item_id,
                        "name": item.name,
                        "description": item.description,
                        "category": item.category,
                    }
                    for item in self._categories[cat]
                ]
        return result

    def apply_optimization(self, item_id):
        item = self._items.get(item_id)
        if not item:
            return False, f"未知优化项: {item_id}"

        try:
            if item.item_type == "reg":
                return self._apply_reg(item)
            elif item.item_type == "multi_reg":
                return self._apply_multi_reg(item)
            elif item.item_type == "sc":
                return self._apply_sc(item)
            elif item.item_type == "multi_sc":
                return self._apply_multi_sc(item)
            elif item.item_type == "cmd":
                return self._apply_cmd(item)
            elif item.item_type == "env":
                return self._apply_env(item)
            elif item.item_type == "multi":
                return self._apply_multi(item)
            else:
                return False, f"未知优化类型: {item.item_type}"
        except Exception as e:
            return False, f"优化失败: {str(e)}"

    def _apply_reg(self, item):
        hive = item.kwargs["hive"]
        path = item.kwargs["path"]
        value_name = item.kwargs["value_name"]
        value_data = item.kwargs["value_data"]
        value_type = item.kwargs.get("value_type", winreg.REG_DWORD)

        try:
            key = winreg.CreateKey(hive, path)
            winreg.SetValueEx(key, value_name, 0, value_type, value_data)
            winreg.CloseKey(key)
            return True, f"{item.name} - 设置成功"
        except WindowsError as e:
            return False, f"{item.name} - 注册表写入失败: {str(e)}"

    def _apply_multi_reg(self, item):
        actions = item.kwargs.get("actions", [])
        all_ok = True
        messages = []
        for action in actions:
            hive = action["hive"]
            path = action["path"]
            value_name = action["value_name"]
            value_data = action["value_data"]
            value_type = action.get("value_type", winreg.REG_DWORD)
            try:
                key = winreg.CreateKey(hive, path)
                winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                winreg.CloseKey(key)
                messages.append(f"{value_name} - 成功")
            except WindowsError as e:
                all_ok = False
                messages.append(f"{value_name} - 失败: {str(e)}")
        return all_ok, f"{item.name} - {'; '.join(messages)}"

    def _apply_sc(self, item):
        service_name = item.kwargs["service_name"]
        start_type = item.kwargs.get("start_type", "disabled")
        stop = item.kwargs.get("stop", False)
        all_ok = True
        messages = []

        if stop:
            ok, _, _ = SystemUtils.run_command(f"sc stop {service_name}")
            if not ok:
                all_ok = False
                messages.append(f"停止服务失败")
            else:
                messages.append("服务已停止")

        ok, _, _ = SystemUtils.run_command(f"sc config {service_name} start= {start_type}")
        if not ok:
            all_ok = False
            messages.append(f"配置服务失败")
        else:
            messages.append(f"服务已设为{start_type}")

        return all_ok, f"{item.name} - {'; '.join(messages)}"

    def _apply_multi_sc(self, item):
        services = item.kwargs.get("services", [])
        all_ok = True
        messages = []
        for svc in services:
            service_name = svc["service_name"]
            start_type = svc.get("start_type", "disabled")
            ok, _, _ = SystemUtils.run_command(f"sc config {service_name} start= {start_type}")
            if not ok:
                all_ok = False
                messages.append(f"{service_name} - 失败")
            else:
                messages.append(f"{service_name} - 已设为{start_type}")
        return all_ok, f"{item.name} - {'; '.join(messages)}"

    def _apply_cmd(self, item):
        command = item.kwargs["command"]
        ok, stdout, stderr = SystemUtils.run_command(command)
        if ok:
            return True, f"{item.name} - 命令执行成功"
        else:
            error_msg = stderr.strip() if stderr else "命令执行失败"
            return False, f"{item.name} - {error_msg}"

    def _apply_env(self, item):
        env_var = item.kwargs["env_var"]
        env_value = item.kwargs["env_value"]
        try:
            os.environ[env_var] = env_value
            SystemUtils.run_command(f'setx {env_var} {env_value}')
            return True, f"{item.name} - 环境变量设置成功"
        except Exception as e:
            return False, f"{item.name} - 环境变量设置失败: {str(e)}"

    def _apply_multi(self, item):
        actions = item.kwargs.get("actions", [])
        all_ok = True
        messages = []
        for action in actions:
            action_type = action.get("type", "reg")
            if action_type == "reg":
                try:
                    hive = action["hive"]
                    path = action["path"]
                    value_name = action["value_name"]
                    value_data = action["value_data"]
                    value_type = action.get("value_type", winreg.REG_DWORD)
                    key = winreg.CreateKey(hive, path)
                    winreg.SetValueEx(key, value_name, 0, value_type, value_data)
                    winreg.CloseKey(key)
                    messages.append(f"注册表 {value_name} - 成功")
                except WindowsError as e:
                    all_ok = False
                    messages.append(f"注册表 {value_name} - 失败: {str(e)}")
            elif action_type == "sc":
                service_name = action["service_name"]
                start_type = action.get("start_type", "disabled")
                stop = action.get("stop", False)
                if stop:
                    SystemUtils.run_command(f"sc stop {service_name}")
                ok, _, _ = SystemUtils.run_command(f"sc config {service_name} start= {start_type}")
                if not ok:
                    all_ok = False
                    messages.append(f"服务 {service_name} - 失败")
                else:
                    messages.append(f"服务 {service_name} - 已配置")
        return all_ok, f"{item.name} - {'; '.join(messages)}"

    def apply_batch(self, item_ids, progress_callback=None):
        results = []
        total = len(item_ids)
        for i, item_id in enumerate(item_ids):
            if progress_callback:
                progress_callback(i, total, f"正在优化: {item_id}")
            success, message = self.apply_optimization(item_id)
            results.append({
                "id": item_id,
                "success": success,
                "message": message
            })
            if progress_callback:
                progress_callback(i + 1, total, f"{message}")
        return results

    def get_basic_preset(self):
        basic_ids = [
            "explorer_05", "explorer_06", "explorer_08", "explorer_09",
            "explorer_10", "explorer_11", "explorer_12", "explorer_13",
            "explorer_14", "explorer_17", "explorer_18", "explorer_21",
            "explorer_22", "explorer_23", "explorer_24", "explorer_25",
            "explorer_26", "explorer_27", "explorer_28",
            "xingneng_01", "xingneng_02", "xingneng_03", "xingneng_04",
            "xingneng_05", "xingneng_06", "xingneng_07", "xingneng_08",
            "xingneng_09", "xingneng_10", "xingneng_11", "xingneng_12",
            "xingneng_13", "xingneng_17", "xingneng_18", "xingneng_21",
            "xingneng_22", "xingneng_23", "xingneng_24", "xingneng_25",
            "xingneng_32", "xingneng_33", "xingneng_34", "xingneng_37",
            "xingneng_40", "xingneng_41", "xingneng_42", "xingneng_43",
            "xingneng_45",
            "safe_06", "safe_07",
            "edge_01", "edge_02", "edge_03", "edge_04", "edge_05",
            "edge_06", "edge_07", "edge_08", "edge_09", "edge_10", "edge_11",
            "system_06", "system_10", "system_11",
            "update_01", "update_02", "update_03", "update_05", "update_07",
            "yinsi_01", "yinsi_02", "yinsi_03", "yinsi_04", "yinsi_05",
            "yinsi_06", "yinsi_07", "yinsi_08", "yinsi_09", "yinsi_10",
            "yinsi_11", "yinsi_12", "yinsi_13", "yinsi_19", "yinsi_20",
            "yinsi_21", "yinsi_31", "yinsi_32",
        ]
        return [i for i in basic_ids if i in self._items]

    def get_deep_preset(self):
        conflicting = {"safe_05"}
        return [i for i in self._items if i not in conflicting]

    def backup_registry(self, item_ids):
        self.BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.BACKUP_DIR / f"reg_backup_{timestamp}.json"
        backup_data = {}

        for item_id in item_ids:
            item = self._items.get(item_id)
            if not item:
                continue

            def _backup_reg(hive, path, value_name, value_type):
                entry_key = f"{hive}|{path}|{value_name}"
                if entry_key in backup_data:
                    return
                try:
                    key = winreg.OpenKey(hive, path)
                    old_value, old_type = winreg.QueryValueEx(key, value_name)
                    winreg.CloseKey(key)
                    backup_data[entry_key] = {
                        "hive": hive,
                        "path": path,
                        "value_name": value_name,
                        "old_value": old_value,
                        "old_type": old_type,
                    }
                except WindowsError:
                    backup_data[entry_key] = {
                        "hive": hive,
                        "path": path,
                        "value_name": value_name,
                        "old_value": None,
                        "old_type": None,
                        "did_not_exist": True,
                    }

            if item.item_type == "reg":
                _backup_reg(
                    item.kwargs["hive"], item.kwargs["path"],
                    item.kwargs["value_name"],
                    item.kwargs.get("value_type", winreg.REG_DWORD)
                )
            elif item.item_type in ("multi_reg", "multi"):
                actions = item.kwargs.get("actions", [])
                for action in actions:
                    if action.get("type", "reg") == "reg":
                        _backup_reg(
                            action["hive"], action["path"],
                            action["value_name"],
                            action.get("value_type", winreg.REG_DWORD)
                        )

        try:
            with open(backup_file, "w", encoding="utf-8") as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False, default=str)
            return True, str(backup_file)
        except Exception as e:
            return False, str(e)

    def restore_from_backup(self, backup_file=None):
        if backup_file is None:
            if not self.BACKUP_DIR.exists():
                return False, "没有找到备份目录"
            backups = sorted(self.BACKUP_DIR.glob("reg_backup_*.json"), reverse=True)
            if not backups:
                return False, "没有找到备份文件"
            backup_file = backups[0]

        try:
            with open(backup_file, "r", encoding="utf-8") as f:
                backup_data = json.load(f)
        except Exception as e:
            return False, f"读取备份文件失败: {str(e)}"

        restored = 0
        failed = 0
        for entry_key, entry in backup_data.items():
            hive = entry["hive"]
            path = entry["path"]
            value_name = entry["value_name"]
            old_value = entry["old_value"]
            old_type = entry["old_type"]
            did_not_exist = entry.get("did_not_exist", False)

            try:
                if did_not_exist:
                    try:
                        key = winreg.OpenKey(hive, path, 0, winreg.KEY_WRITE)
                        winreg.DeleteValue(key, value_name)
                        winreg.CloseKey(key)
                    except WindowsError:
                        pass
                else:
                    key = winreg.CreateKey(hive, path)
                    winreg.SetValueEx(key, value_name, 0, old_type, old_value)
                    winreg.CloseKey(key)
                restored += 1
            except WindowsError:
                failed += 1

        return True, f"恢复完成: 成功 {restored} 项, 失败 {failed} 项"

    def get_item_by_id(self, item_id):
        return self._items.get(item_id)

    def get_all_category_names(self):
        return [
            self.CATEGORY_EXPLORER,
            self.CATEGORY_XINGNENG,
            self.CATEGORY_SAFE,
            self.CATEGORY_EDGE,
            self.CATEGORY_SYSTEM,
            self.CATEGORY_UPDATE,
            self.CATEGORY_YINSI,
        ]