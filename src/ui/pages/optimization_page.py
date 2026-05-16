from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTreeWidget, QTreeWidgetItem, QLabel,
                             QProgressBar, QTextEdit, QListWidget, QListWidgetItem,
                             QSplitter, QFrame, QMessageBox)
from PySide6.QtCore import Qt, QThread, Signal
from ...i18n import tr
from ...core.optimizer import Optimizer


class OptimizationPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("ContentPage")
        self.optimizer = Optimizer()
        self._selected_ids = set()
        self._updating_list = False
        self._updating_tree = False
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)

        header = QLabel(tr("opt.header"))
        header.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 6px;")
        main_layout.addWidget(header)

        sub_header = QLabel(
            tr("opt.sub_header",
               count=len(self.optimizer._items),
               categories=len(self.optimizer._categories))
        )
        sub_header.setStyleSheet("color: #666; font-size: 13px; margin-bottom: 10px;")
        main_layout.addWidget(sub_header)

        preset_layout = QHBoxLayout()
        preset_layout.setSpacing(8)

        self.basic_preset_btn = QPushButton("🎯 " + tr("opt.basic_preset"))
        self.basic_preset_btn.setToolTip(tr("opt.basic_preset_tip"))
        self.basic_preset_btn.setMinimumHeight(36)
        self.basic_preset_btn.clicked.connect(self.apply_basic_preset)
        preset_layout.addWidget(self.basic_preset_btn)

        self.deep_preset_btn = QPushButton("⚡ " + tr("opt.deep_preset"))
        self.deep_preset_btn.setToolTip(tr("opt.deep_preset_tip"))
        self.deep_preset_btn.setMinimumHeight(36)
        self.deep_preset_btn.clicked.connect(self.apply_deep_preset)
        preset_layout.addWidget(self.deep_preset_btn)

        self.select_all_btn = QPushButton("☑ " + tr("opt.select_all"))
        self.select_all_btn.setMinimumHeight(36)
        self.select_all_btn.clicked.connect(self.select_all)
        preset_layout.addWidget(self.select_all_btn)

        self.deselect_all_btn = QPushButton("☐ " + tr("opt.deselect_all"))
        self.deselect_all_btn.setMinimumHeight(36)
        self.deselect_all_btn.clicked.connect(self.deselect_all)
        preset_layout.addWidget(self.deselect_all_btn)

        self.expand_all_btn = QPushButton("▼ " + tr("opt.expand_all"))
        self.expand_all_btn.setMinimumHeight(36)
        self.expand_all_btn.clicked.connect(self.expand_all)
        preset_layout.addWidget(self.expand_all_btn)

        self.collapse_all_btn = QPushButton("▶ " + tr("opt.collapse_all"))
        self.collapse_all_btn.setMinimumHeight(36)
        self.collapse_all_btn.clicked.connect(self.collapse_all)
        preset_layout.addWidget(self.collapse_all_btn)

        preset_layout.addStretch()
        main_layout.addLayout(preset_layout)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)

        left_panel = self._create_left_panel()
        splitter.addWidget(left_panel)

        right_panel = self._create_right_panel()
        splitter.addWidget(right_panel)

        splitter.setSizes([600, 350])
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)
        main_layout.addWidget(splitter, 1)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMinimumHeight(22)
        main_layout.addWidget(self.progress_bar)

        log_label = QLabel(tr("opt.log_label"))
        log_label.setStyleSheet("font-weight: bold; margin-top: 4px;")
        main_layout.addWidget(log_label)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(140)
        self.log_text.setPlaceholderText(tr("opt.log_placeholder"))
        main_layout.addWidget(self.log_text)

        action_layout = QHBoxLayout()

        self.backup_btn = QPushButton("💾 " + tr("opt.backup"))
        self.backup_btn.setMinimumHeight(40)
        self.backup_btn.setToolTip(tr("opt.backup_tip"))
        self.backup_btn.clicked.connect(self.backup_and_optimize)
        action_layout.addWidget(self.backup_btn)

        self.restore_btn = QPushButton("🔄 " + tr("opt.restore"))
        self.restore_btn.setMinimumHeight(40)
        self.restore_btn.setToolTip(tr("opt.restore_tip"))
        self.restore_btn.clicked.connect(self.restore_registry)
        action_layout.addWidget(self.restore_btn)

        action_layout.addStretch()

        self.optimize_btn = QPushButton("🚀 " + tr("opt.start"))
        self.optimize_btn.setMinimumHeight(44)
        self.optimize_btn.setMinimumWidth(180)
        self.optimize_btn.clicked.connect(self.start_optimization)
        self.optimize_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078D4;
                color: white;
                border: none;
                padding: 10px 28px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #106EBE;
            }
            QPushButton:disabled {
                background-color: #CCC;
                color: #888;
            }
        """)
        action_layout.addWidget(self.optimize_btn)

        main_layout.addLayout(action_layout)

    def _create_left_panel(self):
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(4, 4, 4, 4)

        label = QLabel(tr("opt.optimize_panel"))
        label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 4px;")
        layout.addWidget(label)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels([tr("opt.tree_name"), tr("opt.tree_desc")])
        self.tree_widget.setColumnWidth(0, 260)
        self.tree_widget.setColumnWidth(1, 280)
        self.tree_widget.setAlternatingRowColors(True)
        self.tree_widget.setRootIsDecorated(True)
        self.tree_widget.itemChanged.connect(self._on_tree_item_changed)
        layout.addWidget(self.tree_widget)

        self.populate_tree()
        return frame

    def _create_right_panel(self):
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(4, 4, 4, 4)

        sel_header = QHBoxLayout()
        label = QLabel(tr("opt.selected_items"))
        label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 4px;")
        sel_header.addWidget(label)
        sel_header.addStretch()

        self.selected_count_label = QLabel(tr("opt.items_count", count=0))
        self.selected_count_label.setStyleSheet("color: #0078D4; font-weight: bold;")
        sel_header.addWidget(self.selected_count_label)
        layout.addLayout(sel_header)

        self.selected_list = QListWidget()
        self.selected_list.setAlternatingRowColors(True)
        self.selected_list.setSelectionMode(QListWidget.NoSelection)
        self.selected_list.itemDoubleClicked.connect(self._on_list_item_double_clicked)
        layout.addWidget(self.selected_list)

        self.clear_selection_btn = QPushButton(tr("opt.clear_selection"))
        self.clear_selection_btn.setMinimumHeight(30)
        self.clear_selection_btn.clicked.connect(self.clear_selection)
        layout.addWidget(self.clear_selection_btn)

        return frame

    def populate_tree(self):
        self._updating_tree = True
        self.tree_widget.clear()
        items_data = self.optimizer.get_optimization_items()

        for category, items in items_data.items():
            category_item = QTreeWidgetItem(self.tree_widget)
            category_item.setText(0, category)
            category_item.setText(1, tr("opt.items_count", count=len(items)))
            category_item.setFlags(category_item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsAutoTristate)
            category_item.setCheckState(0, Qt.Unchecked)
            category_item.setData(0, Qt.UserRole, f"__category__{category}")
            category_item.setExpanded(True)

            category_font = category_item.font(0)
            category_font.setBold(True)
            category_item.setFont(0, category_font)

            for item in items:
                child_item = QTreeWidgetItem(category_item)
                child_item.setText(0, item["name"])
                child_item.setText(1, item["description"])
                child_item.setFlags(child_item.flags() | Qt.ItemIsUserCheckable)
                child_item.setCheckState(0, Qt.Unchecked)
                child_item.setData(0, Qt.UserRole, item["id"])

        self._updating_tree = False

    def _on_tree_item_changed(self, item, column):
        if self._updating_tree:
            return
        if self._updating_list:
            return

        item_id = item.data(0, Qt.UserRole)
        if not item_id:
            return

        if item_id.startswith("__category__"):
            self._update_category_children(item)
        else:
            checked = item.checkState(0) == Qt.Checked
            if checked:
                self._selected_ids.add(item_id)
            else:
                self._selected_ids.discard(item_id)

        self._refresh_selected_list()

    def _update_category_children(self, category_item):
        check_state = category_item.checkState(0)
        for i in range(category_item.childCount()):
            child = category_item.child(i)
            child.setCheckState(0, check_state)

    def _refresh_selected_list(self):
        self._updating_list = True
        self.selected_list.clear()

        for item_id in sorted(self._selected_ids):
            item = self.optimizer.get_item_by_id(item_id)
            if item:
                list_item = QListWidgetItem(f"{item.name}")
                list_item.setData(Qt.UserRole, item_id)
                list_item.setToolTip(item.description)
                self.selected_list.addItem(list_item)

        self.selected_count_label.setText(tr("opt.items_count", count=len(self._selected_ids)))
        self._updating_list = False

    def _on_list_item_double_clicked(self, list_item):
        item_id = list_item.data(Qt.UserRole)
        if item_id:
            self._selected_ids.discard(item_id)
            self._refresh_selected_list()
            self._uncheck_tree_item(item_id)

    def _uncheck_tree_item(self, item_id):
        self._updating_tree = True
        root = self.tree_widget.invisibleRootItem()
        for i in range(root.childCount()):
            cat_item = root.child(i)
            for j in range(cat_item.childCount()):
                child = cat_item.child(j)
                if child.data(0, Qt.UserRole) == item_id:
                    child.setCheckState(0, Qt.Unchecked)
                    break
        self._updating_tree = False

    def _collect_tree_checked(self):
        checked = set()
        root = self.tree_widget.invisibleRootItem()
        for i in range(root.childCount()):
            cat_item = root.child(i)
            for j in range(cat_item.childCount()):
                child = cat_item.child(j)
                if child.checkState(0) == Qt.Checked:
                    item_id = child.data(0, Qt.UserRole)
                    if item_id and not str(item_id).startswith("__category__"):
                        checked.add(item_id)
        return checked

    def select_all(self):
        self._updating_tree = True
        root = self.tree_widget.invisibleRootItem()
        for i in range(root.childCount()):
            cat_item = root.child(i)
            cat_item.setCheckState(0, Qt.Checked)
        self._updating_tree = False
        self._selected_ids = self._collect_tree_checked()
        self._refresh_selected_list()

    def deselect_all(self):
        self._updating_tree = True
        root = self.tree_widget.invisibleRootItem()
        for i in range(root.childCount()):
            cat_item = root.child(i)
            cat_item.setCheckState(0, Qt.Unchecked)
        self._updating_tree = False
        self._selected_ids.clear()
        self._refresh_selected_list()

    def expand_all(self):
        self.tree_widget.expandAll()

    def collapse_all(self):
        self.tree_widget.collapseAll()

    def clear_selection(self):
        self._selected_ids.clear()
        self._refresh_selected_list()
        self.deselect_all()

    def apply_basic_preset(self):
        preset_ids = set(self.optimizer.get_basic_preset())
        self._apply_preset(preset_ids, "基础优化预设")

    def apply_deep_preset(self):
        preset_ids = set(self.optimizer.get_deep_preset())
        self._apply_preset(preset_ids, "深度优化预设")

    def _apply_preset(self, preset_ids, preset_name):
        self._updating_tree = True
        root = self.tree_widget.invisibleRootItem()
        for i in range(root.childCount()):
            cat_item = root.child(i)
            all_children = []
            for j in range(cat_item.childCount()):
                child = cat_item.child(j)
                item_id = child.data(0, Qt.UserRole)
                if item_id and not str(item_id).startswith("__category__"):
                    all_children.append(child)
                    if item_id in preset_ids:
                        child.setCheckState(0, Qt.Checked)
                    else:
                        child.setCheckState(0, Qt.Unchecked)
            if all_children and all(c.checkState(0) == Qt.Checked for c in all_children):
                cat_item.setCheckState(0, Qt.Checked)
            elif all_children and all(c.checkState(0) == Qt.Unchecked for c in all_children):
                cat_item.setCheckState(0, Qt.Unchecked)
            else:
                cat_item.setCheckState(0, Qt.PartiallyChecked)
        self._updating_tree = False
        self._selected_ids = preset_ids.copy()
        self._refresh_selected_list()
        self.log_text.append("[预设] " + tr("opt.preset_loaded", name=preset_name, count=len(preset_ids)))

    def _get_effective_selected_ids(self):
        tree_checked = self._collect_tree_checked()
        return tree_checked if tree_checked else self._selected_ids

    def backup_and_optimize(self):
        selected = self._get_effective_selected_ids()
        if not selected:
            QMessageBox.information(self, tr("opt.prompt"), tr("opt.no_selection"))
            return

        reply = QMessageBox.question(
            self, tr("opt.confirm_backup_title"),
            tr("opt.confirm_backup", count=len(selected)),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
        )
        if reply != QMessageBox.Yes:
            return

        self.log_text.clear()
        self.log_text.append(tr("opt.backup_progress", count=len(selected)))
        success, info = self.optimizer.backup_registry(selected)
        if success:
            self.log_text.append("✓ " + tr("opt.backup_saved", path=info))
        else:
            self.log_text.append("✗ " + tr("opt.backup_failed", error=info))
            return

        self._do_optimization(selected)

    def start_optimization(self):
        selected = self._get_effective_selected_ids()
        if not selected:
            QMessageBox.information(self, tr("opt.prompt"), tr("opt.no_selection"))
            return

        reply = QMessageBox.warning(
            self, tr("opt.confirm_optimize_title"),
            tr("opt.confirm_optimize", count=len(selected)),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        self._do_optimization(selected)

    def _do_optimization(self, selected_ids):
        self.optimize_btn.setEnabled(False)
        self.backup_btn.setEnabled(False)
        self.restore_btn.setEnabled(False)
        self.basic_preset_btn.setEnabled(False)
        self.deep_preset_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.log_text.clear()
        self.log_text.append(tr("opt.optimize_start", count=len(selected_ids)) + "\n")

        self.optimize_thread = OptimizeThread(self.optimizer, list(selected_ids))
        self.optimize_thread.progress.connect(self._on_progress)
        self.optimize_thread.optimize_finished.connect(self._on_optimization_finished)
        self.optimize_thread.start()

    def _on_progress(self, current, total, message):
        if total > 0:
            self.progress_bar.setValue(int(current / total * 100))
        self.log_text.append(message)

    def _on_optimization_finished(self, results):
        self.progress_bar.setValue(100)
        self.optimize_btn.setEnabled(True)
        self.backup_btn.setEnabled(True)
        self.restore_btn.setEnabled(True)
        self.basic_preset_btn.setEnabled(True)
        self.deep_preset_btn.setEnabled(True)

        success_count = sum(1 for r in results if r["success"])
        fail_count = len(results) - success_count
        self.log_text.append(f"\n{'='*50}")
        self.log_text.append(tr("opt.optimize_complete", success=success_count, failed=fail_count, total=len(results)))

        if success_count == len(results):
            self.log_text.append("✓ " + tr("opt.optimize_full"))
        elif fail_count > 0:
            self.log_text.append("⚠ " + tr("opt.optimize_partial"))

    def restore_registry(self):
        reply = QMessageBox.warning(
            self, tr("opt.confirm_restore_title"),
            tr("opt.restore_confirm"),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        self.log_text.clear()
        self.log_text.append(tr("opt.restore_progress"))
        success, info = self.optimizer.restore_from_backup()
        if success:
            self.log_text.append(f"✓ {info}")
        else:
            self.log_text.append(f"✗ {info}")


class OptimizeThread(QThread):
    progress = Signal(int, int, str)
    optimize_finished = Signal(list)

    def __init__(self, optimizer, items):
        super().__init__()
        self.optimizer = optimizer
        self.items = items

    def run(self):
        def progress_cb(current, total, message):
            self.progress.emit(current, total, message)

        results = self.optimizer.apply_batch(self.items, progress_callback=progress_cb)
        self.optimize_finished.emit(results)