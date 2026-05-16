from ...i18n import tr
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("ContentPage")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel(tr("home.title"))
        title.setObjectName("HomeTitle")
        title_font = QFont()
        title_font.setPointSize(28)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel(tr("home.subtitle"))
        subtitle.setObjectName("HomeSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #666; font-size: 14px; margin-bottom: 20px;")
        layout.addWidget(subtitle)

        layout.addSpacing(20)

        feature_frame = QFrame()
        feature_frame.setObjectName("HomeFeatureFrame")
        feature_frame.setStyleSheet("""
            #HomeFeatureFrame {
                background-color: #f8f9fa;
                border-radius: 12px;
                border: 1px solid #e9ecef;
            }
        """)
        feature_layout = QVBoxLayout(feature_frame)
        feature_layout.setContentsMargins(30, 24, 30, 24)
        feature_layout.setSpacing(12)

        features = [
            ("⚡ " + tr("home.feature_optimization"), tr("home.feature_optimization_desc")),
            ("🧹 " + tr("home.feature_cleanup"), tr("home.feature_cleanup_desc")),
            ("📦 " + tr("home.feature_office"), tr("home.feature_office_desc")),
            ("🔑 " + tr("home.feature_activation"), tr("home.feature_activation_desc")),
            ("📲 " + tr("home.feature_appx"), tr("home.feature_appx_desc")),
            ("🛡️ " + tr("home.feature_defender"), tr("home.feature_defender_desc")),
        ]

        for icon_title, desc in features:
            item_label = QLabel(f"{icon_title}")
            item_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #333;")
            feature_layout.addWidget(item_label)

            desc_label = QLabel(f"    {desc}")
            desc_label.setStyleSheet("font-size: 13px; color: #888; margin-bottom: 4px;")
            desc_label.setWordWrap(True)
            feature_layout.addWidget(desc_label)

        layout.addWidget(feature_frame)

        layout.addSpacing(20)

        tip = QLabel(tr("home.tip"))
        tip.setAlignment(Qt.AlignCenter)
        tip.setStyleSheet("color: #aaa; font-size: 13px;")
        layout.addWidget(tip)

        layout.addStretch()