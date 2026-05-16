import platform
import os
import winreg
from pathlib import Path
import subprocess

class SystemUtils:
    @staticmethod
    def get_os_version():
        return platform.platform()

    @staticmethod
    def get_windows_version():
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows NT\CurrentVersion')
            version = winreg.QueryValueEx(reg_key, 'CurrentBuild')[0]
            winreg.CloseKey(reg_key)
            return f"Windows {version}"
        except:
            return "Unknown Windows Version"

    @staticmethod
    def get_system_info():
        return {
            'os': SystemUtils.get_os_version(),
            'windows_version': SystemUtils.get_windows_version(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
        }

    @staticmethod
    def run_command(command, shell=True):
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                encoding='gbk',
                errors='ignore',
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)

    @staticmethod
    def run_as_admin(command):
        try:
            import ctypes
            ret = ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", f"/c {command}", None, 1)
            return ret > 32
        except Exception as e:
            return False

    @staticmethod
    def check_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
