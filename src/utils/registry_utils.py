import winreg
import ctypes

class RegistryUtils:
    @staticmethod
    def read_value(hive, path, name):
        try:
            key = winreg.OpenKey(hive, path)
            value, _ = winreg.QueryValueEx(key, name)
            winreg.CloseKey(key)
            return value
        except WindowsError:
            return None

    @staticmethod
    def write_value(hive, path, name, value, value_type=winreg.REG_SZ):
        try:
            key = winreg.CreateKey(hive, path)
            winreg.SetValueEx(key, name, 0, value_type, value)
            winreg.CloseKey(key)
            return True
        except WindowsError:
            return False

    @staticmethod
    def delete_value(hive, path, name):
        try:
            key = winreg.OpenKey(hive, path, 0, winreg.KEY_WRITE)
            winreg.DeleteValue(key, name)
            winreg.CloseKey(key)
            return True
        except WindowsError:
            return False

    @staticmethod
    def key_exists(hive, path):
        try:
            key = winreg.OpenKey(hive, path)
            winreg.CloseKey(key)
            return True
        except WindowsError:
            return False
