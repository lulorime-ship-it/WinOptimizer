import subprocess
from ..utils.system_utils import SystemUtils

class UWPManager:
    def __init__(self):
        self.common_apps = [
            'Microsoft.549981C3F5F10',  # Cortana
            'Microsoft.BingNews',
            'Microsoft.BingWeather',
            'Microsoft.GamingApp',
            'Microsoft.GetHelp',
            'Microsoft.Getstarted',
            'Microsoft.MicrosoftOfficeHub',
            'Microsoft.MicrosoftSolitaireCollection',
            'Microsoft.People',
            'Microsoft.Photos',
            'Microsoft.PowerAutomateDesktop',
            'Microsoft.SkypeApp',
            'Microsoft.WindowsCamera',
            'Microsoft.WindowsMaps',
            'Microsoft.WindowsSoundRecorder',
            'Microsoft.Xbox.TCUI',
            'Microsoft.XboxApp',
            'Microsoft.XboxGameOverlay',
            'Microsoft.XboxGamingOverlay',
            'Microsoft.XboxIdentityProvider',
            'Microsoft.ZuneMusic',
            'Microsoft.ZuneVideo',
        ]

    def get_installed_apps(self):
        apps = []
        cmd = 'powershell -command "Get-AppxPackage | Select-Object Name, PackageFullName, Status"'
        success, stdout, _ = SystemUtils.run_command(cmd)

        if success:
            lines = stdout.strip().split('\n')
            for line in lines[3:]:
                parts = [p.strip() for p in line.split('|') if p.strip()]
                if len(parts) >= 2:
                    apps.append({
                        'name': parts[0],
                        'package': parts[1],
                        'status': parts[2] if len(parts) > 2 else 'Unknown'
                    })
        return apps

    def uninstall_app(self, package_name):
        cmd = f'powershell -command "Remove-AppxPackage -Package {package_name}"'
        success, stdout, stderr = SystemUtils.run_command(cmd)
        if success:
            return True, "卸载成功"
        else:
            return False, f"卸载失败: {stderr}"

    def install_app(self, package_name):
        cmd = f'powershell -command "Add-AppxPackage -Register "C:\\Program Files\\WindowsApps\\{package_name}\\AppxManifest.xml""'
        success, stdout, stderr = SystemUtils.run_command(cmd)
        if success:
            return True, "重新安装成功"
        else:
            return False, f"重新安装失败: {stderr}"

    def get_common_apps_info(self):
        installed = self.get_installed_apps()
        installed_names = {app['package'] for app in installed}

        apps_info = []
        for app_id in self.common_apps:
            is_installed = any(app_id in pkg for pkg in installed_names)
            apps_info.append({
                'id': app_id,
                'installed': is_installed,
                'can_uninstall': is_installed
            })
        return apps_info
