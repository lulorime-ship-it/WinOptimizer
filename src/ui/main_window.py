from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                                QPushButton, QLabel, QStackedWidget, QFrame)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon

from ..i18n import tr
from .pages.home_page import HomePage
from .pages.optimization_page import OptimizationPage
from .pages.cleanup_page import CleanupPage
from .pages.office_page import OfficePage
from .pages.activation_page import ActivationPage
from .pages.appx_page import AppxPage
from .pages.defender_page import DefenderPage
from .pages.edge_page import EdgePage
from .pages.backup_page import BackupPage
from .pages.faq_page import FAQPage
from .pages.about_page import AboutPage
from .pages.settings_page import SettingsPage

NAV_ICONS = ["🏠", "⚡", "🔄", "🧹", "📦", "🔑", "📲", "🛡️", "🌐", "❓", "⚙", "ℹ️"]
NAV_KEYS = ["home", "optimization", "backup", "cleanup", "office", "activation", "appx", "defender", "edge", "faq", "settings", "about"]


class NavButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(44)
        self.setMaximumHeight(44)

    def set_nav_text(self, icon_text, text):
        self.setText(f"  {icon_text}  {text}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(tr("main.title"))
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)

        self._init_ui()
        self._apply_style()

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        root_layout = QHBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.sidebar = self._create_sidebar()
        root_layout.addWidget(self.sidebar)

        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("ContentStack")
        root_layout.addWidget(self.content_stack, 1)

        self._setup_pages()
        self._connect_nav()

    def _create_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(200)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        title_container = QWidget()
        title_container.setFixedHeight(64)
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(20, 16, 20, 8)
        title_layout.setSpacing(0)

        self.title_label = QLabel(tr("main.sidebar_title"))
        self.title_label.setObjectName("SidebarTitle")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        title_layout.addWidget(self.title_label)

        layout.addWidget(title_container)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setObjectName("SidebarSeparator")
        separator.setFixedHeight(1)
        layout.addWidget(separator)

        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(8, 8, 8, 8)
        nav_layout.setSpacing(2)

        self.nav_buttons = []
        for idx, nav_key in enumerate(NAV_KEYS):
            btn = NavButton()
            btn.setObjectName("NavButton")
            btn.set_nav_text(NAV_ICONS[idx], tr(f"nav.{nav_key}"))
            nav_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        nav_layout.addStretch()
        layout.addWidget(nav_container, 1)

        self.admin_indicator = QLabel()
        self.admin_indicator.setObjectName("AdminIndicator")
        self.admin_indicator.setAlignment(Qt.AlignCenter)
        self.admin_indicator.setFixedHeight(28)
        self.admin_indicator.setCursor(Qt.PointingHandCursor)
        self._update_admin_indicator()
        layout.addWidget(self.admin_indicator)

        self.version_label = QLabel("v1.0")
        self.version_label.setObjectName("VersionLabel")
        self.version_label.setAlignment(Qt.AlignCenter)
        self.version_label.setFixedHeight(32)
        layout.addWidget(self.version_label)

        return sidebar

    def _update_admin_indicator(self):
        if self._check_admin():
            self.admin_indicator.setText("🔒 " + tr("admin.mode"))
            self.admin_indicator.setStyleSheet("color: #52c41a; font-size: 11px; font-weight: bold; background: transparent;")
        else:
            self.admin_indicator.setText("⚠ " + tr("admin.user_mode"))
            self.admin_indicator.setStyleSheet("color: #faad14; font-size: 11px; font-weight: bold; background: transparent;")

    def refresh_language(self):
        self.setWindowTitle(tr("main.title"))
        self.title_label.setText(tr("main.sidebar_title"))
        for idx, btn in enumerate(self.nav_buttons):
            btn.set_nav_text(NAV_ICONS[idx], tr(f"nav.{NAV_KEYS[idx]}"))
        self._update_admin_indicator()

    def _setup_pages(self):
        self.pages = {
            0: HomePage(),
            1: OptimizationPage(),
            2: BackupPage(),
            3: CleanupPage(),
            4: OfficePage(),
            5: ActivationPage(),
            6: AppxPage(),
            7: DefenderPage(),
            8: EdgePage(),
            9: FAQPage(),
            10: SettingsPage(),
            11: AboutPage(),
        }

        for index, page in self.pages.items():
            self.content_stack.addWidget(page)

        settings_page = self.pages[10]
        settings_page.languageChanged.connect(self._on_language_changed)

        self.nav_buttons[0].setChecked(True)
        self.content_stack.setCurrentIndex(0)

    def _connect_nav(self):
        for idx, btn in enumerate(self.nav_buttons):
            btn.clicked.connect(lambda checked, i=idx: self._on_nav_clicked(i))

    def _on_nav_clicked(self, index):
        for btn in self.nav_buttons:
            btn.setChecked(False)
        self.nav_buttons[index].setChecked(True)
        self.content_stack.setCurrentIndex(index)

    def _on_language_changed(self, lang):
        current_index = self.content_stack.currentIndex()

        while self.content_stack.count() > 0:
            w = self.content_stack.widget(0)
            self.content_stack.removeWidget(w)
            w.deleteLater()

        self._setup_pages()

        self.refresh_language()

        target = min(current_index, self.content_stack.count() - 1)
        self.nav_buttons[target].setChecked(True)
        self.content_stack.setCurrentIndex(target)

    def _check_admin(self):
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            return False

    def _apply_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }

            #Sidebar {
                background-color: #ffffff;
                border-right: 1px solid #f0f0f0;
            }

            #SidebarTitle {
                color: #1890ff;
                padding: 0px;
                background: transparent;
            }

            #SidebarSeparator {
                color: #f0f0f0;
                background-color: #f0f0f0;
                border: none;
            }

            #NavButton {
                background-color: transparent;
                border: none;
                border-radius: 6px;
                text-align: left;
                padding-left: 16px;
                font-size: 13px;
                color: #595959;
                font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
            }

            #NavButton:hover {
                background-color: #e6f7ff;
                color: #1890ff;
            }

            #NavButton:checked {
                background-color: #e6f7ff;
                color: #1890ff;
                font-weight: bold;
            }

            #VersionLabel {
                color: #bfbfbf;
                font-size: 12px;
                font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
                background: transparent;
            }

            #ContentStack {
                background-color: #f0f2f5;
            }

            QWidget#ContentPage {
                background-color: #ffffff;
                border-radius: 8px;
                margin: 16px;
            }
        """)