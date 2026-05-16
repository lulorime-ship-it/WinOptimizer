from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QFrame, QMessageBox)
from PySide6.QtCore import Qt, QThread, Signal
from ...i18n import tr


class DefenderPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("ContentPage")
        self._init_ui()
        self._refresh_status()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)

        header = QLabel("\U0001f6e1\ufe0f " + tr("defender.header"))
        header.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 16px;")
        layout.addWidget(header)

        status_frame = QFrame()
        status_frame.setFrameStyle(QFrame.StyledPanel)
        status_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 8px;
                border: 1px solid #e9ecef;
            }
        """)
        status_layout = QVBoxLayout(status_frame)
        status_layout.setContentsMargins(20, 16, 20, 16)
        status_layout.setSpacing(12)

        status_title = QLabel(tr("defender.status_title"))
        status_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        status_layout.addWidget(status_title)

        self.defend_exists_label = QLabel(tr("defender.checking") + " Defender 服务...")
        self.defend_exists_label.setStyleSheet("font-size: 13px; padding: 4px 0;")
        status_layout.addWidget(self.defend_exists_label)

        self.defend_enabled_label = QLabel(tr("defender.checking") + " Defender 启用状态...")
        self.defend_enabled_label.setStyleSheet("font-size: 13px; padding: 4px 0;")
        status_layout.addWidget(self.defend_enabled_label)

        self.defend_running_label = QLabel(tr("defender.checking") + " Defender 运行状态...")
        self.defend_running_label.setStyleSheet("font-size: 13px; padding: 4px 0;")
        status_layout.addWidget(self.defend_running_label)

        self.security_center_label = QLabel(tr("defender.checking") + " 安全中心状态...")
        self.security_center_label.setStyleSheet("font-size: 13px; padding: 4px 0;")
        status_layout.addWidget(self.security_center_label)

        layout.addWidget(status_frame)

        layout.addSpacing(16)

        warn_frame = QFrame()
        warn_frame.setStyleSheet("""
            QFrame {
                background-color: #fff7e6;
                border: 1px solid #ffd591;
                border-radius: 6px;
            }
        """)
        warn_layout = QVBoxLayout(warn_frame)
        warn_layout.setContentsMargins(16, 12, 16, 12)
        warn_label = QLabel("\u26a0 " + tr("defender.warn"))
        warn_label.setWordWrap(True)
        warn_label.setStyleSheet("font-size: 13px; color: #d46b08;")
        warn_layout.addWidget(warn_label)
        layout.addWidget(warn_frame)

        layout.addStretch()

        action_layout = QHBoxLayout()
        action_layout.addStretch()

        self.disable_btn = QPushButton("\U0001f6d1 " + tr("defender.disable_btn"))
        self.disable_btn.setMinimumHeight(44)
        self.disable_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4d4f;
                color: white;
                border: none;
                padding: 10px 24px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #ff7875; }
            QPushButton:disabled { background-color: #CCC; color: #888; }
        """)
        self.disable_btn.clicked.connect(self._disable_defender)
        action_layout.addWidget(self.disable_btn)

        self.enable_btn = QPushButton("\u2705 " + tr("defender.enable_btn"))
        self.enable_btn.setMinimumHeight(44)
        self.enable_btn.setStyleSheet("""
            QPushButton {
                background-color: #52c41a;
                color: white;
                border: none;
                padding: 10px 24px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #73d13d; }
            QPushButton:disabled { background-color: #CCC; color: #888; }
        """)
        self.enable_btn.clicked.connect(self._enable_defender)
        action_layout.addWidget(self.enable_btn)

        layout.addLayout(action_layout)

    def _refresh_status(self):
        self.status_thread = CheckDefenderThread()
        self.status_thread.status_ready.connect(self._on_status_ready)
        self.status_thread.start()

    def _on_status_ready(self, status):
        if status.get("win_defend_exists"):
            self.defend_exists_label.setText("\u2705 " + tr("defender.exists"))
            self.defend_exists_label.setStyleSheet("font-size: 13px; color: #52c41a; padding: 4px 0;")
            self.disable_btn.setEnabled(True)
            self.enable_btn.setEnabled(True)
        else:
            self.defend_exists_label.setText("\u274c " + tr("defender.not_exists"))
            self.defend_exists_label.setStyleSheet("font-size: 13px; color: #ff4d4f; padding: 4px 0;")
            self.defend_enabled_label.setText("")
            self.defend_running_label.setText("")
            self.security_center_label.setText("")
            self.disable_btn.setEnabled(False)
            self.enable_btn.setEnabled(False)
            return

        is_disabled = status.get("win_defend_disabled", False)
        if is_disabled:
            self.defend_enabled_label.setText("\u274c " + tr("defender.not_enabled"))
            self.defend_enabled_label.setStyleSheet("font-size: 13px; color: #ff4d4f; padding: 4px 0;")
        else:
            self.defend_enabled_label.setText("\u2705 " + tr("defender.enabled"))
            self.defend_enabled_label.setStyleSheet("font-size: 13px; color: #52c41a; padding: 4px 0;")

        is_running = status.get("win_defend_running", False)
        if is_running:
            self.defend_running_label.setText("\u2705 " + tr("defender.running"))
            self.defend_running_label.setStyleSheet("font-size: 13px; color: #52c41a; padding: 4px 0;")
        else:
            self.defend_running_label.setText("\u274c " + tr("defender.not_running"))
            self.defend_running_label.setStyleSheet("font-size: 13px; color: #ff4d4f; padding: 4px 0;")

        security_disabled = status.get("security_center_disabled", False)
        if security_disabled:
            self.security_center_label.setText("\u274c " + tr("defender.security_disabled"))
            self.security_center_label.setStyleSheet("font-size: 13px; color: #ff4d4f; padding: 4px 0;")
        else:
            self.security_center_label.setText("\u2705 " + tr("defender.security_enabled"))
            self.security_center_label.setStyleSheet("font-size: 13px; color: #52c41a; padding: 4px 0;")

    def _set_buttons_enabled(self, enabled):
        self.disable_btn.setEnabled(enabled)
        self.enable_btn.setEnabled(enabled)

    def _disable_defender(self):
        reply = QMessageBox.question(
            self, tr("common.confirm"),
            tr("defender.confirm_disable"),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        self._set_buttons_enabled(False)
        self._set_labels_disabling()

        self.action_thread = DefenderActionThread("disable")
        self.action_thread.action_finished.connect(self._on_action_finished)
        self.action_thread.start()

    def _enable_defender(self):
        reply = QMessageBox.question(
            self, tr("common.confirm"),
            tr("defender.confirm_enable"),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        self._set_buttons_enabled(False)
        self._set_labels_disabling()

        self.action_thread = DefenderActionThread("enable")
        self.action_thread.action_finished.connect(self._on_action_finished)
        self.action_thread.start()

    def _set_labels_disabling(self):
        self.defend_exists_label.setText("\u23f3 " + tr("defender.operating"))
        self.defend_exists_label.setStyleSheet("font-size: 13px; color: #faad14; padding: 4px 0;")
        self.defend_enabled_label.setText("")
        self.defend_running_label.setText("")
        self.security_center_label.setText("")

    def _on_action_finished(self, success, message):
        self._set_buttons_enabled(True)
        if success:
            QMessageBox.information(
                self, tr("common.confirm"),
                message + "\n\n" + tr("defender.restart")
            )
        else:
            QMessageBox.warning(self, tr("defender.error"), message)
        self._refresh_status()


class CheckDefenderThread(QThread):
    status_ready = Signal(dict)

    def run(self):
        status = {
            "win_defend_exists": False,
            "win_defend_disabled": False,
            "win_defend_running": False,
            "security_center_disabled": False,
        }

        try:
            import subprocess
            import winreg

            r = subprocess.run(
                'sc query WinDefend', capture_output=True, text=True,
                encoding='gbk', errors='ignore', creationflags=subprocess.CREATE_NO_WINDOW
            )
            if r.returncode == 0:
                status["win_defend_exists"] = True

            r = subprocess.run(
                'sc qc WinDefend', capture_output=True, text=True,
                encoding='gbk', errors='ignore', creationflags=subprocess.CREATE_NO_WINDOW
            )
            if "DISABLED" in (r.stdout or "").upper():
                status["win_defend_disabled"] = True

            r = subprocess.run(
                'sc query WinDefend', capture_output=True, text=True,
                encoding='gbk', errors='ignore', creationflags=subprocess.CREATE_NO_WINDOW
            )
            if "RUNNING" in (r.stdout or "").upper():
                status["win_defend_running"] = True

            try:
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SYSTEM\CurrentControlSet\Services\SecurityHealthService"
                )
                start_value, _ = winreg.QueryValueEx(key, "Start")
                winreg.CloseKey(key)
                if start_value == 4:
                    status["security_center_disabled"] = True
            except WindowsError:
                status["security_center_disabled"] = True

        except Exception:
            pass

        self.status_ready.emit(status)


class DefenderActionThread(QThread):
    action_finished = Signal(bool, str)

    def __init__(self, action):
        super().__init__()
        self.action = action

    def run(self):
        try:
            import subprocess

            if self.action == "disable":
                cmds = [
                    'sc stop WinDefend',
                    'sc config WinDefend start= disabled',
                    'sc stop SecurityHealthService',
                    'sc config SecurityHealthService start= disabled',
                ]
                for cmd in cmds:
                    subprocess.run(
                        cmd, capture_output=True, text=True,
                        encoding='gbk', errors='ignore',
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )

                subprocess.run(
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender" /v DisableAntiSpyware /t REG_DWORD /d 1 /f',
                    capture_output=True, text=True,
                    encoding='gbk', errors='ignore',
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

                self.action_finished.emit(True, tr("defender.disabled"))

            else:
                cmds = [
                    'sc config WinDefend start= auto',
                    'sc start WinDefend',
                    'sc config SecurityHealthService start= auto',
                    'sc start SecurityHealthService',
                ]
                for cmd in cmds:
                    subprocess.run(
                        cmd, capture_output=True, text=True,
                        encoding='gbk', errors='ignore',
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )

                subprocess.run(
                    'reg delete "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender" /v DisableAntiSpyware /f',
                    capture_output=True, text=True,
                    encoding='gbk', errors='ignore',
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

                self.action_finished.emit(True, tr("defender.enabled"))

        except Exception as e:
            self.action_finished.emit(False, tr("defender.error") + ": " + str(e))