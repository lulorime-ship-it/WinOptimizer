from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QLineEdit, QTextEdit, QGroupBox,
                             QMessageBox, QProgressBar)
from PySide6.QtCore import Qt, QThread, Signal
from ..core.activator import Activator

class ActivationPage(QWidget):
    def __init__(self):
        super().__init__()
        self.activator = Activator()
        self.init_ui()
        self.check_status()

    def init_ui(self):
        layout = QVBoxLayout()

        header = QLabel("系统激活")
        header.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        layout.addWidget(header)

        status_group = QGroupBox("激活状态")
        status_layout = QVBoxLayout()

        self.windows_status_label = QLabel("Windows: 检查中...")
        status_layout.addWidget(self.windows_status_label)

        self.office_status_label = QLabel("Office: 检查中...")
        status_layout.addWidget(self.office_status_label)

        status_group.setLayout(status_layout)
        layout.addWidget(status_group)

        windows_group = QGroupBox("Windows 激活")
        windows_layout = QVBoxLayout()

        key_layout = QHBoxLayout()
        key_layout.addWidget(QLabel("产品密钥:"))
        self.windows_key_input = QLineEdit()
        self.windows_key_input.setPlaceholderText("输入 Windows 产品密钥（可选）")
        key_layout.addWidget(self.windows_key_input)
        windows_layout.addLayout(key_layout)

        self.activate_windows_btn = QPushButton("激活 Windows")
        self.activate_windows_btn.clicked.connect(self.activate_windows)
        self.activate_windows_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        windows_layout.addWidget(self.activate_windows_btn)

        windows_group.setLayout(windows_layout)
        layout.addWidget(windows_group)

        office_group = QGroupBox("Office 激活")
        office_layout = QVBoxLayout()

        self.activate_office_btn = QPushButton("激活 Office")
        self.activate_office_btn.clicked.connect(self.activate_office)
        self.activate_office_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        office_layout.addWidget(self.activate_office_btn)

        office_group.setLayout(office_layout)
        layout.addWidget(office_group)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        layout.addWidget(QLabel("激活日志:"))
        layout.addWidget(self.log_text)

        layout.addStretch()

        self.setLayout(layout)

    def check_status(self):
        status = self.activator.get_activation_status()

        windows_status = status['windows']
        self.windows_status_label.setText(f"Windows: {windows_status['status']}")

        office_status = status['office']
        self.office_status_label.setText(f"Office: {office_status['status']}")

    def activate_windows(self):
        product_key = self.windows_key_input.text().strip() or None
        self.activate_windows_btn.setEnabled(False)
        self.log_text.clear()
        self.log_text.append("正在激活 Windows...")

        self.windows_thread = ActivateWindowsThread(self.activator, product_key)
        self.windows_thread.windows_finished.connect(self.windows_activation_finished)
        self.windows_thread.start()

    def windows_activation_finished(self, success, message):
        self.activate_windows_btn.setEnabled(True)
        self.log_text.append(message)
        if success:
            QMessageBox.information(self, "成功", message)
        else:
            QMessageBox.warning(self, "失败", message)
        self.check_status()

    def activate_office(self):
        self.activate_office_btn.setEnabled(False)
        self.log_text.clear()
        self.log_text.append("正在激活 Office...")

        self.office_thread = ActivateOfficeThread(self.activator)
        self.office_thread.office_finished.connect(self.office_activation_finished)
        self.office_thread.start()

    def office_activation_finished(self, success, message):
        self.activate_office_btn.setEnabled(True)
        self.log_text.append(message)
        if success:
            QMessageBox.information(self, "成功", message)
        else:
            QMessageBox.warning(self, "失败", message)
        self.check_status()

class ActivateWindowsThread(QThread):
    windows_finished = Signal(bool, str)

    def __init__(self, activator, product_key):
        super().__init__()
        self.activator = activator
        self.product_key = product_key

    def run(self):
        success, message = self.activator.activate_windows(self.product_key)
        self.windows_finished.emit(success, message)

class ActivateOfficeThread(QThread):
    office_finished = Signal(bool, str)

    def __init__(self, activator):
        super().__init__()
        self.activator = activator

    def run(self):
        success, message = self.activator.activate_office()
        self.office_finished.emit(success, message)
