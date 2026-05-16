from ...i18n import tr
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame,
                             QScrollArea)
from PySide6.QtCore import Qt


class FAQPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("ContentPage")
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel(tr("faq.header"))
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(20)

        faqs = [
            (tr("faq.q1"), tr("faq.a1")),
            (tr("faq.q2"), tr("faq.a2")),
            (tr("faq.q3"), tr("faq.a3")),
            (tr("faq.q4"), tr("faq.a4")),
            (tr("faq.q5"), tr("faq.a5")),
            (tr("faq.q6"), tr("faq.a6")),
            (tr("faq.q7"), tr("faq.a7")),
            (tr("faq.q8"), tr("faq.a8")),
        ]

        for question, answer in faqs:
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: #f8f9fa;
                    border-radius: 8px;
                    border: 1px solid #e9ecef;
                    padding: 16px;
                }
            """)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(16, 12, 16, 12)
            card_layout.setSpacing(8)

            q_label = QLabel(question)
            q_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
            q_label.setWordWrap(True)
            card_layout.addWidget(q_label)

            a_label = QLabel(answer)
            a_label.setStyleSheet("font-size: 13px; color: #666;")
            a_label.setWordWrap(True)
            card_layout.addWidget(a_label)

            layout.addWidget(card)
            layout.addSpacing(8)

        layout.addStretch()

        scroll_area.setWidget(content)
        main_layout.addWidget(scroll_area)