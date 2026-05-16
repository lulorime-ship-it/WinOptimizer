import os
import sys

from ...i18n import tr
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QScrollArea, QPushButton, QApplication)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap


class AboutPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("ContentPage")
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel(tr("about.title"))
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(20)

        info_frame = QFrame()
        info_frame.setObjectName("AboutInfoFrame")
        info_frame.setStyleSheet("""
            #AboutInfoFrame {
                background-color: #f8f9fa;
                border-radius: 12px;
                border: 1px solid #e9ecef;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(30, 24, 30, 24)
        info_layout.setSpacing(10)

        lines = [
            ("WinOptimizer", True, "18px", "#1890ff"),
            ("", False, "", ""),
            (tr("about.version"), False, "14px", "#666"),
            (tr("about.built_with"), False, "14px", "#666"),
            ("", False, "", ""),
            (tr("about.desc1"), False, "14px", "#666"),
            (tr("about.desc2"), False, "14px", "#666"),
        ]

        for text, bold, size, color in lines:
            if not text:
                continue
            label = QLabel(text)
            label.setAlignment(Qt.AlignCenter)
            label.setWordWrap(True)
            if bold:
                fn = QFont()
                fn.setPointSize(18)
                fn.setBold(True)
                label.setFont(fn)
            if size:
                label.setStyleSheet(f"font-size: {size}; color: {color};")
            info_layout.addWidget(label)

        layout.addWidget(info_frame)

        layout.addSpacing(20)

        donation_frame = QFrame()
        donation_frame.setObjectName("DonationFrame")
        donation_frame.setStyleSheet("""
            #DonationFrame {
                background-color: #f8f9fa;
                border-radius: 12px;
                border: 1px solid #e9ecef;
            }
        """)
        donation_layout = QVBoxLayout(donation_frame)
        donation_layout.setContentsMargins(30, 24, 30, 24)
        donation_layout.setSpacing(10)

        author_title_label = QLabel(tr("about.author_title"))
        author_title_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #333;")
        donation_layout.addWidget(author_title_label)

        author_name_label = QLabel(tr("about.author_name"))
        author_name_label.setStyleSheet("font-size: 13px; color: #555;")
        donation_layout.addWidget(author_name_label)

        author_email_label = QLabel(tr("about.author_email"))
        author_email_label.setStyleSheet("font-size: 13px; color: #555;")
        donation_layout.addWidget(author_email_label)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        sep.setStyleSheet("color: #dee2e6;")
        donation_layout.addWidget(sep)

        donation_title_label = QLabel(tr("about.donation_title"))
        donation_title_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #333;")
        donation_layout.addWidget(donation_title_label)

        donation_text_label = QLabel(tr("about.donation_text"))
        donation_text_label.setWordWrap(True)
        donation_text_label.setStyleSheet("font-size: 13px; color: #555;")
        donation_layout.addWidget(donation_text_label)

        crypto_data = [
            ("XMR", "4DSQMNzzq46N1z2pZWAVdeA6JvUL9TCB2bnBiA3ZzoqEdYJnMydt5akCa3vtmapeDsbVKGPFdNkzzqTcJS8M8oyK7WGj5qMvNZRw61w6wMF"),
            ("USDT(TRC20)", "TG6DCBoQszDxc64owRZKkSHqZfcAQrqR8uM"),
            ("USDT(ERC20)", "0x4323d39BA9b6Bd0570920e63a8D3a192b4459330"),
        ]

        for name, addr in crypto_data:
            row = QHBoxLayout()
            row.setSpacing(8)

            addr_label = QLabel(f"{name}: {addr}")
            addr_label.setWordWrap(True)
            addr_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            addr_label.setStyleSheet(
                "font-family: 'Consolas', 'Courier New', monospace; "
                "font-size: 12px; color: #333; background-color: #fff; "
                "padding: 6px 10px; border-radius: 6px;"
            )

            copy_btn = QPushButton("\U0001f4cb \u590d\u5236")
            copy_btn.setMaximumWidth(60)
            copy_btn.setStyleSheet(
                "QPushButton { font-size: 11px; padding: 4px 8px; "
                "background-color: #e9ecef; border: 1px solid #ced4da; border-radius: 4px; }"
                "QPushButton:hover { background-color: #dee2e6; }"
            )
            copy_btn.clicked.connect(lambda checked, a=addr: QApplication.clipboard().setText(a))

            row.addWidget(addr_label)
            row.addWidget(copy_btn)
            donation_layout.addLayout(row)

        qr_title_label = QLabel(tr("about.scan_qr"))
        qr_title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
        donation_layout.addWidget(qr_title_label)

        base = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        erweima_dir = os.path.join(base, "src", "core", "erweima")
        if not os.path.isdir(erweima_dir):
            erweima_dir = os.path.join(base, "erweima")

        qr_row = QHBoxLayout()
        qr_row.setSpacing(20)

        qr_data = [
            ("XMR", "xmr"),
            ("USDT(TRC20)", "usdt-tr20"),
            ("USDT(ERC20)", "usdt-erc20"),
        ]

        for coin_name, filename_base in qr_data:
            container = QVBoxLayout()
            container.setAlignment(Qt.AlignCenter)

            img_label = QLabel()
            img_label.setAlignment(Qt.AlignCenter)
            img_label.setMinimumSize(150, 150)

            img_found = False
            for ext in [".png", ".jpg", ".jpeg"]:
                img_path = os.path.join(erweima_dir, filename_base + ext)
                if os.path.exists(img_path):
                    pixmap = QPixmap(img_path)
                    if not pixmap.isNull():
                        pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        img_label.setPixmap(pixmap)
                        img_found = True
                        break

            if not img_found:
                img_label.setText("QR code not found")
                img_label.setStyleSheet("color: #999; font-size: 12px;")

            container.addWidget(img_label)

            coin_label = QLabel(coin_name)
            coin_label.setAlignment(Qt.AlignCenter)
            coin_label.setStyleSheet("font-size: 12px; color: #666; margin-top: 4px;")
            container.addWidget(coin_label)

            qr_row.addLayout(container)

        donation_layout.addLayout(qr_row)

        layout.addWidget(donation_frame)

        layout.addStretch()

        copyright_label = QLabel(tr("about.copyright"))
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setStyleSheet("color: #aaa; font-size: 12px;")
        layout.addWidget(copyright_label)

        scroll.setWidget(content)
        main_layout.addWidget(scroll)