from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QScrollArea, QFrame, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor

class GlassCard(QFrame):
    def __init__(self, title, content_text, parent=None):
        super().__init__(parent)
        self.setObjectName("GlassCard")
        self.setStyleSheet("""
            #GlassCard {
                background-color: rgba(23, 26, 31, 150);
                border: 1px solid rgba(129, 236, 255, 0.1);
                border-radius: 15px;
            }
        """)
        self.setMinimumHeight(80)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Inter", 10, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #00E5FF;") # Cyan Primary
        
        content_label = QLabel(content_text)
        content_label.setFont(QFont("Inter", 9))
        content_label.setStyleSheet("color: #aaabb0;")
        content_label.setWordWrap(True)
        
        layout.addWidget(title_label)
        layout.addWidget(content_label)
        layout.addStretch()

class VoxDashboardUI(QWidget):
    """
    Native 'Aetheric Flux' Dashboard UI.
    """
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("VoxPolish Dashboard")
        self.setFixedSize(450, 700)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Frameless window, but let's keep it tool style
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool
        )
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.container = QWidget(self)
        self.container.setObjectName("DashboardContainer")
        self.container.setStyleSheet("""
            #DashboardContainer {
                background-color: rgba(12, 14, 18, 240);
                border: 1px solid rgba(129, 236, 255, 0.2);
                border-radius: 20px;
            }
        """)
        
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(25, 25, 25, 25)
        container_layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("VoxPolish")
        title.setFont(QFont("Manrope", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #f6f6fc;")
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #aaabb0;
                font-size: 14pt;
                border: none;
            }
            QPushButton:hover {
                color: #ff716c;
            }
        """)
        close_btn.clicked.connect(self.hide)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(close_btn)
        
        # Metrics Row
        metrics_layout = QHBoxLayout()
        metrics_layout.addWidget(GlassCard("Latency", "< 200ms\nTarget"))
        metrics_layout.addWidget(GlassCard("Accuracy", "99.8%\nTarget"))
        
        # Section Title
        history_title = QLabel("Recent Transcription")
        history_title.setFont(QFont("Inter", 12, QFont.Weight.DemiBold))
        history_title.setStyleSheet("color: #f6f6fc; margin-top: 10px;")
        
        # Scroll Area for History
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background-color: transparent;")
        
        self.history_content = QWidget()
        self.history_content.setStyleSheet("background-color: transparent;")
        self.history_layout = QVBoxLayout(self.history_content)
        self.history_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.history_layout.setContentsMargins(0, 0, 0, 0)
        self.history_layout.setSpacing(10)
        
        self.scroll.setWidget(self.history_content)
        
        # Quit Button
        self.quit_btn = QPushButton("Quit VoxPolish")
        self.quit_btn.setFixedHeight(45)
        self.quit_btn.setFont(QFont("Inter", 10, QFont.Weight.Bold))
        self.quit_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.quit_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 113, 108, 0.05);
                border: 1px solid rgba(255, 113, 108, 0.2);
                border-radius: 12px;
                color: #ff716c;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: rgba(255, 113, 108, 0.15);
                border: 1px solid rgba(255, 113, 108, 0.4);
            }
        """)
        self.quit_btn.clicked.connect(self._quit_app)
        
        container_layout.addLayout(header_layout)
        container_layout.addLayout(metrics_layout)
        container_layout.addWidget(history_title)
        container_layout.addWidget(self.scroll)
        container_layout.addWidget(self.quit_btn)
        
        self.main_layout.addWidget(self.container)
        self.refresh_history()

    def _quit_app(self):
        from PyQt6.QtWidgets import QApplication
        QApplication.quit()

    def add_history_item(self, text, mode, timestamp=""):
        time_label = f" ({timestamp[:16].replace('T', ' ')})" if timestamp else ""
        card = GlassCard(f"{mode.capitalize()} Mode{time_label}", text)
        self.history_layout.insertWidget(0, card) # Add to top

    def refresh_history(self):
        # Clear
        for i in reversed(range(self.history_layout.count())): 
            widget = self.history_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
                
        # Reload
        try:
            from voxpolish.core.data import data_manager
            records = data_manager.get_history()
            # History is reverse-chronological from data manager already
            # So if we insert at 0, we should loop reversed, or just append
            for item in reversed(records):
                self.add_history_item(item.get("text", ""), item.get("mode", ""), item.get("timestamp", ""))
        except ImportError:
            pass

    def showEvent(self, event):
        self.refresh_history()
        super().showEvent(event)

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    dash = VoxDashboardUI()
    dash.show()
    sys.exit(app.exec())
