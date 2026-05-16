from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QComboBox, QLabel, QMessageBox)
from PySide6.QtCore import Qt
from ..core.services_manager import ServicesManager

class ServicesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.services_manager = ServicesManager()
        self.init_ui()
        self.load_services()

    def init_ui(self):
        layout = QVBoxLayout()

        header = QLabel("服务管理")
        header.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        layout.addWidget(header)

        self.services_table = QTableWidget()
        self.services_table.setColumnCount(5)
        self.services_table.setHorizontalHeaderLabels(['服务名称', '显示名称', '状态', '启动类型', '推荐'])
        self.services_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.services_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.services_table)

        button_layout = QHBoxLayout()

        self.refresh_btn = QPushButton("刷新")
        self.refresh_btn.clicked.connect(self.load_services)
        button_layout.addWidget(self.refresh_btn)

        self.apply_btn = QPushButton("应用更改")
        self.apply_btn.clicked.connect(self.apply_changes)
        self.apply_btn.setStyleSheet("""
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
        button_layout.addWidget(self.apply_btn)

        button_layout.addStretch()

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_services(self):
        services = self.services_manager.get_services()
        self.services_table.setRowCount(0)

        for service in services:
            row = self.services_table.rowCount()
            self.services_table.insertRow(row)

            self.services_table.setItem(row, 0, QTableWidgetItem(service['name']))
            self.services_table.setItem(row, 1, QTableWidgetItem(service['display_name']))
            self.services_table.setItem(row, 2, QTableWidgetItem(service['status']))

            start_type_combo = QComboBox()
            start_type_combo.addItems(['Auto', 'Manual', 'Disabled'])
            current_index = start_type_combo.findText(service['start_type'])
            if current_index >= 0:
                start_type_combo.setCurrentIndex(current_index)
            self.services_table.setCellWidget(row, 3, start_type_combo)

            recommended_item = QTableWidgetItem(service['recommended'])
            recommended_item.setForeground(Qt.blue)
            self.services_table.setItem(row, 4, recommended_item)

    def apply_changes(self):
        changes_made = 0
        for row in range(self.services_table.rowCount()):
            service_name = self.services_table.item(row, 0).text()
            start_type_combo = self.services_table.cellWidget(row, 3)
            new_start_type = start_type_combo.currentText()

            current_status = self.services_table.item(row, 2).text()
            status_changed = False

            if new_start_type == 'Disabled' and current_status == 'Running':
                if self.services_manager.stop_service(service_name):
                    status_changed = True

            if self.services_manager.set_service_start_type(service_name, new_start_type):
                changes_made += 1

        QMessageBox.information(self, "完成", f"已应用 {changes_made} 项更改\n部分服务需要重启才能生效")
        self.load_services()
