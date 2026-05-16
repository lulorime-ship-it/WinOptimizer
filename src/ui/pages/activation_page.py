from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QMessageBox)
from PySide6.QtCore import Qt, QThread, Signal

from ...i18n import tr


class ActivationPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("ContentPage")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)

        header = QLabel("🔑 " + tr("activation.header"))
        header.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 16px;")
        layout.addWidget(header)

        desc = QLabel(tr("activation.desc"))
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 13px; color: #666; margin-bottom: 12px;")
        layout.addWidget(desc)

        info_frame = QWidget()
        info_frame.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-radius: 8px;
                border: 1px solid #e9ecef;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(20, 16, 20, 16)
        info_layout.setSpacing(8)

        features = [
            "• " + tr("activation.feature_win10"),
            "• " + tr("activation.feature_hwid"),
            "• " + tr("activation.feature_kms"),
            "• " + tr("activation.feature_verify"),
        ]
        for f in features:
            fl = QLabel(f)
            fl.setStyleSheet("font-size: 13px; color: #333;")
            info_layout.addWidget(fl)

        layout.addWidget(info_frame)

        layout.addSpacing(12)

        link_label = QLabel('MAS 项目地址: <a href="https://github.com/cmontage/mas-cn">github.com/cmontage/mas-cn</a>')
        link_label.setOpenExternalLinks(True)
        link_label.setStyleSheet("font-size: 12px; color: #1890ff;")
        layout.addWidget(link_label)

        layout.addStretch()

        action_layout = QHBoxLayout()
        action_layout.addStretch()

        self.activate_btn = QPushButton("🚀 " + tr("activation.activate_btn"))
        self.activate_btn.setMinimumHeight(48)
        self.activate_btn.setMinimumWidth(200)
        self.activate_btn.clicked.connect(self._start_activation)
        self.activate_btn.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                color: white;
                border: none;
                padding: 12px 32px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover { background-color: #40a9ff; }
            QPushButton:disabled { background-color: #CCC; color: #888; }
        """)
        action_layout.addWidget(self.activate_btn)

        layout.addLayout(action_layout)

    def _start_activation(self):
        reply = QMessageBox.question(
            self, tr("common.confirm"),
            tr("activation.confirm"),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        self.activate_btn.setEnabled(False)
        self.activate_btn.setText(tr("activation.activating"))

        self.activate_thread = ActivateThread()
        self.activate_thread.activate_finished.connect(self._on_finished)
        self.activate_thread.start()

    def _on_finished(self, success, message):
        self.activate_btn.setEnabled(True)
        self.activate_btn.setText("🚀 " + tr("activation.activate_btn"))
        if success:
            QMessageBox.information(self, tr("common.confirm"), tr("activation.done"))
        else:
            QMessageBox.warning(self, tr("common.error"), f"{tr('activation.error')}：\n{message}")


class ActivateThread(QThread):
    activate_finished = Signal(bool, str)

    def run(self):
        try:
            import subprocess
            import os

            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
            bin_dir = os.path.join(base_dir, "Bin")
            cmd_path = os.path.join(bin_dir, "MAS_AIO_CN.cmd")

            if os.path.exists(cmd_path):
                subprocess.Popen(
                    f'cmd.exe /c "{cmd_path}"',
                    cwd=bin_dir,
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
                self.activate_finished.emit(True, "MAS 激活脚本已启动")
            else:
                ir_command = 'powershell -NoExit -Command "irm https://get.activated.win | iex"'
                subprocess.Popen(
                    ir_command,
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
                self.activate_finished.emit(True, "MAS 在线激活脚本已启动")

        except Exception as e:
            self.activate_finished.emit(False, str(e))