from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTreeWidget, QTreeWidgetItem, QLabel,
                             QProgressBar, QTextEdit, QFrame, QMessageBox)
from PySide6.QtCore import Qt, QThread, Signal
from ...core.cleaner import Cleaner
from ...i18n import tr

CATEGORY_KEY_MAP = {
    "缓存文件": "clean.category_cache",
    "系统文件": "clean.category_system",
    "临时文件": "clean.category_temp",
}

ITEM_KEY_MAP = {
    "Terminal Server Client缓存": "clean.item_tscache",
    "Windows更新缓存": "clean.item_wu_cache",
    "网页缓存": "clean.item_web_cache",
    "Cookies": "clean.item_cookies",
    "缩略图缓存": "clean.item_thumb",
    "D3D着色器缓存": "clean.item_d3d_cache",
    ".NET程序集缓存": "clean.item_dotnet_cache",
    "传递优化缓存": "clean.item_do_cache",
    "过时的WinSxS文件": "clean.item_winsxs",
    "错误应用包": "clean.item_error_appx",
    "Windows日志": "clean.item_windows_logs",
    "Windows错误报告": "clean.item_wer",
    "诊断数据": "clean.item_diag",
    "崩溃dmp文件": "clean.item_dmp",
    "Windows Defender扫描": "clean.item_defender_scan",
    "WinSxS临时文件": "clean.item_winsxs_temp",
    "系统临时文件": "clean.item_sys_temp",
    "系统dmp文件": "clean.item_drive_dmp",
    "回收站": "clean.item_recycle",
    "所有临时文件": "clean.item_all_temp",
    "预读取文件": "clean.item_prefetch",
}


def _translate_item_name(name):
    key = ITEM_KEY_MAP.get(name)
    if key:
        return tr(key)
    return name


class CleanupPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("ContentPage")
        self.cleaner = Cleaner()
        self._updating_tree = False
        self._cancel_requested = False
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)

        header = QLabel(tr("clean.header"))
        header.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 6px;")
        layout.addWidget(header)

        sub_header = QLabel(tr("clean.sub_header"))
        sub_header.setStyleSheet("color: #666; font-size: 13px; margin-bottom: 10px;")
        layout.addWidget(sub_header)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)

        self.select_all_btn = QPushButton("☑ " + tr("clean.select_all"))
        self.select_all_btn.setMinimumHeight(32)
        self.select_all_btn.clicked.connect(self._select_all)
        toolbar.addWidget(self.select_all_btn)

        self.deselect_all_btn = QPushButton("☐ " + tr("clean.deselect_all"))
        self.deselect_all_btn.setMinimumHeight(32)
        self.deselect_all_btn.clicked.connect(self._deselect_all)
        toolbar.addWidget(self.deselect_all_btn)

        self.expand_all_btn = QPushButton("▼ " + tr("clean.expand_all"))
        self.expand_all_btn.setMinimumHeight(32)
        self.expand_all_btn.clicked.connect(lambda: self.tree_widget.expandAll())
        toolbar.addWidget(self.expand_all_btn)

        self.collapse_all_btn = QPushButton("▶ " + tr("clean.collapse_all"))
        self.collapse_all_btn.setMinimumHeight(32)
        self.collapse_all_btn.clicked.connect(lambda: self.tree_widget.collapseAll())
        toolbar.addWidget(self.collapse_all_btn)

        toolbar.addStretch()
        layout.addLayout(toolbar)

        tree_frame = QFrame()
        tree_frame.setFrameStyle(QFrame.StyledPanel)
        tree_layout = QVBoxLayout(tree_frame)
        tree_layout.setContentsMargins(4, 4, 4, 4)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels([tr("clean.tree_name")])
        self.tree_widget.setAlternatingRowColors(True)
        self.tree_widget.setRootIsDecorated(True)
        self.tree_widget.itemChanged.connect(self._on_item_changed)
        tree_layout.addWidget(self.tree_widget)

        self._populate_tree()
        layout.addWidget(tree_frame, 1)

        progress_layout = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMinimumHeight(22)
        progress_layout.addWidget(self.progress_bar, 1)

        self.cancel_btn = QPushButton(tr("clean.cancel"))
        self.cancel_btn.setMinimumHeight(32)
        self.cancel_btn.setVisible(False)
        self.cancel_btn.clicked.connect(self._cancel)
        progress_layout.addWidget(self.cancel_btn)
        layout.addLayout(progress_layout)

        log_label = QLabel(tr("clean.log_label"))
        log_label.setStyleSheet("font-weight: bold; margin-top: 4px;")
        layout.addWidget(log_label)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(120)
        self.log_text.setPlaceholderText(tr("clean.log_placeholder"))
        layout.addWidget(self.log_text)

        action_layout = QHBoxLayout()
        action_layout.addStretch()

        self.clean_btn = QPushButton("🧹 " + tr("clean.start"))
        self.clean_btn.setMinimumHeight(44)
        self.clean_btn.setMinimumWidth(180)
        self.clean_btn.clicked.connect(self._start_clean)
        self.clean_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4d4f;
                color: white;
                border: none;
                padding: 10px 28px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover { background-color: #ff7875; }
            QPushButton:disabled { background-color: #CCC; color: #888; }
        """)
        action_layout.addWidget(self.clean_btn)

        layout.addLayout(action_layout)

    def _populate_tree(self):
        self._updating_tree = True
        self.tree_widget.clear()

        for category in self.cleaner.get_categories():
            items = self.cleaner.get_items(category)
            cat_key = CATEGORY_KEY_MAP.get(category, category)
            cat_item = QTreeWidgetItem(self.tree_widget)
            cat_item.setText(0, f"{tr(cat_key)} ({len(items)} 项)")
            cat_item.setFlags(cat_item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsAutoTristate)
            cat_item.setCheckState(0, Qt.Checked)
            cat_item.setData(0, Qt.UserRole, f"__cat__{category}")
            cat_item.setExpanded(True)

            cat_font = cat_item.font(0)
            cat_font.setBold(True)
            cat_item.setFont(0, cat_font)

            for item in items:
                child = QTreeWidgetItem(cat_item)
                child.setText(0, _translate_item_name(item.name))
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setCheckState(0, Qt.Checked)
                child.setData(0, Qt.UserRole, item.name)

        self._updating_tree = False

    def _on_item_changed(self, item, column):
        if self._updating_tree:
            return

        item_id = item.data(0, Qt.UserRole)
        if not item_id:
            return

        if item_id.startswith("__cat__"):
            check_state = item.checkState(0)
            for i in range(item.childCount()):
                item.child(i).setCheckState(0, check_state)

    def _get_selected_items(self):
        selected = []
        root = self.tree_widget.invisibleRootItem()
        for i in range(root.childCount()):
            cat_item = root.child(i)
            for j in range(cat_item.childCount()):
                child = cat_item.child(j)
                if child.checkState(0) == Qt.Checked:
                    name = child.data(0, Qt.UserRole)
                    if name and not str(name).startswith("__cat__"):
                        selected.append(name)
        return selected

    def _select_all(self):
        self._updating_tree = True
        root = self.tree_widget.invisibleRootItem()
        for i in range(root.childCount()):
            root.child(i).setCheckState(0, Qt.Checked)
        self._updating_tree = False

    def _deselect_all(self):
        self._updating_tree = True
        root = self.tree_widget.invisibleRootItem()
        for i in range(root.childCount()):
            root.child(i).setCheckState(0, Qt.Unchecked)
        self._updating_tree = False

    def _start_clean(self):
        selected = self._get_selected_items()
        if not selected:
            QMessageBox.information(self, tr("common.info"), tr("clean.no_selection"))
            return

        msg = tr("clean.confirm_text", count=len(selected)) + "\n\n"
        for item in selected[:8]:
            msg += f"  · {_translate_item_name(item)}\n"
        if len(selected) > 8:
            msg += f"  {tr('clean.confirm_more', count=len(selected) - 8)}\n"
        msg += "\n" + tr("clean.confirm_question")

        reply = QMessageBox.question(
            self, tr("common.confirm"), msg,
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
        )
        if reply != QMessageBox.Yes:
            return

        self._do_clean(selected)

    def _do_clean(self, items):
        self._cancel_requested = False
        self.clean_btn.setEnabled(False)
        self.tree_widget.setEnabled(False)
        self.select_all_btn.setEnabled(False)
        self.deselect_all_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.cancel_btn.setVisible(True)
        self.log_text.clear()
        self.log_text.append(tr("clean.cleaning_start", count=len(items)) + "\n")

        self.clean_thread = CleanThread(self.cleaner, items)
        self.clean_thread.progress.connect(self._on_clean_progress)
        self.clean_thread.clean_finished.connect(self._on_clean_finished)
        self.clean_thread.start()

    def _cancel(self):
        self._cancel_requested = True
        if hasattr(self, 'clean_thread') and self.clean_thread.isRunning():
            self.clean_thread.terminate()
            self.clean_thread.wait()
        self._restore_ui()

    def _on_clean_progress(self, current, total, item_name, success, message):
        if total > 0:
            self.progress_bar.setValue(int(current / total * 100))
        icon = "✓" if success else "✗"
        display_name = _translate_item_name(item_name)
        self.log_text.append(f"  [{current}/{total}] {icon} {display_name} - {message}")

    def _on_clean_finished(self, total, success_count):
        self._restore_ui()
        self.progress_bar.setValue(100)
        self.log_text.append(f"\n{'='*40}")
        self.log_text.append(tr("clean.cleaning_complete", success=success_count, failed=total - success_count, total=total))

        if self._cancel_requested:
            self.log_text.append(tr("clean.cleaning_cancelled"))
        elif success_count == total:
            self.log_text.append("✓ " + tr("clean.cleaning_success"))
        else:
            self.log_text.append("⚠ " + tr("clean.cleaning_partial"))

        QMessageBox.information(
            self, tr("common.info"),
            tr("clean.complete_msg", total=total) if not self._cancel_requested
            else tr("clean.cancelled_msg", count=success_count)
        )

    def _restore_ui(self):
        self.clean_btn.setEnabled(True)
        self.tree_widget.setEnabled(True)
        self.select_all_btn.setEnabled(True)
        self.deselect_all_btn.setEnabled(True)
        self.cancel_btn.setVisible(False)


class CleanThread(QThread):
    progress = Signal(int, int, str, bool, str)
    clean_finished = Signal(int, int)

    def __init__(self, cleaner, items):
        super().__init__()
        self.cleaner = cleaner
        self.items = items

    def run(self):
        total = len(self.items)
        success_count = 0

        for i, item_name in enumerate(self.items, 1):
            if self.isInterruptionRequested():
                break
            success, message = self.cleaner.execute_clean(item_name)
            if success:
                success_count += 1
            self.progress.emit(i, total, item_name, success, message)

        self.clean_finished.emit(total, success_count)