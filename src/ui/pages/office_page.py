from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QComboBox, QFrame, QMessageBox)
from PySide6.QtCore import Qt, QThread, Signal

from ...i18n import tr


class OfficePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("ContentPage")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)

        header = QLabel("📦 " + tr("office.header"))
        header.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 16px;")
        layout.addWidget(header)

        install_frame = QFrame()
        install_frame.setFrameStyle(QFrame.StyledPanel)
        install_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 8px;
                border: 1px solid #e9ecef;
            }
        """)
        install_layout = QVBoxLayout(install_frame)
        install_layout.setContentsMargins(20, 16, 20, 16)
        install_layout.setSpacing(12)

        install_title = QLabel(tr("office.install_title"))
        install_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        install_layout.addWidget(install_title)

        desc = QLabel(tr("office.install_desc"))
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 12px; color: #888;")
        install_layout.addWidget(desc)

        row1 = QHBoxLayout()
        row1.addWidget(QLabel(tr("office.version_label")))
        self.version_combo = QComboBox()
        self.version_combo.addItems([
            tr("office.version_365"),
            tr("office.version_2024"),
            tr("office.version_2021"),
            tr("office.version_2019"),
        ])
        self.version_combo.setMinimumWidth(150)
        row1.addWidget(self.version_combo)
        row1.addStretch()
        install_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel(tr("office.arch_label")))
        self.arch_combo = QComboBox()
        self.arch_combo.addItems([tr("office.arch_64"), tr("office.arch_32")])
        self.arch_combo.setMinimumWidth(150)
        row2.addWidget(self.arch_combo)
        row2.addStretch()
        install_layout.addLayout(row2)

        row3 = QHBoxLayout()
        row3.addWidget(QLabel(tr("office.type_label")))
        self.type_combo = QComboBox()
        self.type_combo.addItems([tr("office.type_all"), tr("office.type_basic")])
        self.type_combo.setMinimumWidth(150)
        row3.addWidget(self.type_combo)
        row3.addStretch()
        install_layout.addLayout(row3)

        self.install_btn = QPushButton(tr("office.install_btn"))
        self.install_btn.setMinimumHeight(40)
        self.install_btn.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                color: white;
                border: none;
                padding: 8px 24px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #40a9ff; }
            QPushButton:disabled { background-color: #CCC; color: #888; }
        """)
        self.install_btn.clicked.connect(self._install_office)
        install_layout.addWidget(self.install_btn)

        layout.addWidget(install_frame)

        layout.addSpacing(16)

        uninstall_frame = QFrame()
        uninstall_frame.setFrameStyle(QFrame.StyledPanel)
        uninstall_frame.setStyleSheet("""
            QFrame {
                background-color: #fff7e6;
                border-radius: 8px;
                border: 1px solid #ffd591;
            }
        """)
        uninstall_layout = QVBoxLayout(uninstall_frame)
        uninstall_layout.setContentsMargins(20, 16, 20, 16)
        uninstall_layout.setSpacing(12)

        uninstall_title = QLabel(tr("office.uninstall_title"))
        uninstall_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        uninstall_layout.addWidget(uninstall_title)

        uninstall_desc = QLabel(tr("office.uninstall_desc"))
        uninstall_desc.setWordWrap(True)
        uninstall_desc.setStyleSheet("font-size: 12px; color: #888;")
        uninstall_layout.addWidget(uninstall_desc)

        self.uninstall_btn = QPushButton(tr("office.uninstall_btn"))
        self.uninstall_btn.setMinimumHeight(40)
        self.uninstall_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4d4f;
                color: white;
                border: none;
                padding: 8px 24px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #ff7875; }
            QPushButton:disabled { background-color: #CCC; color: #888; }
        """)
        self.uninstall_btn.clicked.connect(self._uninstall_office)
        uninstall_layout.addWidget(self.uninstall_btn)

        layout.addWidget(uninstall_frame)

        layout.addStretch()

    def _install_office(self):
        version = self.version_combo.currentText()
        architecture = self.arch_combo.currentText()
        install_type = self.type_combo.currentText()

        product_code = {
            "Office365": "O365ProPlusRetail",
            "Office2024": "ProPlus2024Retail",
            "Office2021": "ProPlus2021Retail",
            "Office2019": "ProPlus2019Retail",
        }.get(version)

        if not product_code:
            QMessageBox.warning(self, tr("office.error"), tr("office.unknown_version"))
            return

        arch = "64" if architecture == tr("office.arch_64") else "32"

        exclude = ""
        if install_type == tr("office.type_basic"):
            exclude = f"&exclude_apps={product_code}:Access,Bing,Groove,Lync,Outlook,OneNote,Publisher,Teams"

        url = f"https://www.coolhub.top/get/?prod_to_add={product_code}_zh-cn{exclude}&arch={arch}"

        reply = QMessageBox.question(
            self, tr("office.confirm_install_title"),
            tr("office.confirm_install", version=version, arch=arch, type=install_type),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        self.install_btn.setEnabled(False)
        self.install_btn.setText(tr("office.installing"))

        self.install_thread = InstallOfficeThread(url)
        self.install_thread.install_finished.connect(self._on_install_finished)
        self.install_thread.start()

    def _on_install_finished(self, success, message):
        self.install_btn.setEnabled(True)
        self.install_btn.setText(tr("office.install_btn"))
        if not success:
            QMessageBox.warning(self, tr("office.error"), f"{tr('office.start_ps_fail')}：{message}")

    def _uninstall_office(self):
        reply = QMessageBox.question(
            self, tr("common.confirm"),
            tr("office.confirm_uninstall"),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        self._set_controls_enabled(False)
        self.uninstall_btn.setText(tr("office.uninstalling"))

        self.uninstall_thread = UninstallOfficeThread()
        self.uninstall_thread.uninstall_finished.connect(self._on_uninstall_finished)
        self.uninstall_thread.start()

    def _on_uninstall_finished(self, success, message):
        self._set_controls_enabled(True)
        self.uninstall_btn.setText(tr("office.uninstall_btn"))
        if success:
            QMessageBox.information(self, tr("common.confirm"), tr("office.uninstall_done"))
        else:
            QMessageBox.warning(self, tr("office.error"), f"{tr('office.uninstall_fail')}: {message}")

    def _set_controls_enabled(self, enabled):
        self.version_combo.setEnabled(enabled)
        self.arch_combo.setEnabled(enabled)
        self.type_combo.setEnabled(enabled)
        self.install_btn.setEnabled(enabled)
        self.uninstall_btn.setEnabled(enabled)


class InstallOfficeThread(QThread):
    install_finished = Signal(bool, str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            import subprocess
            subprocess.Popen(
                f'powershell -NoExit -Command "irm \'{self.url}\' | iex"',
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            self.install_finished.emit(True, "")
        except Exception as e:
            self.install_finished.emit(False, str(e))


class UninstallOfficeThread(QThread):
    uninstall_finished = Signal(bool, str)

    def run(self):
        try:
            import subprocess
            import os

            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
            vbs_path = os.path.join(base_dir, "Bin", "UnInstallC2R.vbs")

            if os.path.exists(vbs_path):
                subprocess.run(
                    f'wscript.exe "{vbs_path}"',
                    capture_output=True, text=True,
                    encoding='gbk', errors='ignore',
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    timeout=300
                )
                self.uninstall_finished.emit(True, "")
            else:
                subprocess.run(
                    'powershell -Command "Get-CimInstance -Query \\"SELECT * FROM Win32_Product WHERE Name LIKE \'%Microsoft Office%\'\\" | ForEach-Object { Invoke-CimMethod -InputObject $_ -MethodName Uninstall }"',
                    capture_output=True, text=True,
                    encoding='gbk', errors='ignore',
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    timeout=300
                )
                self.uninstall_finished.emit(True, "")
        except subprocess.TimeoutExpired:
            self.uninstall_finished.emit(False, "卸载超时")
        except Exception as e:
            self.uninstall_finished.emit(False, str(e))