from PySide6.QtCore import QSize
from PySide6.QtGui import QMovie
from PySide6.QtWidgets import QLabel
import os
import sys
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path,relative_path)

class movie(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(70, 70)
        movie = QMovie(resource_path("media\\textures\\globe.gif"))
        movie.setScaledSize(QSize(70, 70))
        movie.setSpeed(70)
        self.setMovie(movie)
        movie.start()
        self.move(310, 210)