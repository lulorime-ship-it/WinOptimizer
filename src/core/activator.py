import subprocess
from ..utils.system_utils import SystemUtils

class Activator:
    def __init__(self):
        self.activation_status = {
            'windows': self._check_windows_activation(),
            'office': self._check_office_activation()
        }

    def _check_windows_activation(self):
        cmd = 'slmgr /xpr'
        success, stdout, _ = SystemUtils.run_command(cmd)
        if success and stdout:
            stdout_lower = stdout.lower()
            if 'activated' in stdout_lower:
                return {'status': '已激活', 'licensed': True}
            elif 'licensed' in stdout_lower:
                return {'status': '已许可', 'licensed': True}
            else:
                return {'status': '未激活', 'licensed': False}
        return {'status': '检查失败', 'licensed': False}

    def _check_office_activation(self):
        paths = [
            r'C:\Program Files\Microsoft Office\Office16',
            r'C:\Program Files\Microsoft Office\Office15',
            r'C:\Program Files (x86)\Microsoft Office\Office16',
            r'C:\Program Files (x86)\Microsoft Office\Office15',
        ]

        for path in paths:
            if SystemUtils.run_command(f'dir "{path}"'):
                return {'status': '已安装', 'licensed': '未知'}
        return {'status': '未安装', 'licensed': False}

    def activate_windows(self, product_key=None):
        if product_key:
            cmd = f'slmgr /ipk {product_key}'
            success, _, _ = SystemUtils.run_command(cmd)
            if not success:
                return False, "密钥安装失败"

        cmd = 'slmgr /skms kms.example.com'
        success, _, _ = SystemUtils.run_command(cmd)
        if not success:
            return False, "KMS服务器设置失败"

        cmd = 'slmgr /ato'
        success, stdout, stderr = SystemUtils.run_command(cmd)
        if success:
            return True, "Windows激活成功"
        else:
            return False, f"激活失败: {stderr}"

    def activate_office(self):
        kms_servers = [
            'kms.example.com',
            'kms.example.net',
        ]

        office_paths = [
            r'C:\Program Files\Microsoft Office\Office16\ospp.vbs',
            r'C:\Program Files (x86)\Microsoft Office\Office16\ospp.vbs',
            r'C:\Program Files\Microsoft Office\Office15\ospp.vbs',
            r'C:\Program Files (x86)\Microsoft Office\Office15\ospp.vbs',
        ]

        for server in kms_servers:
            for path in office_paths:
                if SystemUtils.run_command(f'dir "{path}"'):
                    cmd = f'cscript "{path}" /sethst:{server}'
                    SystemUtils.run_command(cmd)

                    cmd = f'cscript "{path}" /act'
                    success, stdout, _ = SystemUtils.run_command(cmd)
                    if success:
                        return True, "Office激活成功"
                    return False, "Office激活失败"

        return False, "未找到Office安装路径"

    def get_activation_status(self):
        return self.activation_status
