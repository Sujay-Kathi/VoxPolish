import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QGraphicsDropShadowEffect, QGraphicsOpacityEffect, QMenu
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, pyqtProperty, pyqtSignal, QPoint, QRect
from PyQt6.QtGui import QColor, QFont, QAction
from PyQt6.QtSvgWidgets import QSvgWidget
from voxpolish.ui.dashboard import VoxDashboardUI

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class ClickableSvgWidget(QSvgWidget):
    clicked = pyqtSignal()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mouseReleaseEvent(event)

class VoxWedgeUI(QWidget):
    """
    Native floating 'Wedge' UI inspired by Wispr Flow.
    Positions itself at the bottom center of the screen.
    """
    def __init__(self):
        super().__init__()
        
        # 1. Window Configuration
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 2. Dimensions & State
        self.base_width = 320
        self.base_height = 60
        self.expanded_height = 100
        # Increased padding to prevent shadow Clipping/UpdateLayeredWindow errors
        self.padding_w = 80
        self.padding_h = 80
        self.setFixedSize(self.base_width + self.padding_w, self.expanded_height + self.padding_h)
        
        # 3. Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Floating Preview (Above the wedge)
        self.preview_label = QLabel("", self)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("color: rgba(255, 255, 255, 0.6); font-size: 10pt; margin-bottom: 5px;")
        self.preview_label.hide()
        self.main_layout.addWidget(self.preview_label)

        # The Wedge Container
        self.container = QWidget(self)
        self.container.setFixedSize(self.base_width, self.base_height)
        self.container.setObjectName("Wedge")
        
        self.layout = QHBoxLayout(self.container)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(15)

        # Icons
        self.coding_icon = QSvgWidget(resource_path(os.path.join("voxpolish", "assets", "icons", "terminal.svg")))
        self.coding_icon.setFixedSize(20, 20)
        self.coding_opacity = QGraphicsOpacityEffect()
        self.coding_opacity.setOpacity(0.4)
        self.coding_icon.setGraphicsEffect(self.coding_opacity)
        
        self.mic_icon = QSvgWidget(resource_path(os.path.join("voxpolish", "assets", "icons", "mic.svg")))
        self.mic_icon.setFixedSize(28, 28)
        
        self.status_label = QLabel("Ready", self.container)
        self.status_label.setFont(QFont("Inter", 11, QFont.Weight.Medium))
        self.status_label.setStyleSheet("color: #f6f6fc;")
        
        self.settings_icon = ClickableSvgWidget(resource_path(os.path.join("voxpolish", "assets", "icons", "settings.svg")))
        self.settings_icon.setFixedSize(20, 20)
        self.settings_icon.setCursor(Qt.CursorShape.PointingHandCursor)
        self.settings_opacity = QGraphicsOpacityEffect()
        self.settings_opacity.setOpacity(0.4)
        self.settings_icon.setGraphicsEffect(self.settings_opacity)
        
        # Dashboard UI
        self.dashboard = VoxDashboardUI()
        self.settings_icon.clicked.connect(self._toggle_dashboard)

        self.layout.addWidget(self.coding_icon)
        self.layout.addWidget(self.mic_icon)
        self.layout.addWidget(self.status_label)
        self.layout.addStretch()
        self.layout.addWidget(self.settings_icon)

        self.main_layout.addWidget(self.container)

        # 4. Styling (Glassmorphism)
        self.container.setStyleSheet("""
            #Wedge {
                background-color: rgba(12, 14, 18, 200);
                border: 1px solid rgba(129, 236, 255, 0.15);
                border-radius: 30px;
            }
        """)

        # 5. Effects & Animations
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(25)
        self.shadow.setColor(QColor(0, 229, 255, 0)) # Initial cyan glow hidden
        self.shadow.setOffset(0, 0)
        self.container.setGraphicsEffect(self.shadow)

        self._glow_alpha = 0
        self.pulse_anim = QPropertyAnimation(self, b"glow_alpha")
        self.pulse_anim.setDuration(1500)
        self.pulse_anim.setStartValue(20)
        self.pulse_anim.setEndValue(150)
        self.pulse_anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.pulse_anim.setLoopCount(-1)

        # Improved Performance for Animations
        self.height_anim = QPropertyAnimation(self, b"geometry")
        self.height_anim.setDuration(250)
        self.height_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._is_expanded = False
        self._current_state = "IDLE"
        self._hover_timer = QTimer(self)
        self._hover_timer.setSingleShot(True)
        self._hover_timer.timeout.connect(self._do_expand)
        
        self._setup_positions()
        self.show()

    def _setup_positions(self):
        screen = QApplication.primaryScreen().availableGeometry()
        total_w = self.base_width + self.padding_w
        total_h_active = self.expanded_height + self.padding_h
        
        self.center_x = (screen.width() - total_w) // 2
        
        # Geometry for both states
        # Minimized: Tiny thin trigger at the taskbar
        self.min_geo = QRect(int(self.center_x), int(screen.height() - 15), total_w, 15)
        # Resting: Standard visible height
        self.rest_geo = QRect(int(self.center_x), int(screen.height() - 85), total_w, 85)
        # Active: Expanded height for listening
        self.active_geo = QRect(int(self.center_x), int(screen.height() - total_h_active), total_w, total_h_active)
        
        self.setGeometry(self.min_geo)

    @pyqtProperty(int)
    def container_height(self):
        return self.container.height()

    @container_height.setter
    def container_height(self, value):
        self.container.setFixedHeight(value)

    @pyqtProperty(int)
    def glow_alpha(self):
        return self._glow_alpha

    @glow_alpha.setter
    def glow_alpha(self, value):
        self._glow_alpha = value
        color = self.shadow.color()
        color.setAlpha(value)
        self.shadow.setColor(color)

    def contextMenuEvent(self, event):
        """Right-click menu for quick actions like Quit"""
        menu = QMenu(self)
        menu.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint | Qt.WindowType.NoDropShadowWindowHint)
        menu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        menu.setStyleSheet("""
            QMenu {
                background-color: #0c0e12;
                color: #f6f6fc;
                border: 1px solid rgba(129, 236, 255, 0.2);
                border-radius: 12px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 12px 8px 12px;
                border-radius: 6px;
                margin: 2px;
            }
            QMenu::item:selected {
                background-color: rgba(255, 113, 108, 0.1);
                color: #ff716c;
            }
        """)
        
        quit_action = QAction("Quit VoxPolish", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        menu.addAction(quit_action)
        
        menu.exec(event.globalPos())

    def enterEvent(self, event):
        """Debounced roll up - only when idle"""
        if self._current_state in ["IDLE", "READY"]:
            self._hover_timer.start(50)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Roll down if not busy"""
        self._hover_timer.stop()
        if self._current_state in ["IDLE", "READY"]:
            self._animate_ui(state="MINIMIZED")
        super().leaveEvent(event)

    def _do_expand(self):
        """Only roll up to resting if we're not already busy with something else"""
        if self._current_state in ["IDLE", "READY"]:
            self._animate_ui(state="RESTING")

    def _animate_ui(self, state="RESTING"):
        """Performance optimized slide + scale"""
        target_geo = self.min_geo
        target_h = self.base_height
        
        if state == "RESTING":
            target_geo = self.rest_geo
            target_h = self.base_height
        elif state == "ACTIVE":
            target_geo = self.active_geo
            target_h = self.expanded_height

        # Start combined geometry animation (Faster than separate pos/size)
        self.height_anim.stop()
        self.height_anim.setEndValue(target_geo)
        self.height_anim.start()
        
        # Internal container resize
        self.container.setFixedHeight(target_h)

    def _center_on_screen(self):
        self._setup_positions()

    def _toggle_dashboard(self):
        if self.dashboard.isVisible():
            self.dashboard.hide()
        else:
            # Position dashboard above wedge
            screen = QApplication.primaryScreen().availableGeometry()
            dx = (screen.width() - self.dashboard.width()) // 2
            dy = screen.height() - self.dashboard.height() - self.height() - 40
            self.dashboard.move(dx, dy)
            self.dashboard.show()

    def update_state(self, state, text=None):
        state = state.upper()
        self._current_state = state
        
        # Check for mode change string in text
        if text and "TECHNICAL" in text:
            self.coding_opacity.setOpacity(1.0)
            self.coding_icon.setStyleSheet("background-color: rgba(0, 229, 255, 30); border-radius: 10px;")
        elif text and "PROSE" in text:
            self.coding_opacity.setOpacity(0.4)
            self.coding_icon.setStyleSheet("")
            
        self.pulse_anim.stop()
        self.preview_label.hide()
        
        if state == "IDLE" or state == "READY":
            self.status_label.setText(text or "Vox Ready")
            self.shadow.setColor(QColor(0, 229, 255, 0))
            # Relax the wedge if mouse isn't over it
            if not self.underMouse():
                self._animate_ui(state="MINIMIZED")
            
        elif state == "LISTENING":
            self._animate_ui(state="ACTIVE") 
            self.status_label.setText(text or "Listening...")
            self.shadow.setColor(QColor(0, 229, 255, 100)) # Cyan
            self.pulse_anim.start()
            self.preview_label.setText("Vocalize your intent...")
            self.preview_label.show()
            
        elif state == "THINKING" or state == "PROCESSING":
            self._animate_ui(state="ACTIVE")
            self.status_label.setText(text or "Transcribing...")
            self.shadow.setColor(QColor(0, 255, 171, 100)) # Emerald
            self.pulse_anim.start()
            
        elif state == "SUCCESS":
            self._animate_ui(state="ACTIVE")
            self.status_label.setText(text or "Transcribed ✓")
            self.shadow.setColor(QColor(0, 255, 171, 200)) # Emerald
            QTimer.singleShot(2000, lambda: self.update_state("READY"))

        elif state == "ERROR":
            self.status_label.setText(text or "Error")
            self.shadow.setColor(QColor(255, 113, 108, 200)) # Error Red
            QTimer.singleShot(3000, lambda: self.update_state("READY"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wedge = VoxWedgeUI()
    sys.exit(app.exec())
