import sys
import os
import json
import ctypes

from PySide6.QtWidgets import QApplication
from src.i18n import get_config, save_config
from src.ui.main_window import MainWindow


DEFER_ADMIN_FLAG = "--defer-admin"


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def run_as_admin():
    try:
        python_exe = sys.executable
        script_path = os.path.abspath(sys.argv[0])
        cwd = os.path.abspath(os.getcwd())

        params = f'/c cd /d "{cwd}" && "{python_exe}" "{script_path}" {DEFER_ADMIN_FLAG}'
        ret = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", "cmd.exe", params, None, 1
        )
        if ret <= 32:
            error_codes = {
                2: "File not found",
                3: "Path not found",
                5: "Access denied",
                11: "Invalid EXE",
                26: "Sharing violation",
                27: "Incomplete file name association",
                29: "DDE transaction failed",
                30: "DDE transaction timeout",
                31: "DLL not found",
                32: "No associated application",
            }
            return False, error_codes.get(ret, f"Unknown error (code {ret})")
        return True, ""
    except Exception as e:
        return False, str(e)


def _ensure_user_config():
    user_cfg_dir = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "WinOptimizer")
    user_cfg = os.path.join(user_cfg_dir, "config.json")
    if not os.path.exists(user_cfg_dir):
        os.makedirs(user_cfg_dir, exist_ok=True)
    if not os.path.exists(user_cfg):
        try:
            config = get_config()
            with open(user_cfg, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
        except Exception:
            pass


def main():
    _ensure_user_config()
    config = get_config()
    require_admin = config.get("settings", {}).get("require_admin", True)

    if require_admin and DEFER_ADMIN_FLAG not in sys.argv and not is_admin():
        success, error = run_as_admin()
        if not success:
            from PySide6.QtWidgets import QMessageBox
            app = QApplication(sys.argv)
            QMessageBox.critical(
                None, "Permission Error",
                f"Administrator privileges are required to run this application.\n\n"
                f"Please right-click and run as administrator.\n\nError: {error}"
            )
            sys.exit(1)
        sys.exit(0)

    app = QApplication(sys.argv)
    app.setApplicationName("WinOptimizer")
    app.setOrganizationName("WinOptimizer")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()