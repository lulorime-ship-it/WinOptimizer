from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QCheckBox, QGroupBox, QComboBox,
                             QFileDialog, QMessageBox)
from PySide6.QtCore import Qt
from ..core.config_manager import ConfigManager
from ..utils.system_utils import SystemUtils

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        layout = QVBoxLayout()

        header = QLabel("设置")
        header.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        layout.addWidget(header)

        general_group = QGroupBox("常规设置")
        general_layout = QVBoxLayout()

        self.auto_save_check = QCheckBox("自动保存配置")
        general_layout.addWidget(self.auto_save_check)

        self.backup_check = QCheckBox("优化前自动备份")
        general_layout.addWidget(self.backup_check)

        self.notifications_check = QCheckBox("显示通知")
        general_layout.addWidget(self.notifications_check)

        general_group.setLayout(general_layout)
        layout.addWidget(general_group)

        optimization_group = QGroupBox("优化设置")
        optimization_layout = QVBoxLayout()

        profile_layout = QHBoxLayout()
        profile_layout.addWidget(QLabel("优化预设:"))
        self.profile_combo = QComboBox()
        self.profile_combo.addItems(['快速优化', '平衡优化', '深度优化'])
        profile_layout.addWidget(self.profile_combo)
        optimization_layout.addLayout(profile_layout)

        optimization_group.setLayout(optimization_layout)
        layout.addWidget(optimization_group)

        config_group = QGroupBox("配置管理")
        config_layout = QVBoxLayout()

        config_btn_layout = QHBoxLayout()

        self.export_btn = QPushButton("导出配置")
        self.export_btn.clicked.connect(self.export_config)
        config_btn_layout.addWidget(self.export_btn)

        self.import_btn = QPushButton("导入配置")
        self.import_btn.clicked.connect(self.import_config)
        config_btn_layout.addWidget(self.import_btn)

        self.reset_btn = QPushButton("恢复默认")
        self.reset_btn.clicked.connect(self.reset_config)
        config_btn_layout.addWidget(self.reset_btn)

        config_layout.addLayout(config_btn_layout)

        config_group.setLayout(config_layout)
        layout.addWidget(config_group)

        system_group = QGroupBox("系统信息")
        system_layout = QVBoxLayout()

        sys_info = SystemUtils.get_system_info()
        for key, value in sys_info.items():
            info_label = QLabel(f"{key}: {value}")
            system_layout.addWidget(info_label)

        is_admin = SystemUtils.check_admin()
        admin_label = QLabel(f"管理员权限: {'是' if is_admin else '否'}")
        admin_label.setStyleSheet("color: green;" if is_admin else "color: red;")
        system_layout.addWidget(admin_label)

        system_group.setLayout(system_layout)
        layout.addWidget(system_group)

        layout.addStretch()

        apply_btn = QPushButton("应用设置")
        apply_btn.clicked.connect(self.apply_settings)
        apply_btn.setStyleSheet("""
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
        layout.addWidget(apply_btn)

        self.setLayout(layout)

    def load_settings(self):
        self.auto_save_check.setChecked(self.config_manager.get('auto_save', True))
        self.backup_check.setChecked(self.config_manager.get('backup_before_optimize', True))
        self.notifications_check.setChecked(self.config_manager.get('show_notifications', True))

        profile_map = {'quick': 0, 'balanced': 1, 'deep': 2}
        profile = self.config_manager.get('optimization_profile', 'balanced')
        self.profile_combo.setCurrentIndex(profile_map.get(profile, 1))

    def apply_settings(self):
        self.config_manager.set('auto_save', self.auto_save_check.isChecked())
        self.config_manager.set('backup_before_optimize', self.backup_check.isChecked())
        self.config_manager.set('show_notifications', self.notifications_check.isChecked())

        profile_map = {0: 'quick', 1: 'balanced', 2: 'deep'}
        self.config_manager.set('optimization_profile', profile_map.get(self.profile_combo.currentIndex(), 'balanced'))

        QMessageBox.information(self, "成功", "设置已保存")

    def export_config(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出配置", "winoptimizer_config.json", "JSON Files (*.json)"
        )
        if file_path:
            try:
                self.config_manager.export_config(file_path)
                QMessageBox.information(self, "成功", f"配置已导出到:\n{file_path}")
            except Exception as e:
                QMessageBox.warning(self, "失败", f"导出失败:\n{str(e)}")

    def import_config(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "导入配置", "", "JSON Files (*.json)"
        )
        if file_path:
            try:
                self.config_manager.import_config(file_path)
                self.load_settings()
                QMessageBox.information(self, "成功", "配置已导入")
            except Exception as e:
                QMessageBox.warning(self, "失败", f"导入失败:\n{str(e)}")

    def reset_config(self):
        reply = QMessageBox.question(
            self, "确认", "确定要恢复默认设置吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.config_manager.config = self.config_manager.get_default_config()
            self.config_manager.save_config()
            self.load_settings()
            QMessageBox.information(self, "成功", "已恢复默认设置")
