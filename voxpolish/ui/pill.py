import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, pyqtProperty
from PyQt6.QtGui import QColor, QFont

class VoxPillUI(QWidget):
    """
    Floating 'Frosted Glass' pill UI centered at the top of the monitor.
    Provides system status feedback through colors and animations.
    """
    def __init__(self):
        super().__init__()
        
        # 1. Window Flag configuration (Floating, Frameless, Always on Top)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 2. UI Layout (The Pill)
        self.setFixedSize(320, 50)
        self.container = QWidget(self)
        self.container.setObjectName("Pill")
        self.container.setFixedSize(300, 40)
        
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(10, 0, 10, 0)
        
        self.label = QLabel("Ready", self.container)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont("Segoe UI Variable Display", 11, QFont.Weight.Medium))
        self.layout.addWidget(self.label)
        
        # 3. Styling (Frosted Glass / Glassmorphism)
        self.base_style = """
            #Pill {
                background-color: rgba(30, 30, 35, 180); /* Frosted Dark */
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
            }
            QLabel {
                color: rgba(255, 255, 255, 0.9);
            }
        """
        self.setStyleSheet(self.base_style)
        
        # 4. Glow/Pulse Effect (The Pulse)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 0)) # Start transparent
        self.container.setGraphicsEffect(self.shadow)
        
        # Animation for pulsing
        self._glow_alpha = 0
        self.pulse_anim = QPropertyAnimation(self, b"glow_alpha")
        self.pulse_anim.setDuration(1200)
        self.pulse_anim.setStartValue(50)
        self.pulse_anim.setEndValue(220)
        self.pulse_anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.pulse_anim.setLoopCount(-1)
        
        # Position at top center of primary monitor
        self._center_on_screen()
        self.show()
        
        # Default state
        self.update_state("IDLE")

    @pyqtProperty(int)
    def glow_alpha(self):
        return self._glow_alpha

    @glow_alpha.setter
    def glow_alpha(self, value):
        self._glow_alpha = value
        color = self.shadow.color()
        color.setAlpha(value)
        self.shadow.setColor(color)

    def _center_on_screen(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = screen.top() + 15 # 15px from top
        self.move(x, y)

    def update_state(self, state, text=None):
        """Update UI based on application state."""
        state = state.upper()
        self.pulse_anim.stop()
        
        if state == "IDLE":
            self.label.setText(text or "Vox Ready")
            self.shadow.setColor(QColor(0, 0, 0, 0))
            self.container.setStyleSheet("background-color: rgba(30, 30, 40, 100); border: 1px solid rgba(255, 255, 255, 0.1);")
            
        elif state == "LISTENING":
            self.label.setText(text or "Listening...")
            self.shadow.setColor(QColor(0, 120, 255, 150)) # Blue
            self.pulse_anim.start()
            
        elif state == "THINKING":
            self.label.setText(text or "Polishing...")
            self.shadow.setColor(QColor(255, 180, 0, 150)) # Gold
            self.pulse_anim.start()
            
        elif state == "SUCCESS":
            self.label.setText(text or "Polished ✓")
            self.shadow.setColor(QColor(0, 255, 100, 200)) # Green
            QTimer.singleShot(1500, lambda: self.update_state("IDLE"))
            
        elif state == "ERROR":
            self.label.setText(text or "Error")
            self.shadow.setColor(QColor(255, 50, 50, 200)) # Red
            QTimer.singleShot(2500, lambda: self.update_state("IDLE"))

if __name__ == "__main__":
    # Test script to preview the pill
    app = QApplication(sys.argv)
    pill = VoxPillUI()
    
    # Cycle through states for demonstration
    states = ["LISTENING", "THINKING", "SUCCESS", "IDLE"]
    current = 0
    
    def cycle():
        global current
        pill.update_state(states[current])
        current = (current + 1) % len(states)

    timer = QTimer()
    timer.timeout.connect(cycle)
    timer.start(3000)
    
    sys.exit(app.exec())
