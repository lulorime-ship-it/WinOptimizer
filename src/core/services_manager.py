import subprocess
import winreg
from ..utils.system_utils import SystemUtils

class ServicesManager:
    def __init__(self):
        self.services_info = {
            'DiagTrack': {'name': '诊断跟踪服务', 'description': '遥测数据收集', 'recommended': 'disabled'},
            'wscsvc': {'name': 'Windows安全中心', 'description': '安全中心服务', 'recommended': 'auto'},
            'WinDefend': {'name': 'Windows Defender', 'description': 'Windows Defender服务', 'recommended': 'auto'},
            'Spooler': {'name': '打印后台处理', 'description': '打印机服务', 'recommended': 'auto'},
            'BITS': {'name': '后台智能传输', 'description': '后台传输服务', 'recommended': 'auto'},
            'WSearch': {'name': 'Windows搜索', 'description': '索引服务', 'recommended': 'auto'},
            'wuauserv': {'name': 'Windows更新', 'description': '自动更新服务', 'recommended': 'disabled'},
            'Themes': {'name': '主题服务', 'description': '主题支持', 'recommended': 'auto'},
            'BluetoothSupportService': {'name': '蓝牙支持服务', 'description': '蓝牙支持', 'recommended': 'disabled'},
            'TabletInputService': {'name': '触摸键盘和手写板', 'description': '触摸输入服务', 'recommended': 'disabled'},
        }

    def get_services(self):
        services = []
        for service_name, info in self.services_info.items():
            status = self._get_service_status(service_name)
            start_type = self._get_service_start_type(service_name)
            services.append({
                'name': service_name,
                'display_name': info['name'],
                'description': info['description'],
                'status': status,
                'start_type': start_type,
                'recommended': info['recommended']
            })
        return services

    def _get_service_status(self, service_name):
        cmd = f'sc query {service_name}'
        success, stdout, _ = SystemUtils.run_command(cmd)
        if success and stdout:
            if 'RUNNING' in stdout:
                return 'Running'
            elif 'STOPPED' in stdout:
                return 'Stopped'
        return 'Unknown'

    def _get_service_start_type(self, service_name):
        cmd = f'sc qc {service_name}'
        success, stdout, _ = SystemUtils.run_command(cmd)
        if success and stdout:
            if 'AUTO_START' in stdout:
                return 'Auto'
            elif 'DEMAND_START' in stdout:
                return 'Manual'
            elif 'DISABLED' in stdout:
                return 'Disabled'
        return 'Unknown'

    def set_service_start_type(self, service_name, start_type):
        type_map = {
            'Auto': 'auto',
            'Manual': 'demand',
            'Disabled': 'disabled'
        }
        sc_type = type_map.get(start_type, 'demand')
        cmd = f'sc config {service_name} start= {sc_type}'
        success, _, _ = SystemUtils.run_command(cmd)
        return success

    def start_service(self, service_name):
        cmd = f'net start {service_name}'
        success, _, _ = SystemUtils.run_command(cmd)
        return success

    def stop_service(self, service_name):
        cmd = f'net stop {service_name}'
        success, _, _ = SystemUtils.run_command(cmd)
        return success
