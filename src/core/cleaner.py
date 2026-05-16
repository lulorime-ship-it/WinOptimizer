import subprocess
import os


class Cleaner:
    CACHE_FILES = "缓存文件"
    SYSTEM_FILES = "系统文件"
    TEMP_FILES = "临时文件"

    def __init__(self):
        self._commands = self._build_commands()

    def _build_commands(self):
        return {
            self.CACHE_FILES: [
                CleanItem("Terminal Server Client缓存",
                          'del /f /s /q "%LocalAppData%\\Microsoft\\Terminal Server Client\\Cache\\*" >nul 2>&1'),
                CleanItem("Windows更新缓存",
                          'del /f /s /q "%SystemRoot%\\SoftwareDistribution\\Download\\*" >nul 2>&1'),
                CleanItem("网页缓存",
                          'del /f /s /q "%LocalAppData%\\Microsoft\\Windows\\INetCache\\*" >nul 2>&1'),
                CleanItem("Cookies",
                          'del /f /s /q "%LocalAppData%\\Microsoft\\Windows\\INetCookies\\*" >nul 2>&1'),
                CleanItem("缩略图缓存",
                          'del /f /s /q "%LocalAppData%\\Microsoft\\Windows\\Explorer\\thumbcache_*.db" >nul 2>&1'),
                CleanItem("D3D着色器缓存",
                          'del /f /s /q "%LocalAppData%\\Local\\D3DSCache\\*" >nul 2>&1'),
                CleanItem(".NET程序集缓存",
                          'rd /s /q "%WinDir%\\assembly\\NativeImages_v4.0.30319_32" >nul 2>&1 & rd /s /q "%WinDir%\\assembly\\NativeImages_v4.0.30319_64" >nul 2>&1'),
                CleanItem("传递优化缓存",
                          'del /f /s /q "%SystemRoot%\\SoftwareDistribution\\DeliveryOptimization\\*" >nul 2>&1'),
            ],
            self.SYSTEM_FILES: [
                CleanItem("过时的WinSxS文件",
                          'dism /Online /Cleanup-Image /StartComponentCleanup /ResetBase >nul 2>&1'),
                CleanItem("错误应用包",
                          'powershell -Command "Get-AppxPackage -AllUsers | Where-Object {$_.Status -eq \'Error\'} | Remove-AppxPackage -ErrorAction SilentlyContinue" >nul'),
                CleanItem("Windows日志",
                          'del /f /s /q "%SystemRoot%\\Logs\\*" >nul 2>&1'),
                CleanItem("Windows错误报告",
                          'del /f /s /q "%ProgramData%\\Microsoft\\Windows\\WER\\ReportQueue\\*" >nul 2>&1'),
                CleanItem("诊断数据",
                          'del /f /s /q "%ProgramData%\\Microsoft\\Diagnosis\\*" >nul 2>&1'),
                CleanItem("崩溃dmp文件",
                          'del /f /s /q "%SystemRoot%\\Minidump\\*.dmp" >nul 2>&1 & del /f /q "%SystemRoot%\\memory.dmp" >nul 2>&1'),
            ],
            self.TEMP_FILES: [
                CleanItem("Windows Defender扫描",
                          'del /f /s /q "%ProgramData%\\Microsoft\\Windows Defender\\Scans\\*" >nul 2>&1'),
                CleanItem("WinSxS临时文件",
                          'del /f /s /q "%SystemRoot%\\WinSxS\\Temp\\*" >nul 2>&1'),
                CleanItem("系统临时文件",
                          'del /f /s /q "%SystemRoot%\\Temp\\*" >nul 2>&1'),
                CleanItem("系统dmp文件",
                          'del /f /s /q "%SystemDrive%\\*.dmp" >nul 2>&1'),
                CleanItem("回收站",
                          'rd /s /q "%SystemDrive%\\$Recycle.bin" >nul 2>&1'),
                CleanItem("所有临时文件",
                          'del /f /s /q "%SystemDrive%\\Windows\\Temp\\*" >nul 2>&1 & del /f /s /q "%SystemRoot%\\Temp\\*" >nul 2>&1 & del /f /s /q "%TEMP%\\*" >nul 2>&1'),
                CleanItem("预读取文件",
                          'del /f /s /q "%SystemRoot%\\Prefetch\\*" >nul 2>&1'),
            ],
        }

    def get_categories(self):
        return [self.CACHE_FILES, self.SYSTEM_FILES, self.TEMP_FILES]

    def get_items(self, category):
        return self._commands.get(category, [])

    def execute_clean(self, item_name, timeout=60):
        for cat_items in self._commands.values():
            for item in cat_items:
                if item.name == item_name:
                    return self._run_command(item.command, timeout)
        return False, "未找到清理项目"

    def _run_command(self, command, timeout=60):
        try:
            result = subprocess.run(
                f'cmd /c "{command}"',
                capture_output=True,
                text=True,
                encoding='gbk',
                errors='ignore',
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=timeout
            )
            return result.returncode == 0, result.stderr if result.stderr else "成功"
        except subprocess.TimeoutExpired:
            return False, "命令执行超时"
        except Exception as e:
            return False, str(e)


class CleanItem:
    def __init__(self, name, command):
        self.name = name
        self.command = command