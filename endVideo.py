
import os
import sys
from pathlib import Path

# Find where PySide6 is installed
import PySide6

pyside_dir = Path(PySide6.__file__).parent
os.add_dll_directory(str(pyside_dir))
#os.environ["QT_DEBUG_PLUGINS"] = "1"
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QStackedLayout,
    QPushButton, QSizePolicy, 
)
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget 
from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QAudioOutput


import PySide6
import PySide6.QtCore
from PySide6.QtCore import QLibraryInfo
class AutoplayVideoWidget(QWidget):
    """
    A bare QWidget that plays a video with no controls and no sound.
    Starts playing automatically as soon as it's shown (e.g. when it
    becomes the active widget in a QStackedLayout / QStackedWidget).
    Hides itself when playback finishes.
    """

    def __init__(self, video_path: str, parent=None):
        
        super().__init__(parent)
        from pathlib import Path

        #print(video_path)
        #print(Path(video_path).exists())
        #print(Path(video_path).resolve())

        #print(QLibraryInfo.path(QLibraryInfo.LibraryPath.PluginsPath))
        
        #print(
        #"Qt: v", PySide6.QtCore.__version__,
        #"\tPySide6: v", PySide6.__version__
        #)
        self.player = QMediaPlayer(self)
        self.video_path = video_path

        
    
         
        print(self.player)
        # No QAudioOutput is set -> the video plays silently.
        self.audio_output = QAudioOutput(self)
        self.audio_output.setMuted(True)   # or setVolume(0)
        self.player.setAudioOutput(self.audio_output)
        self.video_widget = QVideoWidget(self)
        self.video_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.player.setVideoOutput(self.video_widget)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.video_widget)

        self.player.setSource(QUrl.fromLocalFile(video_path))

        self.player.errorOccurred.connect(self._on_error)
        self.player.mediaStatusChanged.connect(self._on_media_status_changed)

    def _on_error(self, error, error_string):
        print(f"[Player ERROR] {error} - {error_string}")

    def _on_media_status_changed(self, status):
        print(f"[Media status] {status}")
        if status == QMediaPlayer.EndOfMedia:
            self.hide()

    def showEvent(self, event):
        super().showEvent(event)
        self.player.play()

    def hideEvent(self, event):
        super().hideEvent(event)
        self.player.stop()