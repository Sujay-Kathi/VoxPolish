import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QGraphicsDropShadowEffect, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, pyqtProperty, pyqtSignal, QPoint
from PyQt6.QtGui import QColor, QFont
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
        self.setFixedSize(self.base_width + 40, self.expanded_height + 40) # Padding for shadows
        
        # 3. Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.setContentsMargins(0, 0, 0, 20)
        
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

        # Height & Position Animations
        self.expansion_anim = QPropertyAnimation(self, b"container_height")
        self.expansion_anim.setDuration(400)
        self.expansion_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.pos_anim = QPropertyAnimation(self, b"pos")
        self.pos_anim.setDuration(450)
        self.pos_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._is_expanded = False
        self._current_state = "IDLE"
        
        # Calculate resting and idle positions
        self._setup_positions()
        self.show()

    def _setup_positions(self):
        screen = QApplication.primaryScreen().availableGeometry()
        self.center_x = (screen.width() - self.width()) // 2
        # Resting Y: Standard visible position (20px above taskbar)
        self.resting_y = screen.height() - self.height() - 5
        # Idle Y: Pushed down so only the 'bulge' top shows (~12px)
        self.idle_y = screen.height() - 45 # Window is tall, so -45 exposes the top curve
        
        self.move(self.center_x, self.idle_y)

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

    def enterEvent(self, event):
        """Roll up on hover"""
        self._animate_ui(expand=True, raise_up=True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Roll down on leave (if not busy)"""
        # Only roll down if idle
        if self._current_state == "IDLE":
            self._animate_ui(expand=False, raise_up=False)
        super().leaveEvent(event)

    def _animate_ui(self, expand: bool, raise_up: bool):
        """Unified animation for both height and position"""
        # 1. Animate Position (Slide Up/Down)
        target_y = self.resting_y if raise_up else self.idle_y
        self.pos_anim.stop()
        self.pos_anim.setEndValue(QPoint(int(self.center_x), int(target_y)))
        self.pos_anim.start()

        # 2. Animate Height (Expansion)
        if self._is_expanded != expand:
            self._is_expanded = expand
            target_h = self.expanded_height if expand else self.base_height
            self.expansion_anim.stop()
            self.expansion_anim.setEndValue(target_h)
            self.expansion_anim.start()

    def _center_on_screen(self):
        # Deprecated by _setup_positions, but kept for legacy calls
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
        
        if state == "IDLE":
            self.status_label.setText(text or "Vox Ready")
            self.shadow.setColor(QColor(0, 229, 255, 0))
            # Relax the wedge if mouse isn't over it
            if not self.underMouse():
                self._animate_ui(expand=False, raise_up=False)
            
        elif state == "LISTENING":
            self._animate_ui(expand=True, raise_up=True) # Full reveal!
            self.status_label.setText(text or "Listening...")
            self.shadow.setColor(QColor(0, 229, 255, 100)) # Cyan
            self.pulse_anim.start()
            self.preview_label.setText("Vocalize your intent...")
            self.preview_label.show()
            
        elif state == "THINKING":
            self._animate_ui(expand=True, raise_up=True)
            self.status_label.setText(text or "Polishing...")
            self.shadow.setColor(QColor(0, 255, 171, 100)) # Emerald
            self.pulse_anim.start()
            
        elif state == "SUCCESS":
            self._animate_ui(expand=True, raise_up=True)
            self.status_label.setText(text or "Polished ✓")
            self.shadow.setColor(QColor(0, 255, 171, 200))
            QTimer.singleShot(2000, lambda: self.update_state("IDLE"))

        elif state == "ERROR":
            self.status_label.setText(text or "Error")
            self.shadow.setColor(QColor(255, 113, 108, 200)) # Error Red
            QTimer.singleShot(3000, lambda: self.update_state("IDLE"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wedge = VoxWedgeUI()
    sys.exit(app.exec())
