from PySide6.QtCore import QTimer
from PySide6.QtGui import QPainter, QPixmap, Qt
from PySide6.QtWidgets import QWidget
import os
import sys
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path,relative_path)
class Rocket(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(75, 75)
        self.angle = 0
        self.solved = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.timer.start(16)  # ~60fps
        self.move(2000,2000)

    def rotate(self):
        if self.solved == False:
            self.angle = (self.angle + 2) % 360
            self.update()  # triggers paintEvent

    def setAngle(self, angle):

        self.angle = -90 + angle
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(resource_path("media\\textures\\rocket.png")).scaled(
            self.width(), self.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self.angle)
        painter.drawPixmap(-pixmap.width() // 2, -pixmap.height() // 2, pixmap)

