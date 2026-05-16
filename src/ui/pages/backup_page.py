from ...i18n import tr
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel,
                             QTreeWidget, QTreeWidgetItem, QFrame, QMessageBox)
from PySide6.QtCore import Qt
import os
from pathlib import Path


class BackupPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("ContentPage")
        self._init_ui()
        self._load_backups()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)

        header = QLabel(tr("backup.header"))
        header.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 6px;")
        layout.addWidget(header)

        sub_header = QLabel(tr("backup.sub_header"))
        sub_header.setStyleSheet("color: #666; font-size: 13px; margin-bottom: 10px;")
        layout.addWidget(sub_header)

        tree_frame = QFrame()
        tree_frame.setFrameStyle(QFrame.StyledPanel)
        tree_layout = QVBoxLayout(tree_frame)
        tree_layout.setContentsMargins(4, 4, 4, 4)

        tl = QLabel(tr("backup.tree_name"))
        tl.setStyleSheet("font-weight: bold; font-size: 14px; padding: 4px;")
        tree_layout.addWidget(tl)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels([tr("backup.tree_filename"), tr("backup.tree_time"), tr("backup.tree_size")])
        self.tree_widget.setAlternatingRowColors(True)
        self.tree_widget.setRootIsDecorated(True)
        tree_layout.addWidget(self.tree_widget)

        layout.addWidget(tree_frame, 1)

        tip = QLabel(tr("backup.tip"))
        tip.setStyleSheet("font-size: 12px; color: #999; margin-top: 6px;")
        layout.addWidget(tip)

    def _load_backups(self):
        self.tree_widget.clear()

        backup_dir = Path(os.environ.get("APPDATA", ".")) / "WinOptimizer" / "backups"
        root_item = QTreeWidgetItem(self.tree_widget)
        root_item.setText(0, tr("backup.root_name"))
        root_item.setExpanded(True)

        root_font = root_item.font(0)
        root_font.setBold(True)
        root_item.setFont(0, root_font)

        if not backup_dir.exists():
            empty_item = QTreeWidgetItem(root_item)
            empty_item.setText(0, tr("backup.empty"))
            return

        backup_files = sorted(backup_dir.glob("reg_backup_*.json"), reverse=True)
        if not backup_files:
            empty_item = QTreeWidgetItem(root_item)
            empty_item.setText(0, tr("backup.empty"))
            return

        for bf in backup_files:
            file_item = QTreeWidgetItem(root_item)
            file_item.setText(0, bf.name)
            mtime = bf.stat().st_mtime
            from datetime import datetime
            dt = datetime.fromtimestamp(mtime)
            file_item.setText(1, dt.strftime("%Y-%m-%d %H:%M:%S"))
            size = bf.stat().st_size
            file_item.setText(2, self._format_size(size))
            file_item.setData(0, Qt.UserRole, str(bf))

    def _format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"