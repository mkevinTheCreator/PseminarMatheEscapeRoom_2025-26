from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QPainter, QColor, QPen, QIcon
from PySide6.QtCore import Qt, QSize, QRect


class PaintedCircleButton(QPushButton):
    def __init__(self, text="", icon: QIcon = None, icon_size: QSize = None, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(170, 170)
        self.setFlat(True)
        self.isActive = True
        self._icon = icon
        self._icon_size = icon_size or QSize(28, 28)  # default icon size

    def setCircleIcon(self, icon: QIcon, size: QSize = None):
        self._icon = icon
        if size:
            self._icon_size = size
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw circle background
        color = QColor("#6c80c1") if self.getActive() else QColor("#F80091")
        painter.setBrush(Qt.NoBrush)
        painter.setPen(color)
        painter.drawEllipse(self.rect())


        rect = self.rect()
        # Icon only — center it
        icon_x = (rect.width() - 4* self._icon_size.width()) // 2
        icon_y = (rect.height() - 4* self._icon_size.height()) // 2
        icon_rect = QRect(icon_x, icon_y, self._icon_size.width()*4, self._icon_size.height()*4)

        pixmap = self._icon.pixmap(self._icon_size*4)
        painter.setCompositionMode(QPainter.CompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver))

        painter.drawPixmap(icon_rect, pixmap)
    def setActive(self, state:bool):
        self.isActive = state
        self.update()

    def getActive(self):

        return self.isActive
        