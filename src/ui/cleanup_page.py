from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QCheckBox, QLabel, QProgressBar, QTextEdit,
                             QGroupBox, QTableWidget, QTableWidgetItem)
from PySide6.QtCore import Qt, QThread, Signal
from ..core.cleaner import Cleaner

class CleanupPage(QWidget):
    def __init__(self):
        super().__init__()
        self.cleaner = Cleaner()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        header = QLabel("垃圾清理")
        header.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        layout.addWidget(header)

        options_group = QGroupBox("清理选项")
        options_layout = QVBoxLayout()

        self.temp_check = QCheckBox("临时文件")
        self.temp_check.setChecked(True)
        options_layout.addWidget(self.temp_check)

        self.prefetch_check = QCheckBox("预读取文件")
        self.prefetch_check.setChecked(True)
        options_layout.addWidget(self.prefetch_check)

        self.recent_check = QCheckBox("最近使用记录")
        self.recent_check.setChecked(False)
        options_layout.addWidget(self.recent_check)

        self.logs_check = QCheckBox("日志文件")
        self.logs_check.setChecked(True)
        options_layout.addWidget(self.logs_check)

        self.thumbnails_check = QCheckBox("缩略图缓存")
        self.thumbnails_check.setChecked(True)
        options_layout.addWidget(self.thumbnails_check)

        options_group.setLayout(options_layout)
        layout.addWidget(options_group)

        button_layout = QHBoxLayout()
        self.scan_btn = QPushButton("扫描垃圾")
        self.scan_btn.clicked.connect(self.scan_garbage)
        button_layout.addWidget(self.scan_btn)

        self.clean_btn = QPushButton("开始清理")
        self.clean_btn.clicked.connect(self.start_cleanup)
        self.clean_btn.setEnabled(False)
        self.clean_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        button_layout.addWidget(self.clean_btn)

        layout.addLayout(button_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.result_table = QTableWidget()
        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(['类别', '文件数', '大小'])
        layout.addWidget(self.result_table)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(120)
        layout.addWidget(QLabel("清理日志:"))
        layout.addWidget(self.log_text)

        self.setLayout(layout)

    def get_scan_options(self):
        return {
            'temp': self.temp_check.isChecked(),
            'prefetch': self.prefetch_check.isChecked(),
            'recent': self.recent_check.isChecked(),
            'logs': self.logs_check.isChecked(),
            'thumbnails': self.thumbnails_check.isChecked()
        }

    def scan_garbage(self):
        self.scan_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.log_text.clear()
        self.log_text.append("正在扫描...")

        self.scan_thread = ScanThread(self.cleaner, self.get_scan_options())
        self.scan_thread.progress.connect(self.update_progress)
        self.scan_thread.scan_finished.connect(self.scan_finished)
        self.scan_thread.start()

    def update_progress(self, value, message):
        self.progress_bar.setValue(value)
        self.log_text.append(message)

    def scan_finished(self, results):
        self.progress_bar.setValue(100)
        self.scan_btn.setEnabled(True)
        self.scan_results = results

        self.result_table.setRowCount(0)
        for category, data in results['details'].items():
            row = self.result_table.rowCount()
            self.result_table.insertRow(row)
            self.result_table.setItem(row, 0, QTableWidgetItem(self.get_category_name(category)))
            self.result_table.setItem(row, 1, QTableWidgetItem(str(data['files'])))
            self.result_table.setItem(row, 2, QTableWidgetItem(self.cleaner.format_size(data['size'])))

        total_row = self.result_table.rowCount()
        self.result_table.insertRow(total_row)
        self.result_table.setItem(total_row, 0, QTableWidgetItem("总计"))
        self.result_table.setItem(total_row, 1, QTableWidgetItem(str(results['total_files'])))
        self.result_table.setItem(total_row, 2, QTableWidgetItem(self.cleaner.format_size(results['total_size'])))

        self.log_text.append(f"\n扫描完成！发现 {results['total_files']} 个文件，共 {self.cleaner.format_size(results['total_size'])}")
        self.clean_btn.setEnabled(True)

    def get_category_name(self, category):
        names = {
            'temp': '临时文件',
            'prefetch': '预读取',
            'recent': '最近记录',
            'logs': '日志文件',
            'thumbnails': '缩略图'
        }
        return names.get(category, category)

    def start_cleanup(self):
        if not hasattr(self, 'scan_results'):
            return

        self.clean_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.log_text.clear()

        self.clean_thread = CleanThread(self.cleaner, self.get_scan_options())
        self.clean_thread.progress.connect(self.update_progress)
        self.clean_thread.clean_finished.connect(self.cleanup_finished)
        self.clean_thread.start()

    def cleanup_finished(self, results):
        self.progress_bar.setValue(100)
        self.clean_btn.setEnabled(True)
        self.scan_results = None

        self.log_text.append(f"\n清理完成！")
        self.log_text.append(f"删除文件: {results['deleted_files']} 个")
        self.log_text.append(f"释放空间: {self.cleaner.format_size(results['deleted_size'])}")
        if results['errors']:
            self.log_text.append(f"\n部分文件清理失败 (权限问题)")
        self.result_table.setRowCount(0)

class ScanThread(QThread):
    progress = Signal(int, str)
    scan_finished = Signal(dict)

    def __init__(self, cleaner, options):
        super().__init__()
        self.cleaner = cleaner
        self.options = options

    def run(self):
        self.progress.emit(50, "正在扫描...")
        results = self.cleaner.scan(self.options)
        self.progress.emit(100, "扫描完成")
        self.scan_finished.emit(results)

class CleanThread(QThread):
    progress = Signal(int, str)
    clean_finished = Signal(dict)

    def __init__(self, cleaner, options):
        super().__init__()
        self.cleaner = cleaner
        self.options = options

    def run(self):
        results = self.cleaner.clean(self.options, lambda p, m: self.progress.emit(p, m))
        self.clean_finished.emit(results)
