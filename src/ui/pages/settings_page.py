from ...i18n import tr, get_config, save_config, set_language
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QCheckBox, QGroupBox, QComboBox,
                             QScrollArea, QMessageBox, QHBoxLayout)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class SettingsPage(QWidget):
    languageChanged = Signal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("ContentPage")
        self._built = False
        self._init_ui()
        self._load_settings()
        self._built = True

    def _init_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")

        content = QWidget()
        content.setObjectName("SettingsContent")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        header = QLabel("\u2699  " + tr("settings.header"))
        header_font = QFont()
        header_font.setPointSize(24)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setStyleSheet("color: #333; padding-bottom: 8px;")
        layout.addWidget(header)

        general_group = QGroupBox(tr("settings.general"))
        general_group.setObjectName("SettingsGroupBox")
        general_group.setStyleSheet("""
            #SettingsGroupBox {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 16px;
                padding-top: 20px;
                background-color: #ffffff;
            }
            #SettingsGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px;
                color: #333;
                font-weight: bold;
                font-size: 15px;
            }
        """)
        general_layout = QVBoxLayout(general_group)
        general_layout.setContentsMargins(20, 28, 20, 20)
        general_layout.setSpacing(16)

        lang_layout = QHBoxLayout()
        lang_layout.setSpacing(12)

        lang_label = QLabel(tr("settings.language_label"))
        lang_label.setStyleSheet("font-size: 14px; color: #333;")
        lang_label.setFixedWidth(140)
        lang_layout.addWidget(lang_label)

        self.lang_combo = QComboBox()
        self.lang_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #d9d9d9;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 14px;
                min-width: 160px;
                background-color: #ffffff;
            }
            QComboBox:hover { border-color: #40a9ff; }
            QComboBox:focus { border-color: #1890ff; }
        """)
        self.lang_combo.addItems([
            tr("settings.language_zh"),
            tr("settings.language_en"),
            tr("settings.language_es"),
        ])
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()

        general_layout.addLayout(lang_layout)

        lang_note = QLabel(tr("settings.language_restart"))
        lang_note.setStyleSheet("color: #999; font-size: 12px; padding-left: 152px;")
        general_layout.addWidget(lang_note)

        self.admin_check = QCheckBox(tr("settings.admin_mode"))
        self.admin_check.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #333;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)
        general_layout.addWidget(self.admin_check)

        admin_desc = QLabel(tr("settings.admin_mode_desc"))
        admin_desc.setStyleSheet("color: #999; font-size: 12px; padding-left: 26px;")
        admin_desc.setWordWrap(True)
        general_layout.addWidget(admin_desc)

        self.backup_check = QCheckBox(tr("settings.auto_backup"))
        self.backup_check.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #333;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)
        general_layout.addWidget(self.backup_check)

        backup_desc = QLabel(tr("settings.auto_backup_desc"))
        backup_desc.setStyleSheet("color: #999; font-size: 12px; padding-left: 26px;")
        backup_desc.setWordWrap(True)
        general_layout.addWidget(backup_desc)

        general_group.setLayout(general_layout)
        layout.addWidget(general_group)

        layout.addSpacing(8)

        self.save_btn = QLabel("\U0001F4BE  " + tr("common.ok"))
        self.save_btn.setAlignment(Qt.AlignCenter)
        self.save_btn.setObjectName("SettingsSaveButton")
        self.save_btn.setStyleSheet("""
            #SettingsSaveButton {
                background-color: #1890ff;
                color: white;
                border-radius: 6px;
                padding: 10px 32px;
                font-size: 14px;
                font-weight: bold;
                cursor: pointer;
            }
            #SettingsSaveButton:hover {
                background-color: #40a9ff;
            }
        """)
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.mousePressEvent = lambda e: self._save_settings()
        self.save_btn.setFixedWidth(200)
        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(self.save_btn)
        btn_container.addStretch()
        layout.addLayout(btn_container)

        layout.addSpacing(16)

        restart_note = QLabel(tr("settings.restart_required"))
        restart_note.setAlignment(Qt.AlignCenter)
        restart_note.setStyleSheet("color: #aaa; font-size: 13px; font-style: italic;")
        restart_note.setWordWrap(True)
        layout.addWidget(restart_note)

        layout.addStretch()

        scroll.setWidget(content)
        outer_layout.addWidget(scroll)

    def _load_settings(self):
        config = get_config()

        lang = config.get("language", "zh")
        lang_index_map = {"zh": 0, "en": 1, "es": 2}
        self.lang_combo.setCurrentIndex(lang_index_map.get(lang, 0))

        settings = config.get("settings", {})
        self.admin_check.setChecked(settings.get("require_admin", True))
        self.backup_check.setChecked(settings.get("auto_backup_before_optimize", True))

    def _save_settings(self):
        config = get_config()

        lang_index_map = {0: "zh", 1: "en", 2: "es"}
        old_lang = config.get("language", "en")
        new_lang = lang_index_map.get(self.lang_combo.currentIndex(), "en")
        config["language"] = new_lang

        if "settings" not in config:
            config["settings"] = {}
        config["settings"]["require_admin"] = self.admin_check.isChecked()
        config["settings"]["auto_backup_before_optimize"] = self.backup_check.isChecked()

        save_config(config)

        if new_lang != old_lang:
            set_language(new_lang)
            self.languageChanged.emit(new_lang)

        QMessageBox.information(self, tr("common.success"), tr("settings.saved"))