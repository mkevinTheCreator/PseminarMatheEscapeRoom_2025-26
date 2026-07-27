from PySide6.QtCore import QObject, QThread, Signal
import speech_recognition as sr

class SpeechWorker(QObject):
    finished = Signal(str)      # recognized text
    failed = Signal()           # UnknownValueError
    listening_started = Signal()

    def run(self):
        r = sr.Recognizer()
        self.listening_started.emit()
        with sr.Microphone(device_index=1) as source: # set to wanted microphone
            print("Say something!")
            audio = r.listen(source)
            print("stopped")
        try:
            text = r.recognize_google(audio, language="de-DE")
            self.finished.emit(text)
        except sr.UnknownValueError:
            self.failed.emit()