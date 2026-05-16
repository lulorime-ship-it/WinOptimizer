from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QCheckBox, QFrame, QMessageBox)
from PySide6.QtCore import Qt, QThread, Signal
from ...i18n import tr


class EdgePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("ContentPage")
        self._init_ui()
        self._check_status()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)

        header = QLabel("\U0001f310 " + tr("edge.header"))
        header.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 16px;")
        layout.addWidget(header)

        desc = QLabel(tr("edge.desc"))
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 13px; color: #666; margin-bottom: 12px;")
        layout.addWidget(desc)

        edge_frame = QFrame()
        edge_frame.setFrameStyle(QFrame.StyledPanel)
        edge_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 8px;
                border: 1px solid #e9ecef;
            }
        """)
        edge_layout = QVBoxLayout(edge_frame)
        edge_layout.setContentsMargins(20, 16, 20, 16)
        edge_layout.setSpacing(12)

        edge_title = QLabel(tr("edge.status_title"))
        edge_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        edge_layout.addWidget(edge_title)

        row1 = QHBoxLayout()
        self.edge_status_label = QLabel(tr("edge.checking"))
        self.edge_status_label.setStyleSheet("font-size: 13px; color: #999;")
        row1.addWidget(self.edge_status_label)
        row1.addStretch()
        self.edge_version_label = QLabel(tr("edge.version_prefix") + tr("edge.checking"))
        self.edge_version_label.setStyleSheet("font-size: 12px; color: #999;")
        row1.addWidget(self.edge_version_label)
        self.uninstall_edge_btn = QPushButton(tr("edge.uninstall_edge"))
        self.uninstall_edge_btn.setMinimumHeight(32)
        self.uninstall_edge_btn.setEnabled(False)
        self.uninstall_edge_btn.setStyleSheet("""
            QPushButton { background-color: #ff4d4f; color: white; border: none; padding: 6px 16px; border-radius: 4px; font-size: 12px; }
            QPushButton:hover { background-color: #ff7875; }
            QPushButton:disabled { background-color: #CCC; color: #888; }
        """)
        self.uninstall_edge_btn.clicked.connect(lambda: self._uninstall_component("Edge"))
        row1.addWidget(self.uninstall_edge_btn)
        edge_layout.addLayout(row1)

        row2 = QHBoxLayout()
        self.webview_status_label = QLabel(tr("edge.checking"))
        self.webview_status_label.setStyleSheet("font-size: 13px; color: #999;")
        row2.addWidget(self.webview_status_label)
        row2.addStretch()
        self.webview_version_label = QLabel(tr("edge.version_prefix") + tr("edge.checking"))
        self.webview_version_label.setStyleSheet("font-size: 12px; color: #999;")
        row2.addWidget(self.webview_version_label)
        self.uninstall_webview_btn = QPushButton(tr("edge.uninstall_webview"))
        self.uninstall_webview_btn.setMinimumHeight(32)
        self.uninstall_webview_btn.setEnabled(False)
        self.uninstall_webview_btn.setStyleSheet("""
            QPushButton { background-color: #ff4d4f; color: white; border: none; padding: 6px 16px; border-radius: 4px; font-size: 12px; }
            QPushButton:hover { background-color: #ff7875; }
            QPushButton:disabled { background-color: #CCC; color: #888; }
        """)
        self.uninstall_webview_btn.clicked.connect(lambda: self._uninstall_component("Edge WebView"))
        row2.addWidget(self.uninstall_webview_btn)
        edge_layout.addLayout(row2)

        row3 = QHBoxLayout()
        self.core_status_label = QLabel(tr("edge.checking"))
        self.core_status_label.setStyleSheet("font-size: 13px; color: #999;")
        row3.addWidget(self.core_status_label)
        row3.addStretch()
        self.core_version_label = QLabel(tr("edge.version_prefix") + tr("edge.checking"))
        self.core_version_label.setStyleSheet("font-size: 12px; color: #999;")
        row3.addWidget(self.core_version_label)
        self.uninstall_core_btn = QPushButton(tr("edge.uninstall_core"))
        self.uninstall_core_btn.setMinimumHeight(32)
        self.uninstall_core_btn.setEnabled(False)
        self.uninstall_core_btn.setStyleSheet("""
            QPushButton { background-color: #ff4d4f; color: white; border: none; padding: 6px 16px; border-radius: 4px; font-size: 12px; }
            QPushButton:hover { background-color: #ff7875; }
            QPushButton:disabled { background-color: #CCC; color: #888; }
        """)
        self.uninstall_core_btn.clicked.connect(lambda: self._uninstall_component("Edge Core"))
        row3.addWidget(self.uninstall_core_btn)
        edge_layout.addLayout(row3)

        layout.addWidget(edge_frame)

        layout.addSpacing(12)

        uninstall_all_frame = QFrame()
        uninstall_all_frame.setStyleSheet("""
            QFrame {
                background-color: #fff2f0;
                border-radius: 8px;
                border: 1px solid #ffccc7;
            }
        """)
        uninstall_all_layout = QHBoxLayout(uninstall_all_frame)
        uninstall_all_layout.setContentsMargins(20, 12, 20, 12)

        warn_label = QLabel("\u26a0 " + tr("edge.uninstall_all_label"))
        warn_label.setStyleSheet("font-size: 12px; color: #cf1322;")
        uninstall_all_layout.addWidget(warn_label)
        uninstall_all_layout.addStretch()

        self.uninstall_all_btn = QPushButton(tr("edge.uninstall_all"))
        self.uninstall_all_btn.setMinimumHeight(38)
        self.uninstall_all_btn.setEnabled(False)
        self.uninstall_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #cf1322; color: white; border: none;
                padding: 6px 20px; border-radius: 6px; font-weight: bold; font-size: 13px;
            }
            QPushButton:hover { background-color: #ff4d4f; }
            QPushButton:disabled { background-color: #CCC; color: #888; }
        """)
        self.uninstall_all_btn.clicked.connect(lambda: self._uninstall_component("\u6240\u6709 Edge \u7ec4\u4ef6"))
        uninstall_all_layout.addWidget(self.uninstall_all_btn)

        layout.addWidget(uninstall_all_frame)

        layout.addSpacing(12)

        service_frame = QFrame()
        service_frame.setFrameStyle(QFrame.StyledPanel)
        service_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 8px;
                border: 1px solid #e9ecef;
            }
        """)
        service_layout = QHBoxLayout(service_frame)
        service_layout.setContentsMargins(20, 12, 20, 12)

        self.service_checkbox = QCheckBox(tr("edge.service_disable"))
        self.service_checkbox.setStyleSheet("font-size: 13px; color: #333;")
        self.service_checkbox.setEnabled(False)
        self.service_checkbox.stateChanged.connect(self._on_service_checkbox_changed)
        service_layout.addWidget(self.service_checkbox)
        service_layout.addStretch()

        layout.addWidget(service_frame)

        layout.addStretch()

    def _check_status(self):
        self.status_thread = CheckEdgeThread()
        self.status_thread.status_ready.connect(self._on_status_ready)
        self.status_thread.start()

    def _on_status_ready(self, status):
        for key, info in status.items():
            label_map = {
                "edge": self.edge_status_label,
                "webview": self.webview_status_label,
                "core": self.core_status_label,
            }
            version_map = {
                "edge": self.edge_version_label,
                "webview": self.webview_version_label,
                "core": self.core_version_label,
            }
            btn_map = {
                "edge": self.uninstall_edge_btn,
                "webview": self.uninstall_webview_btn,
                "core": self.uninstall_core_btn,
            }

            if key not in label_map:
                continue

            label = label_map.get(key)
            version = version_map.get(key)
            btn = btn_map.get(key)

            if info["is_installed"]:
                label.setText("\u2705 " + info["display_name"])
                label.setStyleSheet("font-size: 13px; color: #52c41a;")
                if version:
                    version.setText(tr("edge.version_prefix") + info.get("version", "N/A"))
                if btn:
                    btn.setEnabled(True)
            else:
                label.setText("\u274c " + info["display_name"])
                label.setStyleSheet("font-size: 13px; color: #ff4d4f;")
                if version:
                    version.setText(tr("edge.no_version"))
                if btn:
                    btn.setEnabled(False)

        any_installed = any(
            info["is_installed"]
            for key, info in status.items()
            if key in ("edge", "webview", "core")
        )
        self.uninstall_all_btn.setEnabled(any_installed)

        if status.get("service_exists"):
            self.service_checkbox.setEnabled(True)
            self.service_checkbox.setChecked(status.get("service_disabled", False))
        else:
            self.service_checkbox.setEnabled(False)
            self.service_checkbox.setChecked(False)

    def _uninstall_component(self, component_name):
        reply = QMessageBox.question(
            self, tr("edge.confirm_title"),
            tr("edge.confirm", name=component_name),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        self._set_buttons_enabled(False)

        self.uninstall_thread = EdgeUninstallThread(component_name)
        self.uninstall_thread.uninstall_finished.connect(self._on_uninstall_finished)
        self.uninstall_thread.start()

    def _on_uninstall_finished(self, success, message):
        self._set_buttons_enabled(True)
        if success:
            QMessageBox.information(self, tr("common.confirm"), tr("edge.complete", name=message))
        else:
            QMessageBox.warning(self, tr("edge.error"), tr("edge.exec_error") + ": " + message)
        self._check_status()

    def _set_buttons_enabled(self, enabled):
        self.uninstall_edge_btn.setEnabled(enabled)
        self.uninstall_webview_btn.setEnabled(enabled)
        self.uninstall_core_btn.setEnabled(enabled)
        self.uninstall_all_btn.setEnabled(enabled)
        self.service_checkbox.setEnabled(enabled)

    def _on_service_checkbox_changed(self, state):
        import subprocess

        if state == Qt.Checked.value:
            cmd = 'sc config edgeupdate start= disabled'
            msg = tr("edge.service_disabled")
        else:
            cmd = 'sc config edgeupdate start= auto'
            msg = tr("edge.service_enabled")

        self._set_buttons_enabled(False)
        try:
            subprocess.run(
                cmd, capture_output=True, text=True,
                encoding='gbk', errors='ignore',
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            QMessageBox.information(self, tr("common.confirm"), msg)
        except Exception as e:
            QMessageBox.warning(self, tr("edge.error"), tr("edge.exec_error") + ": " + str(e))
        finally:
            self._set_buttons_enabled(True)
            self._check_status()


class CheckEdgeThread(QThread):
    status_ready = Signal(dict)

    def run(self):
        import os
        import subprocess
        import re

        status = {}

        is_64bit = os.environ.get("PROCESSOR_ARCHITEW6432") == "AMD64" or os.environ.get(
            "PROCESSOR_ARCHITECTURE") == "AMD64"
        program_files = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)") if is_64bit else os.environ.get(
            "ProgramFiles", r"C:\Program Files")

        components = {
            "edge": ("Microsoft Edge", os.path.join(program_files, "Microsoft", "Edge", "Application")),
            "webview": ("Edge WebView", os.path.join(program_files, "Microsoft", "EdgeWebView", "Application")),
            "core": ("Edge Core", os.path.join(program_files, "Microsoft", "EdgeCore")),
        }

        version_pattern = re.compile(r"^\d+\.\d+\.\d+\.\d+$")

        for key, (display_name, base_path) in components.items():
            info = {"display_name": display_name, "is_installed": False, "version": ""}

            if os.path.isdir(base_path):
                versions = []
                for d in os.listdir(base_path):
                    d_path = os.path.join(base_path, d)
                    if os.path.isdir(d_path) and version_pattern.match(d):
                        versions.append(d)

                if versions:
                    versions.sort(key=lambda v: [int(x) for x in v.split(".")], reverse=True)
                    latest = versions[0]
                    installer_dir = os.path.join(base_path, latest, "Installer")
                    setup_exe = os.path.join(installer_dir, "setup.exe")
                    if os.path.isdir(installer_dir) and os.path.isfile(setup_exe):
                        info["is_installed"] = True
                        info["version"] = latest

            status[key] = info

        r = subprocess.run(
            "sc query edgeupdate", capture_output=True, text=True,
            encoding='gbk', errors='ignore',
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        status["service_exists"] = r.returncode == 0

        if status["service_exists"]:
            r2 = subprocess.run(
                "sc qc edgeupdate", capture_output=True, text=True,
                encoding='gbk', errors='ignore',
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            status["service_disabled"] = "DISABLED" in (r2.stdout or "").upper()
        else:
            status["service_disabled"] = False

        self.status_ready.emit(status)


class EdgeUninstallThread(QThread):
    uninstall_finished = Signal(bool, str)

    def __init__(self, component_name):
        super().__init__()
        self.component_name = component_name

    def run(self):
        import os
        import subprocess

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

        bat_map = {
            "Edge": "Edge\\Edge.bat",
            "Edge WebView": "Edge\\EdgeWebView2.bat",
            "Edge Core": "Edge\\EdgeCore.bat",
            "\u6240\u6709 Edge \u7ec4\u4ef6": "Edge\\All.bat",
        }

        bat_file = bat_map.get(self.component_name)
        if not bat_file:
            self.uninstall_finished.emit(False, tr("edge.unknown") + ": " + self.component_name)
            return

        bat_path = os.path.join(base_dir, "Bin", bat_file)

        try:
            if os.path.exists(bat_path):
                import subprocess
                r = subprocess.run(
                    f'cmd.exe /c "{bat_path}"',
                    capture_output=True, text=True,
                    encoding='gbk', errors='ignore',
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    timeout=120
                )
                self.uninstall_finished.emit(r.returncode == 0, self.component_name)
            else:
                self._fallback_uninstall()

        except subprocess.TimeoutExpired:
            self.uninstall_finished.emit(False, tr("edge.timeout"))
        except Exception as e:
            self.uninstall_finished.emit(False, str(e))

    def _fallback_uninstall(self):
        import subprocess

        component = self.component_name

        uninstall_paths = {
            "Edge": r'"%ProgramFiles(x86)%\Microsoft\Edge\Application\*\Installer\setup.exe" --uninstall --force-uninstall --system-level',
            "Edge WebView": r'"%ProgramFiles(x86)%\Microsoft\EdgeWebView\Application\*\Installer\setup.exe" --uninstall --msedgewebview --force-uninstall --system-level',
            "Edge Core": r'"%ProgramFiles(x86)%\Microsoft\EdgeCore\*\Installer\setup.exe" --uninstall --force-uninstall --system-level',
        }

        cmd = uninstall_paths.get(component)
        if cmd:
            r = subprocess.run(
                cmd, capture_output=True, text=True,
                encoding='gbk', errors='ignore',
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=120
            )
            self.uninstall_finished.emit(r.returncode == 0, component)
        else:
            self.uninstall_finished.emit(False, tr("edge.not_found"))