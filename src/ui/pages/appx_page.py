from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QListWidget, QListWidgetItem,
                             QProgressBar, QMessageBox, QFrame)
from PySide6.QtCore import Qt, QThread, Signal

from ...i18n import tr


class AppxPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("ContentPage")
        self._init_ui()
        self._load_apps()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)

        header = QLabel("📲 " + tr("appx.header"))
        header.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 6px;")
        layout.addWidget(header)

        sub_header = QLabel(tr("appx.sub_header"))
        sub_header.setStyleSheet("color: #666; font-size: 13px; margin-bottom: 10px;")
        layout.addWidget(sub_header)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)

        self.select_all_btn = QPushButton("☑ " + tr("appx.select_all"))
        self.select_all_btn.setMinimumHeight(32)
        self.select_all_btn.clicked.connect(self._select_all)
        toolbar.addWidget(self.select_all_btn)

        self.deselect_all_btn = QPushButton("☐ " + tr("appx.deselect_all"))
        self.deselect_all_btn.setMinimumHeight(32)
        self.deselect_all_btn.clicked.connect(self._deselect_all)
        toolbar.addWidget(self.deselect_all_btn)

        self.refresh_btn = QPushButton("🔄 " + tr("appx.refresh"))
        self.refresh_btn.setMinimumHeight(32)
        self.refresh_btn.clicked.connect(self._load_apps)
        toolbar.addWidget(self.refresh_btn)

        toolbar.addStretch()
        layout.addLayout(toolbar)

        list_frame = QFrame()
        list_frame.setFrameStyle(QFrame.StyledPanel)
        list_layout = QVBoxLayout(list_frame)
        list_layout.setContentsMargins(4, 4, 4, 4)

        self.app_list = QListWidget()
        self.app_list.setAlternatingRowColors(True)
        self.app_list.setSelectionMode(QListWidget.NoSelection)
        list_layout.addWidget(self.app_list)

        layout.addWidget(list_frame, 1)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMinimumHeight(22)
        layout.addWidget(self.progress_bar)

        action_layout = QHBoxLayout()
        action_layout.addStretch()

        self.uninstall_btn = QPushButton("🗑 " + tr("appx.uninstall_btn"))
        self.uninstall_btn.setMinimumHeight(44)
        self.uninstall_btn.setMinimumWidth(180)
        self.uninstall_btn.clicked.connect(self._start_uninstall)
        self.uninstall_btn.setStyleSheet("""
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
        action_layout.addWidget(self.uninstall_btn)

        layout.addLayout(action_layout)

    def _load_apps(self):
        self.app_list.clear()
        item = QListWidgetItem(tr("appx.loading"))
        item.setFlags(Qt.NoItemFlags)
        self.app_list.addItem(item)

        self.load_thread = LoadAppsThread()
        self.load_thread.apps_loaded.connect(self._on_apps_loaded)
        self.load_thread.start()

    def _on_apps_loaded(self, packages):
        self.app_list.clear()
        if not packages:
            self.app_list.addItem(tr("appx.no_apps"))
            return

        if isinstance(packages, list) and len(packages) > 0 and packages[0].startswith(tr("appx.load_fail")):
            self.app_list.addItems(packages)
            return

        for pkg in packages:
            item = QListWidgetItem(pkg)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            item.setData(Qt.UserRole, pkg)
            self.app_list.addItem(item)

    def _select_all(self):
        for i in range(self.app_list.count()):
            item = self.app_list.item(i)
            if item.flags() & Qt.ItemIsUserCheckable:
                item.setCheckState(Qt.Checked)

    def _deselect_all(self):
        for i in range(self.app_list.count()):
            item = self.app_list.item(i)
            if item.flags() & Qt.ItemIsUserCheckable:
                item.setCheckState(Qt.Unchecked)

    def _get_selected(self):
        selected = []
        for i in range(self.app_list.count()):
            item = self.app_list.item(i)
            if item.flags() & Qt.ItemIsUserCheckable and item.checkState() == Qt.Checked:
                pkg = item.data(Qt.UserRole)
                if pkg:
                    selected.append(pkg)
        return selected

    def _start_uninstall(self):
        selected = self._get_selected()
        if not selected:
            QMessageBox.information(self, tr("common.info"), tr("appx.no_selection"))
            return

        msg = tr("appx.confirm_title") + "\n\n"
        msg += "\n".join(selected[:10])
        if len(selected) > 10:
            msg += "\n\n" + tr("appx.confirm_more", count=len(selected) - 10)
        msg += "\n\n" + tr("appx.confirm_question")

        reply = QMessageBox.warning(
            self, tr("common.confirm"), msg,
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        self._set_controls_enabled(False)
        self.uninstall_btn.setText(tr("appx.uninstalling"))
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(selected))
        self.progress_bar.setValue(0)

        self.uninstall_thread = UninstallAppsThread(selected)
        self.uninstall_thread.progress.connect(lambda v: self.progress_bar.setValue(v))
        self.uninstall_thread.uninstall_finished.connect(self._on_uninstall_finished)
        self.uninstall_thread.start()

    def _on_uninstall_finished(self, success_count, failed_count, failed_list):
        self._set_controls_enabled(True)
        self.uninstall_btn.setText("🗑 " + tr("appx.uninstall_btn"))
        self.progress_bar.setValue(0)
        self._load_apps()

        total = success_count + failed_count
        msg = tr("appx.complete_success", success=success_count) + "\n" + tr("appx.complete_failed", failed=failed_count)

        if failed_count > 0 and failed_list:
            msg += "\n\n" + tr("appx.complete_failed_list")
            msg += "\n" + "\n".join(failed_list[:3])
            if len(failed_list) > 3:
                msg += "\n" + tr("appx.complete_more_failed", count=len(failed_list) - 3)
            msg += "\n\n" + tr("appx.complete_note")

        QMessageBox.information(self, tr("common.confirm"), msg)

    def _set_controls_enabled(self, enabled):
        self.select_all_btn.setEnabled(enabled)
        self.deselect_all_btn.setEnabled(enabled)
        self.refresh_btn.setEnabled(enabled)
        self.uninstall_btn.setEnabled(enabled)
        self.app_list.setEnabled(enabled)


class LoadAppsThread(QThread):
    apps_loaded = Signal(list)

    def run(self):
        try:
            import subprocess
            from ...i18n import tr as _tr

            ps_script = "Get-AppxPackage | Where-Object { !$_.IsFramework -and !$_.NonRemovable } | ForEach-Object { $_.PackageFullName }"

            r = subprocess.run(
                f'powershell -Command "{ps_script}"',
                capture_output=True, text=True,
                encoding='gbk', errors='ignore',
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=30
            )

            if r.returncode == 0 and r.stdout.strip():
                packages = [
                    line.strip()
                    for line in r.stdout.splitlines()
                    if line.strip()
                ]
                self.apps_loaded.emit(packages)
            else:
                self.apps_loaded.emit([f"{_tr('appx.load_fail')}: {r.stderr}" if r.stderr else _tr("appx.no_apps")])
        except Exception as e:
            self.apps_loaded.emit([f"{_tr('appx.load_fail')}: {str(e)}"])


class UninstallAppsThread(QThread):
    progress = Signal(int)
    uninstall_finished = Signal(int, int, list)

    def __init__(self, packages):
        super().__init__()
        self.packages = packages

    def run(self):
        import subprocess
        success = 0
        failed = 0
        failed_list = []

        for i, pkg in enumerate(self.packages):
            self.progress.emit(i + 1)
            try:
                r = subprocess.run(
                    f'powershell -Command "Remove-AppxPackage -Package \'{pkg}\'"',
                    capture_output=True, text=True,
                    encoding='gbk', errors='ignore',
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    timeout=60
                )
                if r.returncode == 0:
                    success += 1
                else:
                    failed += 1
                    failed_list.append(pkg)
            except Exception:
                failed += 1
                failed_list.append(pkg)

        self.uninstall_finished.emit(success, failed, failed_list)